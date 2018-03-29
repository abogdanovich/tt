# -*- coding: utf-8 -*-
__author__ = 'ABKorotky'
__email__ = ['akorotky@minsk.ximxim.com', 'aleksandr.korotky@ximad.com']


from django.db import models
from timecard.models import User as ttUser
from permissions import PERMISSIONS

DEFAULT_LEVEL = 0
MANAGE_LEVEL = 4
ACCESS_LEVELS = (
    (DEFAULT_LEVEL, "default"),
    (MANAGE_LEVEL, "managers")
)
FLS = (
    ('en', 'English'),
    ('ge', 'German'),
    ('it', 'Italian'),
    ('fr', 'French'),
    ('sp', 'Spain'),
    ('ch', 'China'),
)
FL_LEVELS = (
    (10, 'basic'),
    (20, 'advanced'),
    (30, 'fluent'),
)
SKILL_LEVELS = (
    (0, 'none'),
    (10, 'junior'),
    (20, 'middle'),
    (30, 'senior'),
)
DEFAULT_TEXT_NO_DATA = ""

class Skill(models.Model):
    """
    skill info.
    """
    name = models.CharField("Name", max_length=50)
    desc = models.TextField("Description", blank=True, null=True, default=None)
    on_main = models.BooleanField("Show on Home page", default=False)

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural ="Skills"
        unique_together = ('name', )

    def __unicode__(self):
        return self.name

    def get_cvs(self):
        return tuple(cv_skill.cv for cv_skill in self.cvs.filter(cv__fired=False))

    def get_tags_nums(self):
        tags = {}
        for cv_skill in self.cvs.filter(cv__fired=False):
            for tag in cv_skill.get_tags():
                if not tags.get(tag):
                    tags[tag] = 1
                else:
                    tags[tag] += 1
        return tags


class InProjectManager(models.Manager):
    def get_query_set(self):
        return super(InProjectManager, self).get_query_set().filter(in_projects=True)


class Position(models.Model):
    """
    position data. position - it`s group of some skills.
    """
    name = models.CharField("Position", max_length=200, help_text="Contain such positions, as GM, PM, HRM, Developer, Designer, Copywriter, etc...")
    in_projects = models.BooleanField("Use in Projects", default=False, help_text="")
    permissions = models.CharField("Permissions", max_length=55, default="0"*55, help_text="Contain Permissions for access to different parts of ERP System.")

    objects = models.Manager()
    projects = InProjectManager()

    class Meta:
        verbose_name = "Position"
        verbose_name_plural = "Positions"
        unique_together = ('name', )

    def __unicode__(self):
        return self.name

    def get_cvs(self):
        return tuple(cv for cv in self.cvs.filter(fired=False) if cv.skills.count())

    def get_cvs_without_wg(self, wg_cvs=()):
        return tuple(cv for cv in self.cvs.filter(fired=False) if cv.skills.count() and (cv not in wg_cvs))


class CVActiveManager(models.Manager):
    def get_query_set(self):
        return super(CVActiveManager, self).get_query_set().filter(fired=False)

    def empty_positions(self):
        return self.get_query_set().filter(position__isnull=True)

    def empty_fls(self):
        return self.get_query_set().select_related('fl').annotate(num_fls=models.Count('fl')).filter(num_fls=0)

    def empty_skills(self):
        return self.get_query_set().select_related('skills').annotate(num_skills=models.Count('skills')).filter(num_skills=0)

    def empty_projects(self):
        return self.get_query_set().select_related('wg').filter(position__in=Position.projects.all()).annotate(num_projects=models.Count('wg')).filter(num_projects=0)

    def fulls(self):
        return self.get_query_set().select_related('fl', 'skills', 'wg').exclude(position__isnull=True)\
            .annotate(num_fls=models.Count('fl'), num_skills=models.Count('skills'), num_projects=models.Count('wg'))\
            .exclude(num_fls=0).exclude(num_skills=0).exclude(num_projects=0)

