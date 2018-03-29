# -*- coding: utf-8 -*-
__author__ = 'ABKorotky'
__email__ = ['akorotky@minsk.ximxim.com', 'aleksandr.korotky@ximad.com']


#from django.conf.urls.defaults import patterns, url
from django.conf.urls import patterns, url


urlpatterns = patterns('cv.views',
    url(r'^$', "cvitae.list_vf", kwargs={'fltr':"all"}, name="erp_cvs"),
    url(r'^filter/full/$', "cvitae.list_vf", kwargs={'fltr':"full"}, name="erp_cvs_full"),
    url(r'^filter/empty_position/$', "cvitae.list_vf", kwargs={'fltr':"position"}, name="erp_cvs_empty_position"),
    url(r'^filter/empty_fl/$', "cvitae.list_vf", kwargs={'fltr':"fls"}, name="erp_cvs_empty_fls"),
    url(r'^filter/empty_skills/$', "cvitae.list_vf", kwargs={'fltr':"skills"}, name="erp_cvs_empty_skills"),
    url(r'^filter/empty_projects/$', "cvitae.list_vf", kwargs={'fltr':"projects"}, name="erp_cvs_empty_projects"),
    url(r'^filter/prepare/$', "cvitae.list_vf", kwargs={'fltr':"prepare"}, name="erp_cvs_prepare"),
    url(r'^filter/develop/$', "cvitae.list_vf", kwargs={'fltr':"develop"}, name="erp_cvs_develop"),
    url(r'^filter/work/$', "cvitae.list_vf", kwargs={'fltr':"work"}, name="erp_cvs_work"),
    url(r'^filter/pause/$', "cvitae.list_vf", kwargs={'fltr':"pause"}, name="erp_cvs_pause"),
    url(r'^filter/idle/$', "cvitae.list_vf", kwargs={'fltr':"idle"}, name="erp_cvs_idle"),
    url(r'^manage/$', "cvitae.manage_vf", name="erp_cvs_manage"),
    url(r'^(?P<cv_id>\d+)/$', "cvitae.view_cv_vf", kwargs={'output': ""}, name="erp_cv"),
    url(r'^(?P<cv_id>\d+)/print/$', "cvitae.view_cv_vf", kwargs={'output': "_print"}, name="erp_cv_print"),
    url(r'^add/$', "cvitae.add_cv_vf", name="erp_cv_add"),
    url(r'^(?P<cv_id>\d+)/mod/personal/$', "cvitae.mod_cv_personal_vf", name="erp_cv_mod_personal"),
    url(r'^(?P<cv_id>\d+)/mod/contacts/$', "cvitae.mod_cv_contacts_vf", name="erp_cv_mod_contacts"),
    url(r'^(?P<cv_id>\d+)/mod/fl/$', "cvitae.mod_cv_fl_vf", name="erp_cv_mod_fl"),
    url(r'^(?P<cv_id>\d+)/mod/skills/$', "cvitae.mod_cv_skills_vf", name="erp_cv_mod_skills"),
    url(r'^(?P<cv_id>\d+)/mod/projects/$', "cvitae.mod_cv_projects_vf", name="erp_cv_mod_projects"),
    url(r'^(?P<cv_id>\d+)/add/skills/$', "cvitae.add_cv_skills_vf", name="erp_cv_add_skills"),
    url(r'^(?P<cv_id>\d+)/certificates/$', "certificates.list_vf", name="erp_cv_certificates"),
    url(r'^(?P<cv_id>\d+)/certificates/add/$', "certificates.mod_vf", kwargs={'op':"add"}, name="erp_cv_certificates_add"),
    url(r'^(?P<cv_id>\d+)/certificates/del/$', "certificates.del_vf", name="erp_cv_certificates_del"),
    url(r'^(?P<cv_id>\d+)/certificate/(?P<cert_id>\d+)/$', "certificates.view_vf", kwargs={'output':""}, name="erp_cv_certificate"),
    url(r'^(?P<cv_id>\d+)/certificate/(?P<cert_id>\d+)/print/$', "certificates.view_vf", kwargs={'output':"_print"}, name="erp_cv_certificate_print"),
    url(r'^(?P<cv_id>\d+)/certificate/(?P<cert_id>\d+)/mod/$', "certificates.mod_vf", kwargs={'op':"mod"}, name="erp_cv_certificate_mod"),
    url(r'^(?P<cv_id>\d+)/certificate/(?P<cert_id>\d+)/del/$', "certificates.mod_vf", kwargs={'op':"del"}, name="erp_cv_certificate_del"),
    url(r'^(?P<cv_id>\d+)/prev_projects/$', "prev_projects.list_vf", name="erp_cv_prevprojects"),
    url(r'^(?P<cv_id>\d+)/prev_projects/del/$', "prev_projects.del_vf", name="erp_cv_prevprojects_del"),
    url(r'^(?P<cv_id>\d+)/prev_project/(?P<pp_id>\d+)/$', "prev_projects.view_vf", kwargs={'output': ""}, name="erp_cv_prevproject"),
    url(r'^(?P<cv_id>\d+)/prev_project/(?P<pp_id>\d+)/print/$', "prev_projects.view_vf", kwargs={'output': "_print"}, name="erp_cv_prevproject_print"),
    url(r'^(?P<cv_id>\d+)/prev_project/add/$', "prev_projects.mod_vf", kwargs={'op': "add"}, name="erp_cv_prevproject_add"),
    url(r'^(?P<cv_id>\d+)/prev_project/(?P<pp_id>\d+)/del/$', "prev_projects.mod_vf", kwargs={'op': "del"}, name="erp_cv_prevproject_del"),
    url(r'^(?P<cv_id>\d+)/prev_project/(?P<pp_id>\d+)/mod/$', "prev_projects.mod_vf", kwargs={'op': "mod"}, name="erp_cv_prevproject_mod"),
    url(r'^(?P<cv_id>\d+)/prev_project/(?P<pp_id>\d+)/ss/$', "prev_projects.mod_ss_vf", name="erp_cv_prevproject_mod_ss"),
    url(r'^skills/$', "skills.skills_vf", name="erp_skills"),
    url(r'^positions/$', "positions.positions_vf", name="erp_positions"),
    url(r'^positions/del/$', "positions.positions_vf", name="erp_del_positions"),
    url(r'^position/add/$', "positions.positions_vf", name="erp_add_position"),
    url(r'^position/(?P<pos_id>\d+)/mod/$', "positions.positions_vf", name="erp_mod_position"),
    url(r'^position/(?P<pos_id>\d+)/permissions/$', "positions.mod_permissions_vf", name="erp_position_permissions"),
    url(r'^filter/(?P<s_id>\d+)/', "skills.filter_skill_vf", name="erp_cv_filter_skill"),
)
