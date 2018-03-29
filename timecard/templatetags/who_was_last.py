from timecard.models import User, UserTime, Offices
from django import template
import time, datetime

register = template.Library()

@register.inclusion_tag('timecard/who_was_last.html', takes_context=True)
def who_was_last(context):

    request = context['request']
    user = User.objects.get(id=int(request.session['uid']))
    timeshift = int(Offices.objects.get(short_name = user.office).time_shift)
    #OK. now we have to find the actual start of the current day

    NOW = int(round(time.time())) + timeshift - 3 * 3600
    day = time.strftime ('%d', time.gmtime(NOW))
    month = time.strftime ('%m', time.gmtime(NOW))
    year = time.strftime ('%y', time.gmtime(NOW))
    day_b = datetime.datetime(int(year), int(month), int(day))
    day_start = time.mktime(day_b.timetuple()) + timeshift - 3 * 3600 #that is actual start of day

    #Good. Now we have to get the time for the 7 days before starting from yesterday.
    events = []
    day_end = day_start + 86399
    for x in range(0,9):
        day_start -= 86400
        day_end -= 86400
        #because UserTime don not use ForeignKey we have to do some shitcoding
        users_from_my_office = User.objects.filter(office=user.office).values_list('id',flat=True).distinct()
        if UserTime.objects.filter(time__range=(day_start, day_end),user_id__in=users_from_my_office):
            last_user_timestamp = UserTime.objects.filter(time__range=(day_start, day_end),user_id__in=users_from_my_office).order_by('time').reverse()[0]
            u = User.objects.get(id=last_user_timestamp.user_id)
            d = time.strftime('%d:%b:%Y', time.gmtime(last_user_timestamp.time))
            events.append((d,u))
    d = dict(user=user, events=events)
    return d