class CVFiredManager(models.Manager):
    def get_query_set(self):
        return super(CVFiredManager, self).get_query_set().filter(fired=True)

class CV(models.Model):
    """
    user curriculum vitae
    """
    name = models.CharField("Name", max_length=50, help_text="Contain a first name of employee.\nIn English!!!!")
    surname = models.CharField("Surname", max_length=50, help_text="Contain a last name of employee.\nIn English!!!!")
    position = models.ForeignKey(Position, verbose_name="Position", blank=True, null=True, related_name="cvs", help_text="Contain a position for current user.\nEach position has some skills.")
    login = models.CharField("Login", max_length=50, help_text="Contain LDAP UserName for account")
    user = models.OneToOneField(ttUser, verbose_name="User from TimeTrack", blank=True, null=True, help_text="Contain a identifier to User TimeTrack data.")
    fired = models.BooleanField("Fired Employee", default=False)
    edit_fl = models.BooleanField("Edit Foreign Language", default=True, help_text="Employee can edit their foreign language data.")
    edit_skills = models.BooleanField("Edit Technical Expertise", default=True, help_text="Employee can edit their position skills.")

    objects = models.Manager()
    actives = CVActiveManager()
    fireds = CVFiredManager()

    class Meta:
        verbose_name = "Curriculum Vitae"
        verbose_name_plural = "Curriculum Vitaes"
        unique_together = ('login', )

    def __unicode__(self):
        return u"%s %s" % (self.name, self.surname)

    def get_user_name(self):
        return "%s %s" % (self.user.name, self.user.surname)

    def get_skills(self):
        return tuple(cv_skill.skill for cv_skill in self.skills.all() if cv_skill.desc)

    def has_skill(self, skill):
        try:
            self.skills.get(cv=self, skill=skill)
            return True
        except Exception:
            return False

    def get_tags(self, skill=None, skills=()):
        if skill:
            try:
                cv_skill = self.skills.get(skill=skill, desc__isnull=False)
                return cv_skill.get_tags()
            except Exception:
                return ()
        elif skills:
            tags = {}
            for cv_skill in self.skills.filter(skill__in=skills, desc__isnull=False):
                tags[cv_skill.skill] = cv_skill.get_tags()
            return tags
        else:
            tags = {}
            for cv_skill in self.skills.filter(desc__isnull=False):
                tags[cv_skill.skill] = cv_skill.get_tags()
            return tags

    def get_needed_tags(self, prj_tags):
        tags = self.get_tags()
        needed = {}
        for key, present_tags in tags.items():
            if prj_tags.get(key):
                good_tags = set(present_tags) & set(prj_tags[key])
                if good_tags:
                    needed[key] = tuple(good_tags)
        return needed


    def has_tag(self, tag, skill=None):
        if skill:
            try:
                if self.skills.get(cv=self, skill=skill).has_tag(tag):
                    return True
                return False
            except Exception:
                return False
        else:
            for cv_skill in self.skills.filter(desc__isnull=False):
                if cv_skill.has_tag(tag):
                    return True
            return False

    def get_projects(self):
        prjs = {
            'prepare': 0,
            'develop': 0,
            'work': 0,
            'pause': 0,
            'finish': 0,
        }
        for wg in self.wg.select_related('project').all():
            st = wg.project.get_state()
            prjs[st] += 1
            if st == 'develop':
                if wg.project.is_pause():
                    st = 'pause'
                else:
                    st = 'work'
                prjs[st] += 1
        return prjs


class Contact(models.Model):
    """
    cv addition contact info
    """
    cv = models.ForeignKey(CV, verbose_name="Curriculum Vitae", related_name="contacts")
    name = models.CharField("Contact Name", max_length=50, help_text="contain the name of contact such as 'work phone', 'twitter account', etc... ")
    val = models.CharField("Contact Data", max_length=100, help_text="contain value of contact such as email address, phone number, social account, etc...")

    class Meta:
        verbose_name = "CV Contact"
        verbose_name_plural = "CV Contacts"
        unique_together = ('cv', 'name')

    def __unicode__(self):
        return u"%s: %s" % (self.name, self.val)


