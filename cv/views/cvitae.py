# -*- coding: utf-8 -*-
__author__ = 'ABKorotky'
__email__ = ['akorotky@minsk.ximxim.com', 'aleksandr.korotky@ximad.com']


from django.conf import settings
from django.contrib import messages
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from timecard.models import Offices as ttOffices
from erp.utils import get_cv, check_login, check_permission

from cv.models import *
from cv.forms import *

import logging

@check_login
def list_vf(request, fltr=""):

    """
    display list of CVs (all CVs).
    support filter by active/fired; by offices; by position.
    """
    def build_cvs(req):
        cvs = {}
        for cv in req:
            if cv.id not in cvs:
                cvs[cv.id] = cv
        cvs = cvs.values()
    # ----- MAIN -----
    cv = get_cv(request)
    if not check_permission(cv, perm_index=40): # view CV data
        messages.error(request, "Access denied")
        return redirect("erp_home")
    if fltr == 'full':
        cvs = CV.actives.fulls().select_related('position').order_by('name', 'surname')
        filter_msg = "Filled in completely CVs"
    elif fltr == 'position':
        cvs = CV.actives.empty_positions().select_related('position').order_by('name', 'surname')
        filter_msg = "Empty Position section"
    elif fltr == 'fls':
        cvs = CV.actives.empty_fls().select_related('position').order_by('name', 'surname')
        filter_msg = "Empty Foreign Languages section"
    elif fltr == 'skills':
        cvs = CV.actives.empty_skills().select_related('position').order_by('name', 'surname')
        filter_msg = "Empty Technical Expertise Skills section"
    elif fltr == 'projects':
        cvs = CV.actives.empty_projects().select_related('position').order_by('name', 'surname')
        filter_msg = "Empty Projects section"
    elif fltr == 'idle':
        emps_req = [ emp.cv \
                     for emp in WorkGroup.objects.select_related('project', 'cv', 'cv__position').filter(cv__fired=False).order_by('cv__name', 'cv__surname') \
                     if emp.project.is_develop()
        ]
        cvs = {}
        for cv in CV.actives.select_related('position').all():
            cvs[cv.id] = cv
        for cv in emps_req:
            if cv.id in cvs:
                del cvs[cv.id]
        cvs = cvs.values()
        filter_msg = "Employees without projects in develop state"
    elif fltr == 'prepare':
        emps_req = [ emp.cv \
                     for emp in WorkGroup.objects.select_related('project', 'cv', 'cv__position').filter(cv__fired=False).order_by('cv__name', 'cv__surname') \
                     if emp.project.is_prepare()
        ]
        cvs = build_cvs(emps_req)
        filter_msg = "Employees with projects in prepare state"
    elif fltr == 'develop':
        emps_req = [ emp.cv \
                     for emp in WorkGroup.objects.select_related('project', 'cv', 'cv__position').filter(cv__fired=False).order_by('cv__name', 'cv__surname') \
                     if emp.project.is_develop()
        ]
        cvs = build_cvs(emps_req)
        filter_msg = "Employees with projects in develop state"
    elif fltr == 'work':
        emps_req = [ emp.cv \
                     for emp in WorkGroup.objects.select_related('project', 'cv', 'cv__position').filter(cv__fired=False).order_by('cv__name', 'cv__surname') \
                     if emp.project.is_work()
        ]
        cvs = build_cvs(emps_req)
        filter_msg = "Employees with projects in work state"
    elif fltr == 'pause':
        emps_req = [ emp.cv \
                     for emp in WorkGroup.objects.select_related('project', 'cv', 'cv__position').filter(cv__fired=False).order_by('cv__name', 'cv__surname') \
                     if emp.project.is_pause()
        ]
        cvs = build_cvs(emps_req)
        filter_msg = "Employees with projects in pause state"
    elif fltr == 'finish':
        emps_req = [ emp.cv \
                     for emp in WorkGroup.objects.select_related('project', 'cv', 'cv__position').filter(cv__fired=False).order_by('cv__name', 'cv__surname') \
                     if emp.project.is_finish()
        ]
        cvs = build_cvs(emps_req)
        filter_msg = "Employees with projects in finish state"
    else:
        cvs = CV.actives.select_related('position').order_by('name', 'surname')
        filter_msg = "All CVs"
    return render_to_response(
        "cv/list.html",
        {
            'cv': cv,
            'nav': "cv",
            'cvs': cvs,
            'filter_msg': filter_msg,
            'offices': ttOffices.objects.all(),
            'positions': Position.objects.all()},
        RequestContext(request))


