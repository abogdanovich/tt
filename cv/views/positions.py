# -*- coding: utf-8 -*-
__author__ = 'ABKorotky'
__email__ = ['akorotky@minsk.ximxim.com', 'aleksandr.korotky@ximad.com']


from django.contrib import messages
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from erp.utils import get_cv, check_login, check_permission

from cv.models import Position
from cv.forms import PositionMFormset
from cv.permissions import PERMISSIONS, PermissionForm


@check_login
def positions_vf(request):
    """
    display position list formset.
    operations are add new position, modify data & delete positions.
    check data & save.
    """
    cv = get_cv(request)
    if not check_permission(cv, perm_index=35): # view position data
        messages.error(request, "Access denied")
        return redirect("erp_home")
    else:
        manage = False
        if check_permission(cv, perm_index=36): # manage position data
            manage = True
    positions = None
    pos_mforms = None
    stage = request.REQUEST.get('stage', None)
    if stage == 'confirm':
        if manage:
            pos_del = request.session.get('pos_del', None)
            for pos in pos_del:
                pos.delete()
            del request.session['pos_del']
        else:
            messages.error(request, "Access denied")
            return redirect("erp_home")
    if stage == 'validate':
        if manage:
            pos_mforms = PositionMFormset(request.POST)
            if pos_mforms.is_valid():
                if pos_mforms.deleted_forms:
                    request.session['pos_del'] = [form.instance for form in pos_mforms.deleted_forms]
                    return render_to_response(
                        "cv/del_positions.html",
                        {
                            'cv': get_cv(request),
                            'nav': "cv",
                            'pos_del': request.session['pos_del'],
                            },
                        RequestContext(request))
                pos_mforms.save()
                messages.success(request, 'Positions updated successfully.')
            else: # errors in saving
                messages.error(request, 'Positions didn`t save. There were some errors.')
        else:
            messages.error(request, "Access denied")
            return redirect("erp_home")
    else: # stage == input
        if manage:
            pos_mforms = PositionMFormset()
        else:
            positions = Position.objects.all()
    return render_to_response(
        "cv/positions.html",
        {
            'cv': cv,
            'nav': "cv",
            'positions': positions,
            'pos_mforms': pos_mforms,
            },
        RequestContext(request))


@check_login
def mod_permissions_vf(request, pos_id=None):
    """
    display & edit permissions for selected position
    """
    def make_perm_list(perm_str):
        perms = []
        i = 0
        for perm in PERMISSIONS:
            if perm:
                val = False
                if perm_str[i] == "1":
                    val = True
                perms.append((perm, val))
            i += 1
        return perms
    # ----- MAIN -----
    cv = get_cv(request)
    if not check_permission(cv, perm_index=0): # view permissions
        messages.error(request, "Access denied")
        return redirect("erp_home")
    else:
        manage = False
        if check_permission(cv, perm_index=1): # edit permissions
            manage = True
    if not pos_id:
        messages.error(request, 'Bad request')
        return redirect("erp_home")
    try:
        position = Position.objects.get(id=int(pos_id))
    except Position.DoesNotExist, Position.MultipleObjectsReturned:
        messages.error(request, 'Position was not found.')
        return redirect("cv_positions")
    perms = None
    perms_form = None
    stage = request.REQUEST.get('stage', None)
    if stage == 'validate':
        if manage:
            perms_form = PermissionForm(request.POST)
            if perms_form.is_valid():
                cd = perms_form.cleaned_data
                perms = list(position.permissions)
                i = 0
                for perm in PERMISSIONS:
                    if perm:
                        if cd["p%u" % i]:
                            perms[i] = "1"
                        else:
                            perms[i] = "0"
                    i += 1
                position.permissions = "".join(perms)
                position.save()
                perms = make_perm_list(position.permissions)
                messages.success(request, 'Permissions updated successfully.')
            else: # errors in saving
                messages.error(request, 'Permissions didn`t save. There were some errors.')
        else:
            messages.error(request, "Access denied")
            return redirect("erp_home")
    else: # stage == input
        if manage:
            init = {}
            i = 0
            for perm in PERMISSIONS:
                if perm:
                    val = False
                    if position.permissions[i] == "1":
                        val = True
                    init["p%u" % i] = val
                i += 1
            perms_form = PermissionForm(initial=init)
        else:
            perms = make_perm_list(position.permissions)
    return render_to_response(
        "cv/mod_permissions.html",
        {
            'cv': cv,
            'nav': "cv",
            'position': position,
            'perms': perms,
            'perms_form': perms_form,
            },
        RequestContext(request))