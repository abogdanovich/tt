from django.conf.urls import *
from django.conf.urls import patterns, url, include
# from django.conf.urls.defaults import patterns, url, include
from django.conf import settings
from dajaxice.core import dajaxice_autodiscover, dajaxice_config

from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from django_multiuploader_demo.multiuploader.views import multiuploader_delete
from django_multiuploader_demo.multiuploader.views import image_view
from django_multiuploader_demo.multiuploader.views import multiuploader

# from django_multiuploader_demo.multiuploader.views import *
# from django_multiuploader_demo.multiuploader import *
# from django_multiuploader_demo import *

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()
dajaxice_autodiscover()

urlpatterns = patterns('',
    url(r'^erp/', include('erp.urls', app_name='timetracker')),
    url(r'^', include('timecard.urls', app_name='timetracker')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.PROJECT_ROOT+'/static'}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.PROJECT_ROOT+'/media'}),
    # url(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^add_employee_to_project$', 'timecard.views.add_employee_to_project', name='multi'),
    url(r'^add_employee_to_real_project_project$', 'timecard.views.add_employee_to_real_project_project', name='multi'),
    url(r'^update_employee_role_on_empty_project$', 'timecard.views.update_employee_role_on_empty_project', name='multi'),
    url(r'^update_employee_role_on_real_project$', 'timecard.views.update_employee_role_on_real_project', name='multi'),
    url(r'^remove_employee_from_empty_project$', 'timecard.views.remove_employee_from_empty_project', name='multi'),

    url(r'^update_file_description_for_empty_project$', 'timecard.views.update_file_description_for_empty_project', name='multi'),
    url(r'^update_file_description_for_real_project$', 'timecard.views.update_file_description_for_real_project', name='multi'),

    url(r'^get_all_uploaded_files_objectids$', 'timecard.views.get_all_uploaded_files_objectids', name='multi'),
    url(r'^get_all_uploaded_files_objectids_real_project$', 'timecard.views.get_all_uploaded_files_objectids_real_project', name='multi'),

    url(r'^add_language_to_user$', 'timecard.views.add_language_to_user', name='multi'),
    url(r'^update_user_language$', 'timecard.views.update_user_language', name='multi'),
    url(r'^get_all_user_languages$', 'timecard.views.get_all_user_languages', name='multi'),
    url(r'^remove_user_language$', 'timecard.views.remove_user_language', name='multi'),
    url(r'^block_language_updating$', 'timecard.views.block_language_updating', name='multi'),
    url(r'^unblock_language_updating$', 'timecard.views.unblock_language_updating', name='multi'),
    url(r'^add_skill_to_user$', 'timecard.views.add_skill_to_user', name='multi'),
    url(r'^update_skill_to_user$', 'timecard.views.update_skill_to_user', name='multi'),
    url(r'^remove_skill$', 'timecard.views.remove_skill', name='multi'),
    url(r'^block_editing_skills$', 'timecard.views.block_editing_skills', name='multi'),
    url(r'^unblock_editing_skills$', 'timecard.views.unblock_editing_skills', name='multi'),
    url(r'^showing_skill_on_main_page$', 'timecard.views.showing_skill_on_main_page', name='multi'),

    url(r'^add_position_to_user$', 'timecard.views.add_position_to_user', name='multi'),
    url(r'^remove_position_from_user$', 'timecard.views.remove_position_from_user', name='multi'),
    url(r'^show_position_on_main_page$', 'timecard.views.show_position_on_main_page', name='multi'),


    url(r'^close_project$', 'timecard.views.close_project', name='multi'),
    url(r'^add_project$', 'timecard.views.add_project', name='multi'),
    url(r'^update_project$', 'timecard.views.update_project', name='multi'),

    url(r'^update_work_period_on_project$', 'timecard.views.update_work_period_on_project', name='multi'),

    # url(r'^admin/', include(admin.site.urls)),

# [start]: it's for django_multiuploader_demo
    (r'^projects-create_new-delete_attached_file/(\d+)/$', multiuploader_delete),
    url(r'^projects-create_new-image_view/$', 'django_multiuploader_demo.multiuploader.views.image_view', name='main'),
    url(r'^projects-upload-files-to-temp-project/$', 'timecard.views.projects_upload_files_to_temp_project', name='multi'),
    url(r'^projects-upload-files-to-real-project/$', 'timecard.views.projects_upload_files_to_real_project', name='multi'),
# [end]: it's for django_multiuploader_demo
)

urlpatterns += staticfiles_urlpatterns()
