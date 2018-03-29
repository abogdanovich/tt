# -*- coding: utf-8 -*-
__author__ = 'ABKorotky'
__email__ = ['akorotky@minsk.ximxim.com', 'aleksandr.korotky@ximad.com']


from datetime import date
from django.db import models

from cv.models import CV, Skill
from customers.models import Customer


PROJECT_STATE = (
    (0, "Prepare"),
    (1, "Development"),
    (2, "Pause"),
    (3, "Close"),
    (4, "Finish"),
)


class Preset(models.Model):
    """
    project preset info
    """
    title = models.CharField("Title", max_length=200)
    challenge = models.TextField("Business Challenge", blank=True, default="")
    service = models.CharField("Service", max_length=100, blank=True, default="")
    industry = models.CharField("Industry", max_length=100, blank=True, default="")
    solution=models.TextField("Solution highlight", blank=True, default="")

    class Meta:
        verbose_name = "Preset"
        verbose_name_plural = "Presets"
        unique_together = ('title', )

    def __unicode__(self):
        return self.title


class PresetRequirement(models.Model):
    """
    class for attach and store the list of requirements to current project
    """
    preset = models.ForeignKey(Preset, verbose_name="Preset", related_name="requirements", null=True, help_text="")
    skill = models.ForeignKey(Skill, verbose_name="Skill", related_name="presets", null=True, default=None, help_text="")
    desc = models.TextField("Text Description", blank=True, null=True, help_text="contain the text description of needed requirements by select skill")

    class Meta:
        verbose_name = "Project Requirement"
        verbose_name_plural ="Project Requirements"
        unique_together = ('preset', 'skill')

    def __unicode__(self):
        return self.skill.name

    def get_tags(self):
        """
        build and return the list of tags.
        """
        if self.desc:
            return tuple(map(unicode.strip, self.desc.split(',')))
        return ()

    def has_tag(self, tag):
        """
        check is tag in this requirement or not.
        """
        if tag in self.get_tags():
            return True
        return False


# ----- PROJECT MANAGERS -----
class PrepareProjectManager(models.Manager):
    def get_query_set(self):
        return super(PrepareProjectManager, self).get_query_set().filter(models.Q(date_start=None)|models.Q(date_start__gt=date.today()))


class DevelopProjectManager(models.Manager):
    def get_query_set(self):
        today = date.today()
        return super(DevelopProjectManager, self).get_query_set().filter(models.Q(date_start__lte=today), models.Q(date_finish=None)|models.Q(date_finish__gte=today))

    def work(self):
        return self.get_query_set().filter(pause=False)

    def pause(self):
        return self.get_query_set().filter(pause=True)

class FinishProjectManager(models.Manager):
    def get_query_set(self):
        today = date.today()
        return super(FinishProjectManager, self).get_query_set().filter(date_start__lte=date.today(), date_finish__lt=date.today())


