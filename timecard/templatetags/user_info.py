# Template tag
import time
from timecard.models import User, UserTime, Offices
from django import template
from timecard import utils
from django.template import RequestContext
import settings

register = template.Library()

@register.inclusion_tag('timecard/user_info.html', takes_context = True)
def user_info(context):

    request = context['request']
    
    uid = request.session['uid']
    ttuser = User.objects.get(id=int(uid))
    user_state = utils.get_user_state(ttuser.id)
    worked_online_time = 0
    timeshift = int(Offices.objects.get(short_name = ttuser.office).time_shift)
    # here we have to do a correction and store in DB not actually server time but users's local time
    # because all the users may be situated in different timezones.
    #
    # Also we have to subtract GMS +3 hours because server is in that timezone and we want to be based
    # on the local server time

    nowtime = int(round(time.time()))+timeshift - 3*3600 #get the local time right now
    if user_state == 1:
        #if status 1 (active) - let's get the last user time
        userlasttime = UserTime.objects.filter(user_id=ttuser.id).order_by('-time')[:1]
        worked_online_time = nowtime-userlasttime[0].time #minutes worked online
        #print "worked online seconds % s" % worked_online_time
        #print "converted seconds into minutes\hours: %s " % utils.convert_seconds(worked_online_time)

    year=int(time.strftime ('%Y', time.gmtime(nowtime)))
    month=int(time.strftime ('%m', time.gmtime(nowtime)))
    day=int(time.strftime ('%d', time.gmtime(nowtime)))
    tdate =  "%d-%02d-%02d" % (year, month, day)

    rangetime = utils.make_month_date(year, month, day, "start")

    user_month_seconds = utils.calc_total_month_hours(ttuser.id, month, year) + worked_online_time #add online time
    user_month_time = utils.convert_seconds(user_month_seconds)

    month_days = utils.get_working_month_days(ttuser.office)
    
    month_hours = month_days * 8
    month_user_time = user_month_time
    month_user_need_time = utils.get_required_time(ttuser.id)
    
    month_user_need_time -= worked_online_time
    
    month_user_need_time = utils.convert_seconds(month_user_need_time)
    
    media_url = settings.MEDIA_URL
    
    today_user_time = utils.calc_today_user_hours(uid, day) + worked_online_time
    #add online time of possible:
    
    timer_time = (8*60*60) - today_user_time # 8 hours = 8*60*60 seconds = 28800 seconds
    overtime = False
    
    if timer_time < 0:
        overtime = True
        timer_time = today_user_time - (8*60*60)
    
    today_user_time = utils.convert_seconds(today_user_time)
    
    is_duty = 0
    
    if utils.check_duty(tdate, int(uid)):
        is_duty = 1
    
    d = dict(timer_time = timer_time, media_url=media_url, ttuser=ttuser, user_month_time=user_month_time,
             month_days=month_days, month_hours=month_hours,month_user_time=month_user_time,
             month_user_need_time=month_user_need_time, user_state=user_state, context_instance=RequestContext(request),
             today_user_time=today_user_time, is_duty=is_duty, overtime=overtime)
    
    return d
