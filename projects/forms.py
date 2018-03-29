# -*- coding: utf-8 -*-
__author__ = 'ABKorotky'
__email__ = ['akorotky@minsk.ximxim.com', 'aleksandr.korotky@ximad.com']


from datetime import date
from django.forms import Form, ModelForm
from django.forms import IntegerField, BooleanField, CharField, ModelChoiceField
from django.forms import TextInput, Select, HiddenInput, Textarea
from django.forms.models import formset_factory, modelformset_factory, inlineformset_factory
from django.forms.util import ErrorList

from timecard.models import User as ttUser
from erp.widgets import ImgClearableFileInput
from cv.models import CV, Skill
from models import Preset, PresetRequirement, Project, Customer, WorkGroup, Screenshot, ProjectRequirement


class CustomerMForm(ModelForm):

    class Meta:
        model = Customer

class PresetMForm(ModelForm):
    """
    Manage full preset record for view project page.
    """
    class Meta:
        model = Preset
        widgets = {
            'title': TextInput(attrs={'class': "span6"}),
            'challenge': Textarea(attrs={'cols':"100", 'rows':"5", 'class': "span6"}),
            'service': TextInput(attrs={'class': "span6"}),
            'industry': TextInput(attrs={'class': "span6"}),
            'solution': Textarea(attrs={'cols':"100", 'rows':"5", 'class': "span6"}),
        }


class PresetBrieflyMForm(ModelForm):
    """
    Manage project preset record for add/modify preset pages.
    """
    class Meta:
        model = Preset
        fields = ('id', )


class ProjectMForm(ModelForm):
    """
    Manage full project record for view project page.
    """
    class Meta:
        model = Project
        widgets = {
            'title': TextInput(attrs={'class': "span6"}),
            'challenge': Textarea(attrs={'cols':"100", 'rows':"5", 'class': "span6"}),
            'benefits': Textarea(attrs={'cols':"100", 'rows':"5", 'class': "span6"}),
            'feedback': Textarea(attrs={'cols':"100", 'rows':"5", 'class': "span6"}),
            'service': TextInput(attrs={'class': "span6"}),
            'industry': TextInput(attrs={'class': "span6"}),
            'solution': Textarea(attrs={'cols':"100", 'rows':"5", 'class': "span6"}),
        }


class ProjectBrieflyMForm(ModelForm):
    """
    Manage briefly project record for list of projects page.
    """
    class Meta:
        model = Project
        fields = ('id', 'pause')


class ProjectFilterMForm(ModelForm):
    """
    Manage project filter by project data.
    """
    title = CharField(label="Title", required=False, widget= TextInput(attrs={'class': "span6"}))
    class Meta:
        model = Project
        fields = ('title', 'service', 'industry', 'date_start', 'date_finish')
        widgets = {
            'service': TextInput(attrs={'class': "span6"}),
            'industry': TextInput(attrs={'class': "span6"}),
        }


class ProjectFilterReqMForm(ModelForm):
    """
    Manage project filter by project requirements data
    """
    query = CharField(label="Requirement Query", required=False, widget=TextInput(attrs={'class':"span6"}))
    class Meta:
        model = Skill
        fields = ('id',)


class ProjectSSMForm(ModelForm):
    """
    Manage the record of screenshot for current project.
    """
    class Meta:
        model = Screenshot
        widgets = {
            'image': ImgClearableFileInput(),
            'desc': Textarea(attrs={'cols': "100", 'rows': "3", 'class': "span6"}),}


class ProjectWGMForm(ModelForm):
    """
    Manage the record of Employee for current project.
    """
    class Meta:
        model = WorkGroup
        exclude = ('cv', )
        widgets = {
            'role': TextInput(attrs={'class': "span6"}),
            'desc': Textarea(attrs={'cols': "100", 'rows': "5", 'class': "span6"}),
            }

    def clean(self):
        cd = super(ProjectWGMForm, self).clean()
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


class ProjectAddReqMForm(ModelForm):
    """
    Attach/detach the record of Requirement for current project.
    """
    check = BooleanField(label="Check", required=False)
    class Meta:
        model = ProjectRequirement
        fields = ('id', )


class ProjectReqMForm(ModelForm):
    """
    Manage the resord of Requirement for current project.
    """
    class Meta:
        model = ProjectRequirement
        fields = ('id', 'desc')
        widgets = {
            'desc': Textarea(attrs={'cols':"100", 'rows':"5", 'class': "span6"})
        }

    def get_skill_name(self):
        return self.instance.skill.name


class PresetAddReqMForm(ModelForm):
    """
    Attach/detach the record of Requirement for current project.
    """
    check = BooleanField(label="Check", required=False)
    class Meta:
        model = PresetRequirement
        fields = ('id', )


class PresetReqMForm(ModelForm):
    """
    Manage the resord of Requirement for current project.
    """
    class Meta:
        model = PresetRequirement
        fields = ('id', 'desc')
        widgets = {
            'desc': Textarea(attrs={'cols':"100", 'rows':"5", 'class': "span6"})
        }

    def get_skill_name(self):
        return self.instance.skill.name


CustomerMFormset = modelformset_factory(Customer, CustomerMForm, extra=0, can_delete=True)

PresetBrieflyMFormset = modelformset_factory(Preset, PresetBrieflyMForm, extra=0, can_delete=True)
PresetReqIFormset = inlineformset_factory(Preset, PresetRequirement, PresetReqMForm, extra=0, can_delete=False, fk_name='preset')
PresetAddReqMFormset = modelformset_factory(Skill, PresetAddReqMForm, extra=0)

ProjectMFormset = modelformset_factory(Project, ProjectMForm, extra=0, can_delete=True)
ProjectBrieflyMFormset = modelformset_factory(Project, ProjectBrieflyMForm, extra=0, can_delete=True)
ProjectReqIFormset = inlineformset_factory(Project, ProjectRequirement, ProjectReqMForm, extra=0, can_delete=False, fk_name='project')
ProjectAddReqMFormset = modelformset_factory(Skill, ProjectAddReqMForm, extra=0)
ProjectSSIFormset = inlineformset_factory(Project, Screenshot, ProjectSSMForm, fk_name="project", extra=1, can_delete=True)
ProjectWGIFormset = inlineformset_factory(Project, WorkGroup, ProjectWGMForm, fk_name="project", extra=0, can_delete=True)

ProjectFilterReqsMFormset = modelformset_factory(Skill, ProjectFilterReqMForm, extra=0)