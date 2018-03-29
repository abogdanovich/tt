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

from cv.models import MANAGE_LEVEL, Skill, Position, CV
from cv.forms import SkillMFormset
from erp.utils import get_cv, check_login, check_permission

from projects.models import Preset, Project, ProjectRequirement, WorkGroup
from projects.forms import ProjectMForm, ProjectFilterMForm, ProjectFilterReqsMFormset, ProjectBrieflyMFormset, ProjectReqIFormset, ProjectSSIFormset, ProjectWGIFormset, ProjectAddReqMFormset
from projects.utils import ProjectRequirementDict

import logging

@check_login
def list_vf(request):
    """
    display list projects.
    view some projects data, mod pause state, delete projects.
    check & save data
    """
    cv = get_cv(request)

    if not check_permission(cv, perm_index=10): # view project data
        messages.error(request, "Access denied")
        return redirect("erp_home")
    return render_to_response(
        "projects/list.html",
        {
            'cv': cv,
            'nav': "project",
            'tab': request.REQUEST.get('tab', ''),
            'states': ['prepare', 'work', 'pause', 'finish'],
            'presets': Preset.objects.all(),
            'projects': Project.objects.select_related(depth=1).all().order_by('date_start'),
            },
        RequestContext(request))


@check_login
def manage_vf(request):
    """
    display list projects.
    view some projects data, mod pause state, delete projects.
    check & save data
    """
    def _get_projects():
        """
        build projects list sorted by state & start/finish date.
        state_projects = [
            {'state': "prepare", 'projects': Project.objects.filter(Q(date_start=None)|Q(date_start__gt=date.today()))},
            {'state': "develop", 'projects': Project.objects.filter(Q(date_start__lte=date.today()), Q(date_finish=None) | Q(date_finish__gt=date.today()), is_pause=False)},
            {'state': "pause", 'projects': Project.objects.filter(Q(date_start__lte=date.today()), Q(date_finish=None)|Q(date_finish__gt=date.today()), is_pause=True)},
            {'state': "finish", 'projects': Project.objects.filter(date_start__lte=date.today(), date_finish__lte=date.today())},
            #{'state': "all", 'projects': Project.objects.all()},
        ]
        """
        projects = [
            # ('develop', [prj for prj in Project.objects.all() if prj.is_develop()]),
            ('prepare', ProjectBrieflyMFormset(queryset=Project.objects.filter(Q(date_start=None)|Q(date_start__gt=date.today())), prefix="prepare")),
            ('develop', ProjectBrieflyMFormset(queryset=Project.objects.filter(Q(date_start__lte=date.today()), Q(date_finish=None) | Q(date_finish__gte=date.today())), prefix="develop")),
            #('pause', ProjectBrieflyMFormset(queryset=Project.objects.filter(Q(date_start__lte=date.today()), Q(date_finish=None)|Q(date_finish__gte=date.today()), pause=True), prefix="pause")),
            ('finish', ProjectBrieflyMFormset(queryset=Project.objects.filter(date_start__lte=date.today(), date_finish__lt=date.today()), prefix="finish"))]
        return projects
    # --- MAIN FUNCTION ---
    cv = get_cv(request)
    if not check_permission(cv, perm_index=10): # view project data
        messages.error(request, "Access denied")
        return redirect("erp_home")
    else:
        manage = False
        if check_permission(cv, perm_index=15): # edit project data
            manage = True
    projects = None
    stage = request.REQUEST.get('stage', 'input')
    if stage == 'confirm' and request.method == "POST":
        if manage:
            projects_del = request.session.get('projects_del', None)
            for prj in projects_del:
                prj.delete()
            del request.session['projects_del']
            messages.success(request, 'Selected projects has been deleted successfully.')
            stage = 'input'
        else:
            messages.error(request, "Access denied")
            return redirect("erp_home")
    if stage == 'validate' and request.method == "POST":
        if manage:
            prj_mforms = ProjectBrieflyMFormset(request.POST)
            if prj_mforms.is_valid():
                if prj_mforms.deleted_forms:
                    request.session['projects_del'] = [form.instance for form in prj_mforms.deleted_forms]
                    return render_to_response(
                        "projects/del_projects.html",
                        {
                            'cv': cv,
                            'nav': "project",
                            'projects_del': request.session['projects_del'],
                            },
                        RequestContext(request))
                prj_mforms.save()
                messages.success(request, 'Projects pause data has been updated successfully.')
            else: # errors in saving
                messages.error(request, 'Projects data didn`t update. There were some errors.')
        else:
            messages.error(request, "Access denied")
            return redirect("erp_home")
    # stage == input
    if stage == 'input':
        prj_mforms = ProjectBrieflyMFormset()
    return render_to_response(
        "projects/manage.html",
        {
            'cv': cv,
            'nav': "project",
            'tab': request.REQUEST.get('tab', ''),
            'prj_mforms': prj_mforms,
            },
        RequestContext(request))