@check_login
def view_cv_vf(request, cv_id=None, output=""):
    """
    view CV full data:
    - personal data (if is the user in the tt-system then wiew tt-data)
    - contact data
    - foreign languages (fl) skills.
    - technical expertise (te) skills.
    - projects data.
    """
    if cv_id:
        try:
            view_cv = CV.objects.get(id=int(cv_id))
            cv = get_cv(request)
            if view_cv != cv:
                if not check_permission(cv, perm_index=40): # view CV data
                    messages.error(request, "Access denied")
                    return redirect("erp_home")
            return render_to_response(
                "cv/view_cv%s.html" % output,
                {
                    'cv': cv,
                    'nav': "cv",
                    'view_cv': view_cv,
                    'fls': view_cv.fl.all(),
                    'skills': view_cv.skills.all(),
                    'certificates': view_cv.certificates.all(),
                    'wgs': view_cv.wg.all(),
                    'prev_projects': view_cv.prev_projects.all(),},
                RequestContext(request))
        except CV.DoesNotExist:
            return None
    else:
        messages.warning(request, 'The CV didn`t found.')
        return redirect("erp_home")


@check_login
def mod_cv_personal_vf(request, cv_id=None):
    """
    display modify personal form.
    check data & save.
    """
    if cv_id:
        try:
            view_cv = CV.objects.get(id=int(cv_id))
            cv = get_cv(request)
            if view_cv != cv:
                if not check_permission(cv, perm_index=41): # edit CV personal data
                    messages.error(request, "Access denied")
                    return redirect("erp_home")
            stage = request.REQUEST.get('stage', None)
            if stage == 'validate':
                cv_mform = CVPersonalMForm(request.POST, instance=view_cv)
                if cv_mform.is_valid():
                    cv_mform.save()
                    messages.success(request, 'The Personal data updated.')
                    return redirect("erp_cv", cv_id=view_cv.id)
                else: # errors in save
                    messages.error(request, 'The Personal data didn`t update. There were some problems.')
            else: # stage == input
                cv_mform = CVPersonalMForm(instance=view_cv)
            return render_to_response(
                "cv/mod_personal.html",
                {
                    'cv': cv,
                    'nav': "cv",
                    'cv_mform': cv_mform},
                RequestContext(request))
        except CV.DoesNotExist:
            return None
    else: # cv is bad or missing
        messages.warning(request, 'The CV didn`t found.')
        return redirect("erp_home")


@check_login
def mod_cv_contacts_vf(request, cv_id=None):
    """
    display add/modify/delete fl skills form.
    check data & save.
    """
    if cv_id:
        try:
            view_cv = CV.objects.get(id=int(cv_id))
            cv = get_cv(request)
            if view_cv != cv:
                if not check_permission(cv, perm_index=41): # edit CV personal data
                    messages.error(request, "Access denied")
                    return redirect("erp_home")
            stage = request.REQUEST.get('stage', 'input')
            if stage == 'validate':
                cvcontact_iforms = CVContactIFormset(request.POST, instance=view_cv)
                if cvcontact_iforms.is_valid():
                    cvcontact_iforms.save()
                    messages.success(request, 'The Contact Info updated.')
                    stage = 'input'
                else: # errors in save
                    messages.error(request, 'The Contact Info didn`t update. There were some problems.')
            # stage == input
            if stage == 'input':
                cvcontact_iforms = CVContactIFormset(instance=view_cv)
            return render_to_response(
                "cv/mod_contacts.html",
                {
                    'cv': cv,
                    'nav': "cv",
                    'cv_contact_iforms': cvcontact_iforms},
                RequestContext(request))
        except CV.DoesNotExist:
            messages.error(request, "Bad request")
            return redirect("erp_home")
    else: # cv is bad or missing
        messages.warning(request, 'The CV didn`t found.')
        return redirect("erp_home")