class FL(models.Model):
    """
    user foreign languages skills
    """
    cv = models.ForeignKey(CV, verbose_name="Curriculum Vitae", related_name="fl", editable=False)
    language = models.CharField("Language", max_length=2, choices=FLS, help_text="Contain name of foreign language.")
    spoken = models.SmallIntegerField("Spoken Skill", choices=FL_LEVELS, help_text="Contain of spoken skill of this language.")
    written = models.SmallIntegerField("Written Skill", choices=FL_LEVELS, help_text="Contain of written skill of this language.")

    class Meta:
        verbose_name = "Foreign Language"
        verbose_name_plural ="Foreign Languages"
        unique_together = ('cv', 'language')

    def __unicode__(self):
        return self.get_language_display()


class CVSkillsManager(models.Manager):
    def get_query_set(self):
        return super(CVSkillsManager, self).get_query_set().filter(desc__isnull=False)

class CVSkill(models.Model):
    """
    class for attach and store skills to current CV
    """
    cv = models.ForeignKey(CV, verbose_name="Curriculum Vitae", related_name="skills", null=True, help_text="")
    skill = models.ForeignKey(Skill, verbose_name="Skill", related_name="cvs", null=True, default=None, help_text="")
    desc = models.TextField("Text Description", blank=True, null=True, default="", help_text="")

    objects = models.Manager()
    desc_skills = CVSkillsManager()
    class Meta:
        verbose_name = "CV Skill"
        verbose_name_plural ="CV Skills"
        unique_together = ('cv', 'skill')

    def __unicode__(self):
        return self.skill.name

    def get_tags(self):
        if self.desc:
            return tuple(map(unicode.strip, self.desc.split(',')))
        return ()

    def has_tag(self, tag):
        if tag in self.get_tags():
            return True
        return False


class Certificate(models.Model):
    cv = models.ForeignKey(CV, verbose_name="Curriculum Vitae", related_name="certificates")
    title = models.CharField("Title", max_length=100)
    date = models.DateField("Date of receipt", blank=True, null=True)
    desc = models.CharField("Description", max_length=255, blank=True, null=True)
    image = models.ImageField("Image", upload_to="cv/certificates", blank=True, null=True)

    class Meta:
        verbose_name = "CV Certificate"
        verbose_name_plural = "CV Certificates"
        unique_together = ('cv', 'title')

    def __unicode__(self):
        return self.title


class PrevProject(models.Model):
    """
    store data about CV previous projects (from earlier workplaces).
    """
    cv = models.ForeignKey(CV, verbose_name="Curriculum Vitae", related_name="prev_projects")
    title = models.CharField("Title", max_length=100)
    challenge = models.TextField("Briefly Description", blank=True, null=True)
    role = models.CharField("Role", max_length=100, blank=True, null=True)
    desc = models.CharField("Role Description", max_length=255, blank=True, null=True)
    date_start = models.DateField("Start Date", blank=True, null=True)
    date_finish = models.DateField("Finish Date", blank=True, null=True)

    class Meta:
        verbose_name = "Previous Project"
        verbose_name_plural = "Previous Projects"
        unique_together = ('cv', 'title')

    def __unicode__(self):
        return u"%s" % self.title


class PrevScreenshot(models.Model):
    """
    store screenshots for previous projects
    """
    project = models.ForeignKey(PrevProject, verbose_name="Project", related_name="screenshots")
    image=models.ImageField(upload_to="cv/prev_projects/screenshots", verbose_name="Image")
    desc = models.CharField("Briefly Description", max_length=255, blank=True, default="")

    class Meta:
        verbose_name = "Screenshot"
        verbose_name_plural = "Screenshots"

    def __unicode__(self):
        return self.image.name


import signals