class Project(models.Model):
    """
    project info
    """
    title = models.CharField("Title", max_length=200)
    challenge = models.TextField("Business Challenge", blank=True, default="")
    customer = models.ForeignKey(Customer, verbose_name="Customer", related_name="projects")
    benefits = models.TextField("Benefits for Customer", blank=True, default="")
    feedback=models.TextField("Customer's feedback", blank=True, default="")
    service = models.CharField("Service", max_length=100, blank=True, default="")
    industry = models.CharField("Industry", max_length=100, blank=True, default="")
    solution=models.TextField("Solution highlight", blank=True, default="")
    dev_time = models.IntegerField("Development Time (in hours)", blank=True, null=True, default=0)
    date_start = models.DateField("Start Date", blank=True, null=True)
    date_finish = models.DateField("Finish Date", blank=True, null=True)
    pause = models.BooleanField("Project is in pause", default=False)
    preset = models.ForeignKey(Preset, verbose_name="Project Preset", blank=True, null=True, default=None, related_name="projects")

    objects = models.Manager()
    prepare = PrepareProjectManager()
    develop = DevelopProjectManager()
    finish = FinishProjectManager()

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        #return ('projects.views.project.view_vf', [], {'project': self.id})
        return ('erp_project', [], {'prj_id': self.id})

    def get_cvs(self):
        """
        return the tuple of cv which are containing in current work group. format: (cv, ...).
        """
        return tuple(wg.cv for wg in self.wg.all())

    def get_reqs(self):
        """
        return the tuple of requirements (obj_Skill, ...).
        """
        return tuple(req.skill for req in self.requirements.all() if req.desc)

    def has_req(self, req):
        """
        check is req_obj in requirements list or not.
        """
        try:
            self.requirements.get(project=self, skill=req)
            return True
        except Exception:
            return False

    def get_tags(self, req=None, reqs=()):
        """
        build and return the dictionary in format: {req_obj: [tag1, tag2, tag3, ...], ...}
        """
        if req:
            try:
                prj_req = self.requirements.get(skill=req, desc__isnull=False)
                return prj_req.get_tags()
            except Exception:
                return ()
        elif reqs:
            tags = {}
            for prj_req in self.requirements.filter(skill__in=reqs, desc__isnull=False):
                tags[prj_req.skill] = prj_req.get_tags()
            return tags
        else:
            tags = {}
            for prj_req in self.requirements.filter(desc__isnull=False):
                tags[prj_req.skill] = prj_req.get_tags()
            return tags

    def has_tag(self, tag, req=None):
        """
        check is tag in any requirement or not.
        if req is present than check only in this req.
        """
        if req:
            try:
                if self.requirements.get(cv=self, skill=req).has_tag(tag):
                    return True
                return False
            except Exception:
                return False
        else:
            for req in self.requirements.filter(desc__isnull=False):
                if req.has_tag(tag):
                    return True
            return False

    def is_prepare(self):
        """
        check prepare state
        """
        if self.date_start and self.date_start > date.today():
            return True
        else:
            return False

    def is_develop(self):
        """
        check development state
        """
        if (self.date_start and self.date_start <= date.today()) and (not self.date_finish or (self.date_finish and self.date_finish >= date.today())):
            return True
        else:
            return False

    def is_work(self):
        """
        check work (not pause) state (it is development substate!!!)
        """
        if (self.date_start and self.date_start <= date.today()) and (not self.date_finish or (self.date_finish and self.date_finish >= date.today())) and self.pause == False:
            return True
        else:
            return False

    def is_pause(self):
        """
        check pause state (it is development substate!!!)
        """
        if (self.date_start and self.date_start <= date.today()) and (not self.date_finish or (self.date_finish and self.date_finish >= date.today())) and self.pause:
            return True
        else:
            return False

    def is_finish(self):
        """
        check finish state
        """
        if self.date_finish and self.date_finish < date.today():
            return True
        else:
            return False

    def get_state(self):
        if self.is_prepare():
            return "prepare"
        elif self.is_develop():
            return "develop"
        elif self.is_finish():
            return "finish"
        else:
            return ""


class Screenshot(models.Model):
    """
    store screenshots for projects
    """
    project = models.ForeignKey(Project, verbose_name="Project", related_name="screenshots")
    image=models.ImageField(upload_to="projects/screenshots", verbose_name="Image")
    desc = models.CharField("Briefly Description", max_length=255, blank=True, default="")

    class Meta:
        verbose_name = "Screenshot"
        verbose_name_plural = "Screenshots"

    def __unicode__(self):
        return self.image.name


class WorkGroup(models.Model):
    """
    data for persons who are working about project
    """
    project = models.ForeignKey(Project, verbose_name="Project", related_name="wg")
    cv = models.ForeignKey(CV, verbose_name="Employee", related_name="wg")
    role = models.CharField("Role", max_length=100)
    desc = models.TextField("Description of Role", blank=True, default="")
    date_start = models.DateField("Start Date")
    date_finish = models.DateField("Finish Date", blank=True, null=True, default=None)

    class Meta:
        verbose_name = "Work Group"
        verbose_name_plural = "Work Groups"
        unique_together = ('project', 'cv')

    def __unicode__(self):
        return self.cv


class ProjectRequirement(models.Model):
    """
    class for attach and store the list of requirements to current project
    """
    project = models.ForeignKey(Project, verbose_name="Project", related_name="requirements", null=True, help_text="")
    skill = models.ForeignKey(Skill, verbose_name="Skill", related_name="projects", null=True, default=None, help_text="")
    desc = models.TextField("Text Description", blank=True, null=True, help_text="contain the text description of needed requirements by select skill")

    class Meta:
        verbose_name = "Project Requirement"
        verbose_name_plural ="Project Requirements"
        unique_together = ('project', 'skill')

    def __unicode__(self):
        return self.skill.name

    def get_tags(self):
        """
        build and return the list of tags.
        """
        if self.desc:
            return tuple(map(unicode.strip, self.desc.split(',')))
        return ()

    def has_tag(self, tag):
        """
        check is tag in this requirement or not.
        """
        if tag in self.get_tags():
            return True
        return False