# -*- coding: utf-8 -*-
__author__ = 'ABKorotky'
__email__ = ['akorotky@minsk.ximxim.com', 'aleksandr.korotky@ximad.com']


from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.contrib import messages

from erp.utils import get_cv, check_login, check_permission

from cv.models import CV, PrevProject, PrevScreenshot
from cv.forms import PrevProjectMForm, PrevProjectMFormset, PrevProjectIFormset, PrevProjectSSMForm, PrevProjectSSIFormset
import logging


@check_login
def list_vf(request, cv_id=None):

    """
    Display the list of previous projects for current CV user.
    """
    return render_to_response(
        'cv/prev_projects/list.html',
        {},
        RequestContext(request)
    )


@check_login
def view_vf(request, cv_id=None, pp_id=None, output=''):
    """
    Display the full data for selected previous project.
    Also display print version of previous project.
    """
    if cv_id and pp_id:
        try:
            view_cv = CV.objects.get(id=int(cv_id))
            pp = PrevProject.objects.get(id=int(pp_id))
        except CV.DoesNotExist:
            messages.error(request, "CV was not found.")
            redirect("erp_home")
        except PrevProject.DoesNotExist:
            messages.error(request, "Previous Project was not found.")
            redirect("erp_home")
    else:
        messages.error(request, "Bad Request.")
        redirect("erp_home")
    cv = get_cv(request)
    if view_cv != cv:
        if not check_permission(cv, perm_index=46): # manage prev projects data
            messages.error(request, "Access denied")
            return redirect("erp_home")
    return render_to_response(
        'cv/prev_projects/view%s.html' % output,
        {
            'cv': cv,
            'view_cv': view_cv,
            'pp': pp,
            'sss': pp.screenshots.all(),
        },
        RequestContext(request)
    )


@check_login
def mod_vf(request, cv_id=None, pp_id=None, op=''):
    """
    Display the full data for selected previous project.
    Also display print version of previous project.
    """
    if cv_id:
        try:
            view_cv = CV.objects.get(id=int(cv_id))
        except CV.DoesNotExist:
            messages.error(request, "CV was not found.")
            redirect("erp_home")
    else:
        messages.error(request, "Bad Request.")
        redirect("erp_home")
    cv = get_cv(request)
    if view_cv != cv:
        if not check_permission(cv, perm_index=46): # manage prev projects data
            messages.error(request, "Access denied")
            return redirect("erp_home")
    stage = request.REQUEST.get('stage', 'input')
    pp_mform = None
    pp_ss_iforms = None
    # add empty project
    if op == 'add':
        if stage == 'validate':
            if stage == 'validate':
                pp_mform = PrevProjectMForm(request.POST)
                if pp_mform.is_valid():
                    pp_mform.save()
                    messages.success(request, 'Previous Project data saved successfully.')
                    return redirect("erp_cv_prevproject_mod", cv_id=view_cv.id, pp_id=pp_mform.instance.id)
                else:
                    messages.error(request, 'Project data didn`t save. You have some errors.')
        else:
            pp_mform = PrevProjectMForm(initial={'cv':view_cv})
    # modify data of project or delete
    else:
        if pp_id:
            try:
                pp = PrevProject.objects.get(id=int(pp_id))
                if stage == 'confirm':
                    pp.delete()
                    messages.success(request, 'Previous Project data deleted successfully.')
                    return redirect("erp_cv", cv_id=view_cv.id)
                if stage == 'validate':
                    pp_mform = PrevProjectMForm(request.POST, instance=pp)
                    if pp_mform.is_valid():
                        pp_mform.save()
                        messages.success(request, 'Previous Project data saved successfully.')
                        return redirect("erp_cv_prevproject_mod", cv_id=view_cv.id, pp_id=pp.id)
                    else:
                        messages.error(request, 'Previous Project data didn`t save. You have some errors.')
                # stage == input
                else:
                    pp_mform = PrevProjectMForm(instance=pp)
                pp_ss_iforms = PrevProjectSSIFormset(instance=pp)
            except PrevProject.DoesNotExist, PrevProject.MultipleObjectsReturned:
                messages.error(request, 'Project was not found.')
                return redirect("erp_cv", cv_id=view_cv.id)
        else:
            messages.error(request, 'Bad request.')
            return redirect("erp_home")
    return render_to_response(
        'cv/prev_projects/mod.html',
        {
            'cv': cv,
            'view_cv': view_cv,
            'pp_mform': pp_mform,
            'op': op,
            'pp_ss_iforms': pp_ss_iforms,
        },
        RequestContext(request)
    )


@check_login
def mod_ss_vf(request, cv_id=None, pp_id=None):
    """
    Save the screenshots for CV previous projects.
    make redirect to previous project modify data page.
    """
    if cv_id and pp_id:
        try:
            view_cv = CV.objects.get(id=int(cv_id))
            pp = PrevProject.objects.get(id=int(pp_id))
        except CV.DoesNotExist:
            messages.error(request, "CV was not found.")
            redirect("erp_home")
        except PrevProject.DoesNotExist:
            messages.error(request, "Previous Project was not found.")
            redirect("erp_home")
    else:
        messages.error(request, "Bad Request.")
        redirect("erp_home")
    cv = get_cv(request)
    if view_cv != cv:
        if not check_permission(cv, perm_index=46): # manage prev projects data
            messages.error(request, "Access denied")
            return redirect("erp_home")
    stage = request.REQUEST.get('stage', 'input')
    if stage == 'validate':
        pp_ss_iforms = PrevProjectSSIFormset(request.POST, request.FILES, instance=pp)
        if pp_ss_iforms.is_valid():
            pp_ss_iforms.save()
            messages.success(request, 'Screenshot(s) for Previous Project saved successfully.')
            return redirect("erp_cv_prevproject_mod", cv_id=view_cv.id, pp_id=pp.id)
        else:
            messages.error(request, 'Screensoot(s) for Previous Project didn`t save. You have some errors.')
    return render_to_response(
        'cv/prev_projects/mod.html',
        {
            'cv': cv,
            'view_cv': view_cv,
            'pp_mform': PrevProjectMForm(instance=pp),
            'op': "mod",
            'pp_ss_iforms': pp_ss_iforms,
        },
        RequestContext(request)
    )


@check_login
def del_vf(request, cv_id=None):
    """
    Display the list of previous projects for current CV user.
    """
    if cv_id:
        try:
            view_cv = CV.objects.get(id=int(cv_id))
        except CV.DoesNotExist:
            messages.error(request, "CV was not found.")
            redirect("erp_home")
    else:
        messages.error(request, "Bad Request.")
        redirect("erp_home")
    cv = get_cv(request)
    if view_cv != cv:
        if not check_permission(cv, perm_index=46): # manage prev projects data
            messages.error(request, "Access denied")
            return redirect("erp_home")
    stage = request.REQUEST.get('stage', 'input')
    if stage == 'confirm':
        pp_iforms = PrevProjectIFormset(request.POST, instance=view_cv)
        if pp_iforms.is_valid():
            pp_iforms.save()
            messages.success(request, 'Selected Previous Project(s) have been delete successfully.')
            return redirect("erp_cv", cv_id=view_cv.id)
        else:
            messages.error(request, 'Selected Previous Project(s) haven`t been delete. You have some errors.')
    elif stage=='input':
        pp_iforms = PrevProjectIFormset(instance=view_cv)
    return render_to_response(
        'cv/prev_projects/del.html',
        {
            'cv': cv,
            'view_cv': view_cv,
            'pp_iforms': pp_iforms,
        },
        RequestContext(request)
    )