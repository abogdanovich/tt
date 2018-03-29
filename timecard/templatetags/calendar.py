# Template tag
from datetime import date, timedelta
from django import template
from timecard import utils
from timecard.models import CalendarDaysOff, User
import settings

register = template.Library()

def get_last_day_of_month(year, month):

    if month == 12:
        year += 1
        month = 1
    else:
        month += 1
    return date(year, month, 1) - timedelta(1)

@register.inclusion_tag('timecard/calendar.html',takes_context = True)
def calendar(context):

    request = context['request']

    uid = request.session['uid']
    office = User.objects.get(id=int(uid)).office

    static_url = settings.STATIC_URL
    
    year=date.today().year
    month=date.today().month
    today=date.today().day
    
    #current month
    start_date = utils.make_month_date(year, month, 1, "start")
    #end of cur month
    end_date = utils.make_month_date(year, month, utils.get_month_days()-1, "end")

    days_off = CalendarDaysOff.objects.filter(date__range=(start_date, end_date),office=office).order_by('date')

    first_day_of_month = date(year, month, 1)
    month_name = first_day_of_month.strftime("%B")

    last_day_of_month = get_last_day_of_month(year, month)

    first_day_of_calendar = first_day_of_month - timedelta(first_day_of_month.weekday())
    last_day_of_calendar = last_day_of_month + timedelta(7 - last_day_of_month.weekday())


    calendar = []
    week = []
    week_headers = []

    i = 0
    day = first_day_of_calendar
    while day <= last_day_of_calendar:
        if i < 7:
            week_headers.append(day)
        cal_day = {}
        cal_day['day'] = day
        cal_day['event'] = False
        for event in days_off:
            in_day = utils.make_month_date(day.year, day.month, day.day, "start")
            if in_day == event.date:
                cal_day['event'] = True

        if len(utils.get_hb_list("%02d/%02d" % (day.month,day.day))):
            cal_day['hb'] = True
	if day.day == today:
	    cal_day['today'] = True
	else:
	    cal_day['today'] = False

        if day.month == month:
            cal_day['in_month'] = True
        else:
            cal_day['in_month'] = False
        week.append(cal_day)

        if day.weekday() == 6:
            calendar.append(week)
            week = []
        i += 1
	day += timedelta(1)
	month_value = "%02d" % month
    d =  dict(calendar=calendar, headers=week_headers, month_name=month_name, month=month_value, today=today, static_url=static_url)

    return d
