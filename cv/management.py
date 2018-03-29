# -*- coding: utf-8 -*-
__author__ = 'ABKorotky'
__email__ = ['akorotky@minsk.ximxim.com', 'aleksandr.korotky@ximad.com']


from django.conf import settings
from django.db.models.signals import post_syncdb
from django.dispatch import receiver

from timecard.models import User as ttUser
import models


def populate_cv():
    """
    Use this function if has been errors in auto populate
    """
    if settings.DEBUG:
        print "Adding empty CV to all current users. It may take several seconds..."
    for user in ttUser.objects.all():
        models.CV.objects.create(user=user, name=user.name, surname=user.surname).save()
    if settings.DEBUG:
        print "CV has been added to all current user."


# @receiver(post_syncdb, sender=models)
# def post_syncdb_CV_handler(sender, created_models, **kwargs):
#     """
#     print "kwargs: %s" % kwargs
#     kwargs: {
#     'signal': <django.dispatch.dispatcher.Signal object at 0x8825e8c>,
#     'db': 'default',
#     'created_models': set([
#         <class 'erp.models.CV'>,
#         <class 'erp.models.TE_Custom_Fields'>,
#         <class 'erp.models.CV_FL_Skills'>,
#         <class 'erp.models.CV_Fired_User'>
#         ]),
#     'app': <module 'erp.models' from '/home/aleksandr/projects/tt/erp/models.pyc'>,
#     'verbosity': 1,
#     'interactive': True
#     }
#     """
#     if models.CV in created_models:
#         populate_cv()
