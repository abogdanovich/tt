# Template tag

from timecard.models import User, User_duty, UserPostComment
from django import template
from timecard import utils
import datetime

register = template.Library()

@register.inclusion_tag('timecard/spam_module.html', takes_context = True)
def spam_module(context):

    request = context['request']
    
    user = User.objects.get(id=int(request.session['uid']))
    comments = []    
    comments = UserPostComment.objects.all().order_by("-created")[:8]	
    
    d = dict(comments=comments)

    return d