@check_login
def filter_vf(request, op=''):
    """
    display list projects by defined filter.
    view some projects data, mod pause state, delete projects.
    check & save data
    """
    results_data = None
    results_data_flag = False
    results_presets = None
    results_presets_flag = False
    preset_value = None
    results_reqs = None
    results_reqs_flag = False
    if op == 'data' and request.method == "POST":
        results_data_flag = True
        project_data_form = ProjectFilterMForm(request.POST)
        if project_data_form.is_valid():
            cd = project_data_form.cleaned_data
            results_data = Project.objects.all()
            if cd.get('title'):
                results_data = results_data.filter(title__icontains=cd['title'])
            if cd.get('service'):
                results_data = results_data.filter(service__icontains=cd['service'])
            if cd.get('industry'):
                results_data = results_data.filter(industry__icontains=cd['industry'])
            if cd.get('date_start'):
                results_data = results_data.filter(date_start__gte=cd['date_start'])
            if cd.get('date_finish'):
                results_data = results_data.filter(date_finish__lte=cd['date_finish'])
    else:
        project_data_form = ProjectFilterMForm()
    if op == 'presets' and request.method == "POST":
        results_presets_flag = True
        if request.POST.get('preset'):
            preset_value = int(request.POST['preset'])
            if preset_value == 0:
                preset_value = None
            results_data = Project.objects.filter(preset=preset_value)
    presets = Preset.objects.all()
    if op == 'reqs' and request.method == "POST":
        results_reqs_flag = True
        project_reqs_forms = ProjectFilterReqsMFormset(request.POST)
        if project_reqs_forms.is_valid():
            results_data = tuple(rec for rec in Project.objects.all())
            for frm in project_reqs_forms:
                cd = frm.cleaned_data
                if cd.get('query'):
                    tags = tuple(map(unicode.strip, cd['query'].split(',')))
                    for tag in tags:
                        results_data = tuple(rec for rec in results_data if rec.has_req(cd['id']) and rec.requirements.get(skill=cd['id']).has_tag(tag))
    else:
        project_reqs_forms = ProjectFilterReqsMFormset()
    return render_to_response(
        "projects/filter.html",
        {
            'cv': get_cv(request),
            'nav': "project",
            'tab': request.REQUEST.get('tab', ''),
            'project_data_form': project_data_form,
            'presets': presets,
            'project_reqs_forms': project_reqs_forms,
            'results_data': results_data,
            'results_data_flag': results_data_flag,
            'results_presets_flag': results_presets_flag,
            'results_reqs_flag': results_reqs_flag,
            'presets_value': preset_value,
            },
        RequestContext(request))


@check_login
def view_vf(request, prj_id=None, output=''):
    """
    display a full info about current project.
    """
    if prj_id:
        try:
            project = Project.objects.get(id=int(prj_id))
        except Project.DoesNotExist, Project.MultipleObjectsReturned:
            messages.error(request, 'Project was not found.')
            return redirect("erp_projects")
        cv = get_cv(request)
        if not check_permission(cv, perm_index=10): # view project data
            messages.error(request, "Access denied")
            return redirect("erp_home")
        return render_to_response(
            "projects/view%s.html" % output,
            {
                'cv': cv,
                'nav': "project",
                'project': project,
                'reqs': project.requirements.all(),
                'sss': project.screenshots.all(),
                'wg': project.wg.all(),
                },
            RequestContext(request))
    else:
        messages.error(request, 'Bad request')
        return redirect("erp_home")


