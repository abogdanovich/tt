# -*- coding: utf-8 -*-
__author__ = 'ABKorotky'
__email__ = ['akorotky@minsk.ximxim.com', 'aleksandr.korotky@ximad.com']


#from django.conf.urls.defaults import patterns, url, include
from django.conf.urls import patterns, url, include


urlpatterns = patterns('',
    url(r'^cv/', include('cv.urls', app_name='timetracker')),
    url(r'^project/', include('projects.urls', app_name='timetracker')),
    url(r'^customer/', include('customers.urls', app_name='timetracker')),
    url(r'^login/', "erp.views.login_vf", name="erp_login"),
    url(r'^logout/', "erp.views.logout_vf", name="erp_logout"),
    url(r'^$', "erp.views.main_vf", name="erp_home"),
)

