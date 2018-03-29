# -*- coding: utf-8 -*-
__author__ = 'ABKorotky'
__email__ = ['akorotky@minsk.ximxim.com', 'aleksandr.korotky@ximad.com']


import logging
from django.contrib import messages
from django.shortcuts import redirect
from timecard.models import User as ttUser
from cv.models import CV, MANAGE_LEVEL

import logging

def get_cv(request):
    """
    function return the obj id current cv
    """
    try:
        return CV.objects.get(id=int(request.session.get('cv_id', 0)))
    except CV.DoesNotExist:
        return None


def check_login(func):
    def wrapper(request, *args, **kw):
        if request.session.get('cv_id', None):
            # it`s ok!!!
            return func(request, *args, **kw)
        else:
            # cv_id is missing - it may be first request from tt or not.
            if request.session.get('uid', None):
                # user is tt-user. it`s ok!!!
                try:
                    request.session['cv_id'] = ttUser.objects.get(id = int(request.session['uid'])).cv.id
                    return func(request, *args, **kw)
                except ttUser.DoesNotExist:
                    messages.error(request, "Re-login please.")
                    redirect("erp_login")
            else:
                # it is first request. need ldap check
                return redirect("erp_login")
    return wrapper


def is_manage(request):
    """
    function check cv manage access level
    """
    try:
        if CV.objects.get(id=int(request.session.get('cv_id', 0))).accessLevel == MANAGE_LEVEL:
            return True
        else:
            return False
    except CV.DoesNotExist:
        return False


def check_manage(func):
    """
    decorator for check cv manage access level and redirect if none access.
    """
    def wrapper(request, *args, **kwargs):
        cv = get_cv(request)
        if cv.accessLevel == MANAGE_LEVEL:
            return func(request, *args, **kwargs)
        logging.debug(u"check manage access: user with login %s tried to load denied ERP page '%s'." % (cv.login, request.path))
        messages.error(request, "Access denied")
        return redirect("erp_home")
    return wrapper


def check_access_to_cv(func):
    def wrapper(request, *args, **kwargs):
        cv = get_cv(request)
        if cv.accessLevel == MANAGE_LEVEL:
            return func(request, *args, **kwargs)
        else:
            try:
                if cv.id == int(kwargs['cv_id']):
                    return func(request, *args, **kwargs)
                else:
                    logging.debug(u"check access to cv: user with login %s tried to load denied CV page %s" % (cv.login, kwargs['cv_id']))
                    messages.error(request, "Access denied")
                    return redirect("erp_home")
            except KeyError:
                raise AttributeError("The check_access_to_cv doesn`t have a required parameter 'cv_id'.")
    return wrapper


def check_permission(cv, perm_index=None):
    """
    function for check cv current permission
    """
    if cv.position and cv.position.permissions[perm_index] == "1":
        return True
    return False