@check_login
def mod_vf(request, prj_id=None, pst_id=None, op=''):
    stage = request.REQUEST.get('stage', 'input')
    preset = None
    old_project = None
    cv = get_cv(request)
    # make copy of project
    if op == 'copy':
        if prj_id:
            try:
                old_project = Project.objects.get(id=int(prj_id))
            except Project.DoesNotExist:
                messages.error(request, "Project didn`t found. Try again.")
                redirect("erp_projects")
            if not check_permission(cv, perm_index=14): # make copy of project
                messages.error(request, "Access denied")
                return redirect("erp_home")
            if stage == 'validate':
                p_mform = ProjectMForm(request.POST)
                if p_mform.is_valid():
                    p_mform.save()
                    new_project = Project.objects.get(id=p_mform.instance.id)
                    messages.success(request, 'New Project data saved successfully.')
                    for req in old_project.requirements.all():
                        ProjectRequirement.objects.create(project=new_project, skill=req.skill, desc=req.desc)
                    messages.success(request, 'Also to new project were added all requirements from old project "%s"' % old_project)
                    for emp in old_project.wg.all():
                        WorkGroup.objects.create(project=new_project, cv=emp.cv, role=emp.role, desc=emp.desc, date_start=date.today())
                    messages.success(request, 'Also to new project were added all employees from old project "%s" work group.' % old_project)
                    return redirect("erp_project", prj_id=new_project.id)
                else:
                    messages.error(request, 'Project data didn`t save. You have some errors.')
            else: # stage == input
                init = {
                    'id': None,
                    'title': "",
                    'challenge': old_project.challenge,
                    'customer': None,
                    'benefits': old_project.benefits,
                    'feedback': old_project.feedback,
                    'service': old_project.service,
                    'industry': old_project.industry,
                    'solution': old_project.solution,
                    'dev_time': old_project.dev_time,
                    'date_start': date.today(),
                    'date_finish': None,
                    'preset': old_project.preset,
                }
                p_mform = ProjectMForm(initial=init)
        else:
            messages.error(request, "Bad request.")
            redirect("erp_home")
    # add project from preset
    elif op == 'preset':
        if pst_id:
            try:
                preset = Preset.objects.get(id=int(pst_id))
            except Preset.DoesNotExist:
                messages.error(request, "Project Preset didn`t found. Try again.")
                redirect("erp_project_presets")
            if not check_permission(cv, perm_index=26): # manage preset data
                messages.error(request, "Access denied")
                return redirect("erp_home")
            if stage == 'validate':
                p_mform = ProjectMForm(request.POST)
                p_mform.instance.preset = preset
                if p_mform.is_valid():
                    p_mform.save()
                    project = Project.objects.get(id=p_mform.instance.id)
                    for req in preset.requirements.all():
                        ProjectRequirement.objects.create(project=project, skill=req.skill, desc=req.desc)
                    messages.success(request, 'Projects data saved successfully.<br>Also to project were adding all requirements from preset "%s"' % preset)
                    return redirect("erp_project", prj_id=project.id)
                else:
                    messages.error(request, 'Project data didn`t save. You have some errors.')
            elif stage == 'input': # stage == input
                init = {
                    'preset': preset,
                    'challenge': preset.challenge,
                    'service': preset.service,
                    'industry': preset.industry,
                    'solution': preset.solution
                }
                p_mform = ProjectMForm(initial=init)
        else:
            messages.error(request, "Bad request.")
            redirect("erp_home")
    # add empty project
    elif op == 'add':
        if not check_permission(cv, perm_index=12): # create new empty project
            messages.error(request, "Access denied")
            return redirect("erp_home")
        if stage == 'validate':
            p_mform = ProjectMForm(request.POST)
            if p_mform.is_valid():
                p_mform.save()
                messages.success(request, 'Projects data saved successfully.')
                return redirect("erp_project", prj_id=p_mform.instance.id)
            else:
                messages.error(request, 'Project data didn`t save. You have some errors.')
        else:
            p_mform = ProjectMForm()
    elif op == 'mod': # op == 'mod' or 'del'
        if prj_id:
            try:
                project = Project.objects.get(id=int(prj_id))
            except Project.DoesNotExist, Project.MultipleObjectsReturned:
                messages.error(request, 'Project was not found.')
                return redirect("erp_projects")
            if not check_permission(cv, perm_index=15): # edit project data
                messages.error(request, "Access denied")
                return redirect("erp_home")
            if stage == 'validate':
                p_mform = ProjectMForm(request.POST, instance=project)
                if p_mform.is_valid():
                    p_mform.save()
                    messages.success(request, 'Project data saved successfully.')
                    return redirect("erp_project", project.id)
                else:
                    messages.error(request, 'Project data didn`t save. You have some errors.')
            else:
                p_mform = ProjectMForm(instance=project)
        else:
            messages.error(request, 'Bad request')
            return redirect("erp_home")
    return render_to_response(
        "projects/mod.html",
        {
            'cv': cv,
            'nav': "project",
            'op': op,
            'p_mform': p_mform,
            'preset': preset,
            'old_project': old_project},
        RequestContext(request))


