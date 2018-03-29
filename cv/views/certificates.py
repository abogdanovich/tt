# -*- coding: utf-8 -*-
__author__ = 'ABKorotky'
__email__ = ['akorotky@minsk.ximxim.com', 'aleksandr.korotky@ximad.com']


from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.contrib import messages

from erp.utils import get_cv, check_login, check_permission

from cv.models import CV, Certificate
from cv.forms import CertificateMForm, BrieflyCertificateIFormset
import logging

@check_login
def list_vf(request, cv_id=None):
    """
    Display the certificates list for current CV user.
    """
    return render_to_response(
        'cv/certificates/list.html',
        {},
        RequestContext(request)
    )


@check_login
def view_vf(request, cv_id=None, cert_id=None, output=''):
    """
    Display the full data for selected certificate.
    Also display print version of certificate.
    """
    if cv_id and cert_id:
        try:
            view_cv = CV.objects.get(id=int(cv_id))
            cert = Certificate.objects.get(id=int(cert_id))
        except CV.DoesNotExist:
            messages.error(request, "CV was not found.")
            redirect("erp_home")
        except Certificate.DoesNotExist:
            messages.error(request, "Certificate was not found.")
            redirect("erp_home")
    else:
        messages.error(request, "Bad Request.")
        redirect("erp_home")
    cv = get_cv(request)
    return render_to_response(
        'cv/certificates/view%s.html' % output,
        {
            'cv': cv,
            'view_cv': view_cv,
            'certificate': cert,
        },
        RequestContext(request)
    )


@check_login
def mod_vf(request, cv_id=None, cert_id=None, op=''):
    """
    Display the full data for selected certificate.
    Manage the operations add/edit/delete.
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
        if not check_permission(cv, perm_index=44): # manage certificate data
            messages.error(request, "Access denied")
            return redirect("erp_home")
    stage = request.REQUEST.get('stage', 'input')
    cert_mform = None
    # add empty project
    if op == 'add':
        if stage == 'validate':
            if stage == 'validate':
                cert_mform = CertificateMForm(request.POST, request.FILES)
                if cert_mform.is_valid():
                    cert_mform.save()
                    messages.success(request, 'Certificate data saved successfully.')
                    return redirect("erp_cv_certificate_mod", cv_id=view_cv.id, cert_id=cert_mform.instance.id)
                else:
                    messages.error(request, 'Certificate data didn`t save. You have some errors.')
        else:
            cert_mform = CertificateMForm(initial={'cv':view_cv})
    # modify data of project or delete
    else:
        if cert_id:
            try:
                cert = Certificate.objects.get(id=int(cert_id))
                if stage == 'confirm':
                    cert.delete()
                    messages.success(request, 'Selected Certificate data deleted successfully.')
                    return redirect("erp_cv", cv_id=view_cv.id)
                if stage == 'validate':
                    cert_mform = CertificateMForm(request.POST, request.FILES, instance=cert)
                    if cert_mform.is_valid():
                        cert_mform.save()
                        messages.success(request, 'Certificate data saved successfully.')
                        return redirect("erp_cv_certificate_mod", cv_id=view_cv.id, cert_id=cert.id)
                    else:
                        messages.error(request, 'Certificate data didn`t save. You have some errors.')
                # stage == input
                else:
                    cert_mform = CertificateMForm(instance=cert)
            except Certificate.DoesNotExist, Certificate.MultipleObjectsReturned:
                messages.error(request, 'Certificate was not found.')
                return redirect("erp_cv", cv_id=view_cv.id)
        else:
            messages.error(request, 'Bad request.')
            return redirect("erp_home")
    return render_to_response(
        'cv/certificates/mod.html',
        {
            'cv': cv,
            'view_cv': view_cv,
            'cert_mform': cert_mform,
            'op': op,
        },
        RequestContext(request)
    )


@check_login
def del_vf(request, cv_id=None):
    """
    Display the certificates list for current CV user, confirm delete selected and delete theirs.
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
        if not check_permission(cv, perm_index=44): # manage certificate data
            messages.error(request, "Access denied")
            return redirect("erp_home")
    stage = request.REQUEST.get('stage', 'input')
    if stage == 'confirm':
        cert_iforms = BrieflyCertificateIFormset(request.POST, instance=cv)
        if cert_iforms.is_valid():
            cert_iforms.save()
            messages.success(request, 'Selected Certificate(s) have been delete successfully.')
            return redirect("erp_cv", cv_id=view_cv.id)
        else:
            messages.error(request, 'Selected Certificate(s) haven`t been delete. You have some errors.')
    elif stage=='input':
        cert_iforms = BrieflyCertificateIFormset(instance=view_cv)
    return render_to_response(
        'cv/certificates/del.html',
        {
            'cv': cv,
            'view_cv': view_cv,
            'cert_iforms': cert_iforms,
        },
        RequestContext(request)
    )