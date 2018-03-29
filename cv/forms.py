# -*- coding: utf-8 -*-
__author__ = 'ABKorotky'
__email__ = ['akorotky@minsk.ximxim.com', 'aleksandr.korotky@ximad.com']


from django.forms import Form, ModelForm
from django.forms import IntegerField, BooleanField, CharField, ModelChoiceField
from django.forms import TextInput, Select, HiddenInput, Textarea, CheckboxSelectMultiple
from django.forms.models import formset_factory, modelformset_factory, inlineformset_factory
from django.forms.util import ErrorList

from timecard.models import User as ttUser
from erp.widgets import ImgClearableFileInput
from projects.models import WorkGroup
from projects.forms import ProjectWGMForm

from models import CV, Contact, FL, Skill, CVSkill, Certificate, Position, PrevProject, PrevScreenshot


class CVMForm(ModelForm):
    class Meta:
        model = CV

    def get_user_name(self):
        return u"%s %s" % (self.instance.name, self.instance.surname)


class CVSimpleMForm(CVMForm):
    class Meta:
        model = CV
        fields = ('id', 'position', 'edit_fl', 'edit_skills')


class CVPersonalMForm(ModelForm):
    class Meta:
        model = CV
        fields = ('id', 'name', 'surname')


class CVManageMForm(CVMForm):
    class Meta:
        model = CV
        fields = ('id', 'login', 'fired', 'position')


class CVAddMForm(CVMForm):
    class Meta:
        model = CV
        fields = ('id', 'login', 'name', 'surname', 'position')


class ContactMForm(ModelForm):
    class Meta:
        model = Contact
        widgets = {
            'name': TextInput(attrs={'class': "span4"}),
            'val': TextInput(attrs={'class': "span6"}),
        }


class FLMForm(ModelForm):
    class Meta:
        model = FL


class SkillMForm(ModelForm):
    class Meta:
        model = Skill
        widgets = {
            'desc': Textarea(attrs={'cols':"100", 'rows':"3", 'class': "span6"})
        }


class SkillDelMForm(ModelForm):
    class Meta:
        model = Skill
        fields = ('id', )


class CVAddSkillMForm(ModelForm):
    check = BooleanField(label="Check", required=False)
    class Meta:
        model = Skill
        fields = ('id', )


class CVSkillMForm(ModelForm):
    class Meta:
        model = CVSkill
        fields = ('id', 'desc')
        widgets = {
            'desc': Textarea(attrs={'cols':"100", 'rows':"5", 'class': "span6"})
        }

    def get_skill_name(self):
        return self.instance.skill.name


class CertificateMForm(ModelForm):
    class Meta:
        model = Certificate
        widgets = {
            'cv': HiddenInput(),
            'title': TextInput(attrs={'class': "span6"}),
            'desc': Textarea(attrs={'cols':"100", 'rows':"5", 'class': "span6"}),
            'image': ImgClearableFileInput(),
            }


class BrieflyCertificateMForm(ModelForm):
    class Meta:
        model = Certificate
        fields = ('id',)


class CVProjectMForm(ModelForm):
    class Meta:
        model = WorkGroup
        widgets = {
            'project': HiddenInput(),
            'role': TextInput(attrs={'class': "span6"}),
            'desc': Textarea(attrs={'cols':"100", 'rows':"5", 'class': "span6"})
        }

    def clean(self):
        cd = super(CVProjectMForm, self).clean()
        project = cd.get("project")
        date_start = cd.get("date_start")
        date_finish = cd.get("date_finish")
        errs_ds = []
        errs_df = []
        if date_start < project.date_start:
            errs_ds.append("The date start is less than project date start")
        if project.date_finish and date_start > project.date_finish:
            errs_ds.append("The date start is more than project date finish")
        if date_finish:
            if date_finish < project.date_start:
                errs_df.append("The date finish is less than project date start")
            if project.date_finish and date_finish > project.date_finish:
                errs_df.append("The date finish is more than project date finish")
            if date_start > date_finish:
                errs_ds.append("The date start is more than date finish")
                errs_df.append("The date finish is less than date start")
        if errs_ds:
            if not hasattr(self._errors, 'date_start'):
                self._errors['date_start'] = ErrorList()
            for err in errs_ds:
                self._errors['date_start'].append(err)
        if errs_df:
            if not hasattr(self._errors, 'date_finish'):
                self._errors['date_finish'] = ErrorList()
            for err in errs_df:
                self._errors['date_finish'].append(err)
        return cd


