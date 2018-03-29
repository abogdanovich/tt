# Template tag

from timecard.models import User, User_duty
from django import template
from timecard import utils
import datetime

register = template.Library()

@register.inclusion_tag('timecard/duty_user.html', takes_context = True)
def duty_user(context):

    request = context['request']
    
    user = User.objects.get(id=int(request.session['uid']))
    
    date = "%s-%02d-%02d" % (datetime.date.today().year, datetime.date.today().month, datetime.date.today().day)
    duser = User_duty.objects.filter(date=date)
    
    dutyman = []
    
    for d in duser:
	try:
	    dutyman = User.objects.get(id=d.user, office=user.office)
	except:
	    dutyman = []
	
    d = dict(dutyman=dutyman)

    return d