@check_login
def mod_cv_fl_vf(request, cv_id=None):
    """
    display add/modify/delete fl skills form.
    check data & save.
    """
    if cv_id:
        try:
            view_cv = CV.objects.get(id=int(cv_id))
            cv = get_cv(request)
            if view_cv != cv:
                if not check_permission(cv, perm_index=42): # manage CV FL data
                    messages.error(request, "Access denied")
                    return redirect("erp_home")
            stage = request.REQUEST.get('stage', None)
            if stage == 'validate':
                cvfl_iforms = CVFL_IFormset(request.POST, instance=view_cv)
                if cvfl_iforms.is_valid():
                    cvfl_iforms.save()
                    messages.success(request, 'The Foreign Languages skills updated.')
                else: # errors in save
                    messages.error(request, 'The Foreign Languages skills didn`t update. There were some problems.')
            # stage == input
            cvfl_iforms = CVFL_IFormset(instance=view_cv)
            return render_to_response(
                "cv/mod_fl.html",
                {
                    'cv': cv,
                    'nav': "cv",
                    'cvfl_iforms': cvfl_iforms},
                RequestContext(request))
        except CV.DoesNotExist:
            messages.error(request, "Bad request")
            return redirect("erp_home")
    else: # cv is bad or missing
        messages.warning(request, 'The CV didn`t found.')
        return redirect("erp_home")


@check_login
def mod_cv_skills_vf(request, cv_id=None):
    """
    display modify te skills description form.
    check data & save.
    """
    if cv_id:
        try:
            view_cv = CV.objects.get(id=int(cv_id))
            cv = get_cv(request)
            if view_cv != cv:
                if not check_permission(cv, perm_index=43): # manage CV skills data
                    messages.error(request, "Access denied")
                    return redirect("erp_home")
            stage = request.REQUEST.get('stage', None)
            if stage == 'validate':
                cv_skill_iforms = CVSkill_IFormset(request.POST, instance=view_cv)
                if cv_skill_iforms.is_valid():
                    cv_skill_iforms.save()
                    messages.success(request, 'The Technical Expertise data updated.')
                else: # errors in save
                    messages.error(request, 'The Technical Expertise data didn`t update. There were some problems.')
            else: # stage == input
                cv_skill_iforms = CVSkill_IFormset(instance=view_cv)
            return render_to_response(
                "cv/mod_skills.html",
                {
                    'cv': cv,
                    'nav': "cv",
                    'cv_skill_iforms': cv_skill_iforms},
                RequestContext(request))
        except CV.DoesNotExist:
            return None
    else: # cv is bad or missing
        messages.warning(request, 'The CV didn`t found.')
        return redirect("erp_home")


@check_login
def add_cv_skills_vf(request, cv_id=None):
    """
    display add/delete te skills form.
    check data & save.
    """
    if cv_id:
        try:
            view_cv = CV.objects.get(id=int(cv_id))
            cv = get_cv(request)
            if view_cv != cv:
                if not check_permission(cv, perm_index=43): # manage CV skills data
                    messages.error(request, "Access denied")
                    return redirect("erp_home")
            cv_skills = [x.skill for x in view_cv.skills.all()]
            stage = request.REQUEST.get('stage', None)
            if stage == 'validate':
                cv_skill_mforms = CVAddSkill_MFormset(request.POST)
                if cv_skill_mforms.is_valid():
                    is_add = is_del = False
                    for skill in cv_skill_mforms:
                        cd = skill.cleaned_data
                        if cd['check']:
                            if cd['id'] not in cv_skills:
                                CVSkill.objects.create(cv=view_cv, skill=cd['id'])
                                is_add = True
                        else:
                            if cd['id'] in cv_skills:
                                try:
                                    CVSkill.objects.get(cv=view_cv, skill=cd['id']).delete()
                                    is_del = True
                                except CVSkill.DoesNotExist:
                                    pass
                    if is_add:
                        messages.success(request, 'The Technical Expertise Skills has been added successfully.')
                    if is_del:
                        messages.success(request, 'The some Technical Expertise Skills has been deleted successfully.')
                    return redirect("erp_cv", cv_id=cv.id)
                else: # errors in save
                    messages.error(request, 'The Technical Expertise data didn`t update. There were some problems.')
            else: # stage == input
                skills = []
                for skill in Skill.objects.all():
                    if skill in cv_skills:
                        skills.append({'check': True})
                    else:
                        skills.append({'check': False})
                cv_skill_mforms = CVAddSkill_MFormset(initial=skills)
            return render_to_response(
                "cv/add_skills.html",
                {
                    'cv': cv,
                    'nav': "cv",
                    'view_cv': view_cv,
                    'cv_skill_mforms': cv_skill_mforms},
                RequestContext(request))
        except CV.DoesNotExist:
            return None
    else: # cv is bad or missing
        messages.warning(request, 'The CV didn`t found.')
        return redirect("erp_home")


