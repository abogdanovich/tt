# -*- coding: utf-8 -*-
__author__ = 'ABKorotky'
__email__ = ['akorotky@minsk.ximxim.com', 'aleksandr.korotky@ximad.com']


from datetime import date

from django.conf import settings
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.forms.util import ErrorList

from erp.utils import get_cv, check_login, check_permission
from cv.models import Skill

from projects.models import Preset, PresetRequirement, Project
from projects.forms import PresetMForm, PresetBrieflyMFormset, PresetReqIFormset, PresetAddReqMFormset

import logging


@check_login
def list_vf(request):
    """
    display the list of project presets forms.
    This page allow delete selected presets.
    Also it keep links to "Add preset", "Create page from preset" & "View preset data".
    """
    cv = get_cv(request)




    if not check_permission(cv, perm_index=25): # view preset data
        messages.error(request, "Access denied")
        return redirect("erp_home")
    else:
        manage = False
        if check_permission(cv, perm_index=26): # manage preset data
            manage = True
    stage = request.REQUEST.get('stage', 'input')
    if stage == 'confirm' and request.method == "POST":
        if manage:
            presets_del = request.session.get('presets_del', None)
            for pst in presets_del:
                for prj in Project.objects.filter(preset=pst):
                    prj.preset = None
                pst.delete()
            del request.session['presets_del']
            messages.success(request, 'Selected project presets has been deleted successfully.')
        else:
            messages.error(request, "Access denied")
            return redirect("erp_home")
    if stage == 'validate' and request.method == "POST":
        if manage:
            preset_mforms = PresetBrieflyMFormset(request.POST)
            if preset_mforms.is_valid():
                if preset_mforms.deleted_forms:
                    request.session['presets_del'] = [form.instance for form in preset_mforms.deleted_forms]
                    return render_to_response(
                        "projects/presets/del.html",
                        {
                            'cv': get_cv(request),
                            'nav': "project",
                            'presets_del': request.session['presets_del'],
                            },
                        RequestContext(request))
        else:
            messages.error(request, "Access denied")
            return redirect("erp_home")
    # stage == input
    preset_mforms = PresetBrieflyMFormset()
    return render_to_response(
        "projects/presets/list.html",
        {
            'cv': cv,
            'nav': "project",
            'preset_mforms': preset_mforms,},
        RequestContext(request))


@check_login
def view_vf(request, pst_id=None, output=''):
    """
    display the full preset data.
    output to screen & printer.
    Also this page keep links to edit preset data, Add/Del & Edit Technical requirements.
    """
    cv = get_cv(request)
    if not check_permission(cv, perm_index=25): # view preset data
        messages.error(request, "Access denied")
        return redirect("erp_home")
    if pst_id:
        try:
            preset = Preset.objects.get(id=int(pst_id))
        except Preset.DoesNotExist, Preset.MultipleObjectsReturned:
            messages.error(request, 'Project Preset was not found.')
            return redirect("erp_project_presets")
        reqs = preset.requirements.all()
        return render_to_response(
            "projects/presets/view%s.html" % output,
            {
                'cv': cv,
                'nav': "project",
                'preset': preset,
                'reqs': reqs,
                },
            RequestContext(request))
    else:
        messages.error(request, 'Bad request')
        return redirect("erp_home")


@check_login
def mod_vf(request, pst_id=None, prj_id=None, op=''):
    """
    display the form for modify preset data & manage theirs.
    """
    cv = get_cv(request)
    if not check_permission(cv, perm_index=25): # view preset data
        messages.error(request, "Access denied")
        return redirect("erp_home")
    project = None
    stage = request.REQUEST.get('stage', 'input')
    if op == 'add':
        if stage == 'validate':
            p_mform = PresetMForm(request.POST)
            if p_mform.is_valid():
                p_mform.save()
                messages.success(request, 'Project Preset data saved successfully.')
                return redirect("erp_project_presets")
            messages.error(request, 'Project Preset data didn`t save. You have some errors.')
        else:
            p_mform = PresetMForm()
    elif op == 'project':
        if prj_id:
            try:
                project = Project.objects.get(id=int(prj_id))
            except Project.DoesNotExist:
                messages.error(request, "Project didn`t found.")
                redirect("erp_projects")
            if stage == 'validate':
                p_mform = PresetMForm(request.POST)
                if p_mform.is_valid():
                    p_mform.save()
                    preset = Preset.objects.get(id=p_mform.instance.id)
                    for req in project.requirements.all():
                        PresetRequirement.objects.create(preset=preset, skill=req.skill, desc=req.desc)
                        messages.success(request, 'Project Preset data saved successfully.<br>Also to preset were adding all requirements from project "%s"' % project)
                        return redirect("erp_project_preset", pst_id=preset.id)
                messages.error(request, 'Project Preset data didn`t save. You have some errors.')
            else:
                p_mform = PresetMForm(initial={
                    'challenge': project.challenge,
                    'service': project.service,
                    'industry': project.industry,
                    'solution': project.solution,
                })
        else:
            messages.error(request, "Bad request")
            redirect('erp_home')
    else: # op == 'mod' or 'del'
        if pst_id:
            try:
                preset = Preset.objects.get(id=int(pst_id))
            except Preset.DoesNotExist, Preset.MultipleObjectsReturned:
                messages.error(request, 'Project Preset was not found.')
                return redirect("erp_projects_presets")
            if stage == 'validate':
                if not check_permission(cv, perm_index=26): # manage preset data
                    messages.error(request, "Access denied")
                    return redirect("erp_home")
                p_mform = PresetMForm(request.POST, instance=preset)
                if p_mform.is_valid():
                    p_mform.save()
                    messages.success(request, 'Project Preset data saved successfully.')
                    return redirect("erp_project_presets")
                messages.error(request, 'Project Preset data didn`t save. You have some errors.')
            else:
                p_mform = PresetMForm(instance=preset)
        else:
            messages.error(request, 'Bad request')
            return redirect("erp_home")
    return render_to_response(
        "projects/presets/mod.html",
        {
            'cv': cv,
            'nav': "project",
            'p_mform': p_mform,
            'op': op,
            'project': project,
            },
        RequestContext(request))


