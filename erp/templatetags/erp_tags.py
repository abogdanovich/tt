# -*- coding: utf-8 -*-
__author__ = 'ABKorotky'
__email__ = ['akorotky@minsk.ximxim.com', 'aleksandr.korotky@ximad.com']


from classytags.core import Tag, Options
from classytags.arguments import Argument
from django import template


register = template.Library()

class ToDays(Tag):
    name = 'to_days'
    options = Options(
        Argument('hours'),
    )

    def render_tag(self, context, hours=0):
        return str(hours/8)

register.tag(ToDays)


class Permission(Tag):
    name = 'permission'
    options = Options(
        Argument('cv'),
        Argument('perm_index'),
        blocks=[('not_permission', 'has_perm'), ('endpermission', 'has_not_perm')],
    )

    def render_tag(self, context, cv, perm_index, has_perm=None, has_not_perm=None):
        #context.push()
        output = ""
        if cv.position and cv.position.permissions[perm_index] == "1":
            if has_perm:
                output = has_perm.render(context)
        else:
            if has_not_perm:
                output = has_not_perm.render(context)
        #context.pop()
        return output

register.tag(Permission)