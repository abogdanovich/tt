# Template tag

#mod3

from timecard.models import User
from django import template
from timecard import utils

register = template.Library()

@register.inclusion_tag('timecard/currency.html', takes_context = True)
def currency(context):

    request = context['request']

    user = User.objects.get(id=int(request.session['uid']))
    active = utils.get_modules(user.id, "mod3")

    d =  dict(active=active,office = user.office, bel = ["M","G"], rus = ["MO","UL","OB"])

    return d