@check_login
def mod_cv_projects_vf(request, cv_id=None):
    """
    display modify project data form.
    check data & save.
    """
    if cv_id:
        try:
            view_cv = CV.objects.get(id=int(cv_id))
            cv = get_cv(request)
            if view_cv != cv:
                if not check_permission(cv, perm_index=45): # edit CV projects data
                    messages.error(request, "Access denied")
                    return redirect("erp_home")
            stage = request.REQUEST.get('stage', None)
            if stage == 'validate':
                cv_prj_iforms = CVProject_IFormset(request.POST, instance=view_cv)
                if cv_prj_iforms.is_valid():
                    cv_prj_iforms.save()
                    messages.success(request, 'The Project data updated.')
                    return redirect("erp_cv", cv_id=view_cv.id)
                else: # errors in save
                    messages.error(request, 'The Project data didn`t update. There were some problems.')
            else: # stage == input
                cv_prj_iforms = CVProject_IFormset(instance=view_cv)
            return render_to_response(
                "cv/mod_projects.html",
                {
                    'cv': cv,
                    'nav': "cv",
                    'cv_prj_iforms': cv_prj_iforms},
                RequestContext(request))
        except CV.DoesNotExist:
            return None
    else: # cv is bad or missing
        messages.warning(request, 'The CV didn`t found.')
        return redirect("erp_home")


@check_login
def manage_vf(request):
    """
    display list of CV`s, sorted by offices & name/surname.
    for HRM employees only!!!
    view CV, add a new CV template & delete old CV.
    Also modify login, check/uncheck fired flag, select accessLevel.
    """
    cv = get_cv(request)
    if not check_permission(cv, perm_index=40): # view CV data
        messages.error(request, "Access denied")
        return redirect("erp_home")
    else:
        manage = False
        if check_permission(cv, perm_index=48): # manage CV service data
            manage = True
    stage = request.REQUEST.get('stage', 'input')
    if stage == 'confirm' and request.method == "POST":
        if manage:
            cvs_del = request.session.get('cvs_del', None)
            for cv in cvs_del:
                if request.session.get('cv_id', None) == cv.id:
                    messages.warning(request, 'You deleted also yours CV record. Now oyu don`t have possibility to work in ERP System.')
                    del request.session['cv_id']
                    if request.session.get('uid', None):
                        del request.session['uid']
                cv.delete()
            del request.session['cvs_del']
            messages.success(request, 'Selected CVs has been deleted successfully.')
            if not request.session.get('cv_id', None):
                return redirect("erp_logout")
            stage = 'input'
        else:
            messages.error(request, "Access denied")
            return redirect("erp_home")
    if stage == 'validate' and request.method == "POST":
        if manage:
            cv_mforms = CVManageMFormset(request.POST)
            if cv_mforms.is_valid():
                if cv_mforms.deleted_forms:
                    request.session['cvs_del'] = [form.instance for form in cv_mforms.deleted_forms]
                    return render_to_response(
                        "cv/del_cvs.html",
                        {
                            'cv': get_cv(request),
                            'nav': "cv",
                            'cvs_del': request.session['cvs_del'],
                            },
                        RequestContext(request))
                cv_mforms.save()
                messages.success(request, 'CV settings has been save succesfully.')
            else: # form is not valid
                messages.error(request, 'CV settings didn`t update. There were some errors.')
        else:
            messages.error(request, "Access denied")
            return redirect("erp_home")
    # stage == input
    if stage == 'input':
        cv_mforms = CVManageMFormset(queryset=CV.objects.order_by('name', 'surname'))
    return render_to_response(
        "cv/manage.html",
        {
            'cv': cv,
            'nav': "cv",
            'cv_mforms': cv_mforms,
            'offices': ttOffices.objects.all(),
            'positions': Position.objects.all()},
        RequestContext(request))


def add_cv_vf(request):
    """
    display add CV template form.
    check data & save.
    """
    cv = get_cv(request)
    if not check_permission(cv, perm_index=49): # create new CV
        messages.error(request, "Access denied")
        return redirect("erp_home")
    stage = request.REQUEST.get('stage', None)
    if stage == 'validate':
        cv_mform = CVAddMForm(request.POST)
        if cv_mform.is_valid():
            cv_mform.save()
            messages.success(request, 'New CV template created successfully.')
            return  redirect("erp_cvs_manage")
        else: # errors in saving
            messages.error(request, 'CV didn`t save. There were some errors.')
    else: # stage == input
        cv_mform = CVAddMForm()
    return render_to_response(
                "cv/add_cv.html",
                {
                    'cv': cv,
                    'nav': "cv",
                    'cv_mform': cv_mform},
                RequestContext(request))