@check_login
def mod_req_vf(request, prj_id=None):
    cv = get_cv(request)
    if not check_permission(cv, perm_index=16): # manage project requirements
        messages.error(request, "Access denied")
        return redirect("erp_home")
    stage = request.REQUEST.get('stage', None)
    if prj_id:
        try:
            project = Project.objects.get(id=int(prj_id))
        except Project.DoesNotExist, Project.MultipleObjectsReturned:
            messages.error(request, 'Project was not found.')
            return redirect("erp_projects")
        if stage == 'validate':
            prj_req_iforms = ProjectReqIFormset(request.POST, instance=project)
            if prj_req_iforms.is_valid():
                prj_req_iforms.save()
                messages.success(request, 'Project Requirements data saved successfully.')
                return redirect("erp_project", project.id)
            else:
                messages.error(request, 'Project Requirements data didn`t save. You have some errors.')
        # stage == input
        else:
            prj_req_iforms = ProjectReqIFormset(instance=project)
        return render_to_response(
            "projects/mod_req.html",
            {
                'cv': cv,
                'nav': "project",
                'prj_req_iforms': prj_req_iforms,
                },
            RequestContext(request))
    else:
        messages.error(request, 'Bad request')
        return redirect("erp_home")


@check_login
def add_req_vf(request, prj_id=None):
    cv = get_cv(request)
    if not check_permission(cv, perm_index=16): # manage project requirements
        messages.error(request, "Access denied")
        return redirect("erp_home")
    stage = request.REQUEST.get('stage', None)
    if prj_id:
        try:
            project = Project.objects.get(id=int(prj_id))
        except Project.DoesNotExist, Project.MultipleObjectsReturned:
            messages.error(request, 'Project was not found.')
            return redirect("erp_projects")
        prj_reqs = [x.skill for x in project.requirements.all()]
        if stage == 'validate':
            prj_req_mforms = ProjectAddReqMFormset(request.POST)
            if prj_req_mforms.is_valid():
                is_add = is_del = False
                for req in prj_req_mforms:
                    cd = req.cleaned_data
                    if cd['check']:
                        if cd['id'] not in prj_reqs:
                            ProjectRequirement.objects.create(project=project, skill=cd['id'])
                            is_add = True
                    else:
                        if cd['id'] in prj_reqs:
                            try:
                                ProjectRequirement.objects.get(project=project, skill=cd['id']).delete()
                                is_del = True
                            except ProjectRequirement.DoesNotExist:
                                pass
                if is_add:
                    messages.success(request, 'The Project Requirements has been added successfully.')
                if is_del:
                    messages.success(request, 'The some Projects Requirements has been deleted successfully.')
                return redirect("erp_project", prj_id=project.id)
        # stage == input
        reqs = []
        for req in Skill.objects.all():
            if req in prj_reqs:
                reqs.append({'check': True})
            else:
                reqs.append({'check': False})
        prj_req_mforms = ProjectAddReqMFormset(initial=reqs)
        return render_to_response(
            "projects/add_req.html",
            {
                'cv': cv,
                'nav': "project",
                'project': project,
                'prj_req_mforms': prj_req_mforms,
                },
            RequestContext(request))
    else:
        messages.error(request, 'Bad request')
        return redirect("erp_home")


