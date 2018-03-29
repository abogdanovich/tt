# template tag

from timecard.models import Votes, User
from django import template
from timecard import utils

register = template.Library()

@register.inclusion_tag('timecard/voting.html', takes_context = True)
def voting (context):
    request = context['request']
    user = User.objects.get(id=int(request.session['uid']))
    if Votes.objects.filter(office=user.office): # if table is not empty
        current_voting = Votes.objects.filter(office=user.office).latest('id') # here we take the current (last) voting
        d =dict (current_voting = current_voting, voted = user.voted, uid = user.id)
    else:
        d= dict (current_voting = 0)

    return d