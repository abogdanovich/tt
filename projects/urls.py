# -*- coding: utf-8 -*-
__author__ = 'ABKorotky'
__email__ = ['akorotky@minsk.ximxim.com', 'aleksandr.korotky@ximad.com']

# from django.conf.urls.defaults import patterns, url, include
from django.conf.urls import patterns, url, include

urlpatterns = patterns('projects.views',
    url(r'^projects/$', "project.list_vf", name="erp_projects"),
    url(r'^manage/$', "project.manage_vf", name="erp_projects_manage"),
    url(r'^filter/$', "project.filter_vf", kwargs={'op': ""}, name="erp_projects_filter"),
    url(r'^filter/data/$', "project.filter_vf", kwargs={'op': "data"}, name="erp_projects_filter_data"),
    url(r'^filter/presets/$', "project.filter_vf", kwargs={'op': "presets"}, name="erp_projects_filter_presets"),
    url(r'^filter/requirements/$', "project.filter_vf", kwargs={'op': "reqs"}, name="erp_projects_filter_reqs"),
    url(r'^add/$', "project.mod_vf", kwargs={'op': "add"}, name="erp_project_add"),
    url(r'^add/preset/(?P<pst_id>\d+)/$', "project.mod_vf", kwargs={'op': "preset"}, name="erp_project_add_preset"),
    url(r'^copy/(?P<prj_id>\d+)/$', "project.mod_vf", kwargs={'op': "copy"}, name="erp_project_copy"),
    url(r'^(?P<prj_id>\d+)/$', "project.view_vf", kwargs={'output': ""}, name="erp_project"),
    url(r'^(?P<prj_id>\d+)/print/$', "project.view_vf", kwargs={'output': "_print"}, name="erp_project_print"),
    url(r'^(?P<prj_id>\d+)/mod/$', "project.mod_vf", kwargs={'op': "mod"}, name="erp_project_mod"),
    url(r'^(?P<prj_id>\d+)/mod/wg/$', "project.mod_wg_vf", name="erp_project_mod_wg"),
    url(r'^(?P<prj_id>\d+)/mod/req/$', "project.mod_req_vf", name="erp_project_mod_req"),
    url(r'^(?P<prj_id>\d+)/mod/ss/$', "project.mod_ss_vf", name="erp_project_mod_ss"),
    url(r'^(?P<prj_id>\d+)/add/req/$', "project.add_req_vf", name="erp_project_add_req"),
    url(r'^(?P<prj_id>\d+)/del/$', "project.mod_vf", kwargs={'op': "del"}, name="erp_project_del"),
    # project presets
    url(r'^presets/$', "presets.list_vf", name="erp_project_presets"),
    url(r'^presets/add/$', "presets.mod_vf", kwargs={'op': "add"}, name="erp_project_presets_add"),
    url(r'^presets/add/(?P<prj_id>\d+)/$', "presets.mod_vf", kwargs={'op': "project"}, name="erp_project_presets_add_from_project"),
    url(r'^presets/(?P<pst_id>\d+)/$', "presets.view_vf", kwargs={'output': ""}, name="erp_project_preset"),
    url(r'^presets/(?P<pst_id>\d+)/add/req/$', "presets.add_req_vf", name="erp_project_preset_add_req"),
    url(r'^presets/(?P<pst_id>\d+)/mod/req/$', "presets.mod_req_vf", name="erp_project_preset_mod_req"),
    url(r'^presets/(?P<pst_id>\d+)/mod/$', "presets.mod_vf", kwargs={'op': "mod"}, name="erp_project_preset_mod"),
    url(r'^presets/(?P<pst_id>\d+)/del/$', "presets.mod_vf", kwargs={'op': "del"}, name="erp_project_preset_del"),
    url(r'^presets/(?P<pst_id>\d+)/print/$', "presets.view_vf", kwargs={'output': "_print"}, name="erp_project_preset_print"),
)