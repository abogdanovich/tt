# -*- coding: utf-8 -*-
__author__ = 'ABKorotky'
__email__ = ['akorotky@minsk.ximxim.com', 'aleksandr.korotky@ximad.com']


from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from timecard.models import User as ttUser
from models import CV, CVSkill


#print('calc_pages_url callback function. the sender is: %s. the kwargs is: %r. the signal.__dict__ is: %r' % (sender, kwargs, kwargs['signal'].__dict__))


@receiver(post_save, sender=ttUser)
def post_save_ttUser_handler(sender, **kwargs):
    """
    This signal handler making autoadding new CV after new user was been created
    """
    if kwargs.get('created', None):
        user = kwargs['instance']
        if user.accessLevel == 4:
            al = True
        else:
            al = False
        CV.objects.get_or_create(user=user, name=user.name, surname=user.surname, login=user.login, accessLevel=al)


@receiver(pre_delete, sender=ttUser)
def pre_delete_ttUser_handler(sender, **kwargs):
    """
    This signal handler making autostore some info before deleting current user.
    This is info used in resume.
    """
    user = kwargs['instance']
    try:
        cv = CV.objects.get(user=user)
        cv.user = None
        cv.fired = True
    except CV.DoesNotExist:
        pass