@check_login
def mod_ss_vf(request, prj_id=None):
    cv = get_cv(request)
    if not check_permission(cv, perm_index=17): # manage project screenshots
        messages.error(request, "Access denied")
        return redirect("erp_home")
    stage = request.REQUEST.get('stage', None)
    if prj_id:
        try:
            project = Project.objects.get(id=int(prj_id))
        except Project.DoesNotExist, Project.MultipleObjectsReturned:
            messages.error(request, 'Project was not found.')
            return redirect("erp_projects")
        if stage == 'validate':
            pss_iforms = ProjectSSIFormset(request.POST, request.FILES, instance=project)
            if pss_iforms.is_valid():
                pss_iforms.save()
                messages.success(request, 'Project Screenshot data saved successfully.')
            else:
                messages.error(request, 'Project Screenshot data didn`t save. You have some errors.')
        # stage == input
        pss_iforms = ProjectSSIFormset(instance=project)
        return render_to_response(
            "projects/mod_ss.html",
            {
                'cv': cv,
                'nav': "project",
                'pss_iforms': pss_iforms,},
            RequestContext(request))
    else:
        messages.error(request, 'Bad request')
        return redirect("erp_home")


@check_login
def mod_wg_vf(request, prj_id=None):
    cv = get_cv(request)
    if not check_permission(cv, perm_index=19): # edit employee role
        messages.error(request, "Access denied")
        return redirect("erp_home")
    stage = request.REQUEST.get('stage', 'input')
    if prj_id:
        try:
            project = Project.objects.get(id=int(prj_id))
        except Project.DoesNotExist, Project.MultipleObjectsReturned:
            messages.error(request, 'Project was not found.')
            return redirect("erp_projects")
        if stage == 'add' and request.method=="POST":
            if not check_permission(cv, perm_index=18): # add/delete employee role
                messages.error(request, "Access denied")
                return redirect("erp_home")
            for key, val in request.POST.items():
                if val=='on':
                    try:
                        emp = CV.objects.get(id=int(key))
                        try:
                            WorkGroup.objects.get(cv=emp, project=project)
                            messages.error(request, "Employee has been already added to this Project Work Group.")
                        except WorkGroup.DoesNotExist:
                            if project.date_start:
                                ds = project.date_start
                            else:
                                ds = date.today()
                            WorkGroup.objects.create(cv=emp, project=project, role="...", date_start=ds)
                            messages.success(request, "Employee %s has been added successfully.<br>Please, edit 'role' & 'Start Date' fields." % cv)
                    except CV.DoesNotExist:
                        messages.error(request, "Employee CV didn`t found.")
            stage = 'input'
        if stage == 'confirm' and request.method == "POST":
            if not check_permission(cv, perm_index=18): # add/delete employee role
                messages.error(request, "Access denied")
                return redirect("erp_home")
            employees_del = request.session.get('employees_del', None)
            for emp in employees_del:
                emp.delete()
            del request.session['employees_del']
            messages.success(request, 'Selected Employees has been deleted successfully from Project Work Group.')
            stage = 'input'
        if stage == 'validate' and request.method=="POST":
            pwg_iforms = ProjectWGIFormset(request.POST, instance=project)
            if pwg_iforms.is_valid():
                if pwg_iforms.deleted_forms:
                    request.session['employees_del'] = [frm.instance for frm in pwg_iforms.deleted_forms]
                    return render_to_response(
                        "projects/del_employees.html",
                        {
                            'cv': cv,
                            'nav': "project",
                            'project': project,
                            'employees_del': request.session['employees_del'],},
                        RequestContext(request))
                pwg_iforms.save()
                messages.success(request, 'Project Work Group data saved successfully.')
            else:
                messages.error(request, 'Project Work Group data didn`t save. You have some errors.')
        # stage == input
        if stage == 'input':
            pwg_iforms = ProjectWGIFormset(instance=project)
            req_tags = project.get_tags()
            req_tags_nums = ProjectRequirementDict(req_tags)
        if check_permission(cv, perm_index=18): # add/delete employee role
            wg_emps = project.get_cvs()
            employees = []
            for pos in Position.projects.all():
                emps = pos.get_cvs()
                emps_finish = ()
                for emp in emps:
                    needed = emp.get_needed_tags(req_tags)
                    if needed:
                        req_tags_nums.add_cv_skills(needed)
                        if emp not in wg_emps:
                            emps_finish = emps_finish + ((emp, needed), )
                if emps_finish:
                    employees.append((pos, emps_finish))
        else:
            employees = None
        return render_to_response(
            "projects/mod_wg.html",
            {
                'cv': cv,
                'nav': "project",
                'project': project,
                'pwg_iforms': pwg_iforms,
                'req_tags_nums': req_tags_nums.source,
                'employees': employees,},
            RequestContext(request))
    else:
        messages.error(request, 'Bad request')
        return redirect("erp_home")