@check_login
def add_req_vf(request, pst_id=None):
    """
    display the formset with all Requirements for adding some of theirs to current preset.
    Also allow remove unchecked requirement from current preset.
    """
    cv = get_cv(request)
    if not check_permission(cv, perm_index=26): # manage preset data
        messages.error(request, "Access denied")
        return redirect("erp_home")
    stage = request.REQUEST.get('stage', None)
    if pst_id:
        try:
            preset = Preset.objects.get(id=int(pst_id))
        except Project.DoesNotExist, Project.MultipleObjectsReturned:
            messages.error(request, 'Project Preset was not found.')
            return redirect("erp_project_presets")
        pst_reqs = [x.skill for x in preset.requirements.all()]
        if stage == 'validate':
            pst_req_mforms = PresetAddReqMFormset(request.POST)
            if pst_req_mforms.is_valid():
                is_add = is_del = False
                for req in pst_req_mforms:
                    cd = req.cleaned_data
                    if cd['check']:
                        if cd['id'] not in pst_reqs:
                            PresetRequirement.objects.create(preset=preset, skill=cd['id'])
                            is_add = True
                    else:
                        if cd['id'] in pst_reqs:
                            try:
                                PresetRequirement.objects.get(preset=preset, skill=cd['id']).delete()
                                is_del = True
                            except PresetRequirement.DoesNotExist:
                                pass
                if is_add:
                    messages.success(request, 'The Project Requirements has been added successfully.')
                if is_del:
                    messages.success(request, 'The some Projects Requirements has been deleted successfully.')
                return redirect("erp_project_preset", pst_id=preset.id)
        # stage == input
        reqs = []
        for req in Skill.objects.all():
            if req in pst_reqs:
                reqs.append({'check': True})
            else:
                reqs.append({'check': False})
        pst_req_mforms = PresetAddReqMFormset(initial=reqs)
        return render_to_response(
            "projects/presets/add_req.html",
            {
                'cv': cv,
                'nav': "project",
                'preset': preset,
                'pst_req_mforms': pst_req_mforms,
                },
            RequestContext(request))
    else:
        messages.error(request, 'Bad request')
        return redirect("erp_home")


@check_login
def mod_req_vf(request, pst_id=None):
    """
    Display formset with selected requirements for edit theirs description.
    """
    cv = get_cv(request)
    if not check_permission(cv, perm_index=26): # manage preset data
        messages.error(request, "Access denied")
        return redirect("erp_home")
    stage = request.REQUEST.get('stage', None)
    if pst_id:
        try:
            preset = Preset.objects.get(id=int(pst_id))
        except Project.DoesNotExist, Project.MultipleObjectsReturned:
            messages.error(request, 'Project Preset was not found.')
            return redirect("erp_project_presets")
        if stage == 'validate':
            pst_req_iforms = PresetReqIFormset(request.POST, instance=preset)
            if pst_req_iforms.is_valid():
                pst_req_iforms.save()
                messages.success(request, 'Project Preset Requirements data saved successfully.')
                return redirect("erp_project_preset", preset.id)
            else:
                messages.error(request, 'Project Preset Requirements data didn`t save. You have some errors.')
        # stage == input
        else:
            pst_req_iforms = PresetReqIFormset(instance=preset)
        return render_to_response(
            "projects/presets/mod_req.html",
            {
                'cv': cv,
                'nav': "project",
                'pst_req_iforms': pst_req_iforms,
                },
            RequestContext(request))
    else:
        messages.error(request, 'Bad request')
        return redirect("erp_home")