class PositionMForm(ModelForm):
    class Meta:
        model = Position
        exclude = ('permissions',)
        widgets = {
            'name': TextInput(attrs={'class': "span6"})
        }


class PositionCheckboxMForm(ModelForm):
    class Meta:
        model = Position
        widgets = {'skills': CheckboxSelectMultiple(),}


class PositionBrieflyMForm(ModelForm):
    class Meta:
        model = Position
        fields = ('id', )

    def get_skills(self):
        p = u"<ul>"
        for s in self.instance.skills.all():
            p += u"<li>%s</li>" % s
        p += u"</ul>"
        return p


class PrevProjectMForm(ModelForm):
    """
    Manage the record of previous project of CV user (from earlier workplaces).
    """
    class Meta:
        model = PrevProject
        widgets = {
            'cv': HiddenInput(),
            'title': TextInput(attrs={'class': "span6"}),
            'challenge': Textarea(attrs={'cols': "100", 'rows': "5", 'class': "span6"}),
            'role': TextInput(attrs={'class': "span6"}),
            'desc': Textarea(attrs={'cols': "100", 'rows': "3", 'class': "span6"}),}


class BrieflyPrevProjectMForm(ModelForm):
    """
    Manage delete operation
    """
    class Meta:
        model = PrevProject
        fields = ('id',)

class PrevProjectSSMForm(ModelForm):
    """
    Manage the records of screenshots for cv previous projects.
    """
    class Meta:
        model = PrevScreenshot
        widgets = {
            'image': ImgClearableFileInput(),
            'desc': Textarea(attrs={'cols': "100", 'rows': "3", 'class': "span6"}),}


CV_MFormset = modelformset_factory(CV, CVMForm, extra=0)
CVSimple_MFormset = modelformset_factory(CV, CVSimpleMForm, extra=0)
CVManageMFormset = modelformset_factory(CV, CVManageMForm, extra=0, can_delete=True)
CVContactIFormset = inlineformset_factory(CV, Contact, ContactMForm, extra=0, can_delete=True)
CVFL_IFormset = inlineformset_factory(CV, FL, FLMForm, extra=1, can_delete=True)
CVSkill_IFormset = inlineformset_factory(CV, CVSkill, CVSkillMForm, extra=0, can_delete=False, fk_name='cv')
CVProject_IFormset = inlineformset_factory(CV, WorkGroup, CVProjectMForm, extra=0, can_delete=False, fk_name='cv')
SkillMFormset = modelformset_factory(Skill, SkillMForm, extra=0, can_delete=True)
SkillDelMFormset = modelformset_factory(Skill, SkillDelMForm, extra=0, can_delete=True)
PositionMFormset = modelformset_factory(Position, PositionMForm, extra=0, can_delete=True)
PositionBrieflyMFormset = modelformset_factory(Position, PositionBrieflyMForm, extra=0, can_delete=True)
CVAddSkill_MFormset = modelformset_factory(Skill, CVAddSkillMForm, extra=0)

CertificateMFormset = modelformset_factory(Certificate, CertificateMForm, extra=1, can_delete=True)
CertificateIFormset = inlineformset_factory(CV, Certificate, CertificateMForm, extra=1, can_delete=True)
BrieflyCertificateIFormset = inlineformset_factory(CV, Certificate, BrieflyCertificateMForm, extra=0, can_delete=True)

PrevProjectMFormset = modelformset_factory(PrevProject, PrevProjectMForm, extra=0, can_delete=True)
PrevProjectIFormset = inlineformset_factory(CV, PrevProject, BrieflyPrevProjectMForm, extra=0, can_delete=True)
PrevProjectSSIFormset = inlineformset_factory(PrevProject, PrevScreenshot, PrevProjectSSMForm, fk_name="project", extra=1, max_num=5, can_delete=True)
