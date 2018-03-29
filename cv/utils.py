# -*- coding: utf-8 -*-
__author__ = 'ABKorotky'
__email__ = ['akorotky@minsk.ximxim.com', 'aleksandr.korotky@ximad.com']

from timecard.models import User as ttUser
from timecard import utils
from timecard.views import set_menu

from models import CV


def init_context(request, menu_cmd):
    set_menu(request, menu_cmd)
    user = ttUser.objects.get(id=int(request.session['uid']))
    custom_CSS = utils.change_css_on_some_event(user)
    return dict(request=request, user=user, custom_CSS = custom_CSS)


def get_curr_cv(request):
    """
    function return the obj od current ttUser
    """
    if request.REQUEST.get('user', None):
        try:
            return CV.objects.get(id=int(request.REQUEST['user']))
        except ttUser.DoesNotExist:
            return None
    else:
        return None
