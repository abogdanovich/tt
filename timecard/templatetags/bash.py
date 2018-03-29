# Template tag

#mod2

from timecard.models import User
from django import template
from timecard import utils

register = template.Library()

@register.inclusion_tag('timecard/bash.html', takes_context = True)
def bash(context):

    request = context['request']
    
    user = User.objects.get(id=int(request.session['uid']))
    active = utils.get_modules(user.id, "mod2")
    
    d =  dict(active=active)

    return d
