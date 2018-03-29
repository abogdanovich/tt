# Template tag

from timecard.models import User
from django import template

register = template.Library()


@register.inclusion_tag('timecard/check_user_provide_full_info.html', takes_context=True)
def check_user_provide_full_info(context):

    request = context['request']
    user = User.objects.get(id=int(request.session['uid']))
    d = dict(user=user)

    return d