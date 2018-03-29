# -*- coding: utf-8 -*-
__author__ = 'ABKorotky'
__email__ = ['akorotky@minsk.ximxim.com', 'aleksandr.korotky@ximad.com']


#from django.conf.urls.defaults import patterns, url, include
from django.conf.urls import patterns, url, include


urlpatterns = patterns('customers.views',
    url(r'^$', "list_vf", name="erp_customers"),
    url(r'^add/$', "mod_vf", kwargs={'op': "add"}, name="erp_customer_add"),
    url(r'^(?P<c_id>\d+)/$', "view_vf", name="erp_customer"),
    url(r'^(?P<c_id>\d+)/mod/$', "mod_vf", kwargs={'op': "mod"}, name="erp_customer_mod"),
    url(r'^(?P<c_id>\d+)/del/$', "mod_vf", kwargs={'op': "del"}, name="erp_customer_del"),
)