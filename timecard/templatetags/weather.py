# Template tag

#mod1

from timecard.models import User, Offices
from django import template
from timecard import utils

register = template.Library()

@register.inclusion_tag('timecard/weather.html', takes_context = True)
def weather(context):

    request = context['request']
    #TODO: get user module state

    user = User.objects.get(id=int(request.session['uid']))
    active = utils.get_modules(user.id, "mod1")

    try:
        office = Offices.objects.get(short_name = user.office)
        d =  dict(active=active, office = office)
    except:
        d =  dict(active=False)

    return d
