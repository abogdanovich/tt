# Template tag

from timecard.models import User, Offices
from django import template
import time

register = template.Library()


@register.inclusion_tag('timecard/hb_informer.html', takes_context=True)
def hb_informer(context):

    request = context['request']
    user = User.objects.get(id=int(request.session['uid']))

    timeshift = int(Offices.objects.get(short_name=user.office).time_shift)
    NOW = int(round(time.time())) + timeshift - 3 * 3600
    month = time.strftime('%m', time.gmtime(NOW))
    day = time.strftime('%d', time.gmtime(NOW))
    today = month + "/" + day
    users = User.objects.filter(hb=today)
    offices = Offices.objects.all()
    qty_of_users_with_hb = users.count()
    d = dict(users=users, qty=qty_of_users_with_hb, offices = offices)

    return d