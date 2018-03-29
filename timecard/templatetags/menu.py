# Template tag

from django import template
from timecard.models import User, UserPost, UserMissedHours, ProjectThread
from timecard import utils
import datetime

register = template.Library()

@register.inclusion_tag('timecard/menu.html', takes_context = True)
def menu(context):

    request = context['request']
    uid = request.session['uid']
    ttuser = User.objects.get(id=int(uid))

    # we have to check for user reports page - do we have to show anything?
    daytoday= datetime.date.today().isoweekday()
    projects_assigned = ProjectThread.objects.filter(user_id = ttuser.id, who_unassigned = '')
    if (daytoday in [5,6,7]) and projects_assigned:
        conditions_check = True
    else:
        conditions_check = False

    new_posts = utils.get_user_spam_counts(uid)
    new_missed_req = utils.get_user_missedh_counts(uid)
    
    menu = request.session['page']
    active = True
    d =  dict(active=active, menu=menu, new_posts=new_posts, new_missed_req=new_missed_req, user=ttuser, conditions_check = conditions_check)

    return d
