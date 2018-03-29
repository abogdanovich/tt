# from django.conf.urls.defaults import patterns, url
from django.conf.urls import patterns, url



urlpatterns = patterns('timecard.views',


    url (r'^$', 'main'),
    url (r'^login/$','login'),          #login page
    url (r'^logout/$','logout'),        #logout page
    url (r'^main/$','main', name="tt_main"),            #main page
    url (r'^personal/$','personal'),    #personal page
    url (r'^spam/$','spam'),            #spam page
    url (r'^settings/$','settings', name="tt_settings"),    #settings page
    url (r'^admin/$','admin'),          #admin page
    url (r'^events/$','events'),        #sevents page
    url (r'^teams/$','teams'),          #teams page
    url (r'^duty/$','duty'),            #duty page
    url (r'^projects/$','projects'),    #projects page
    url (r'^project/$','project'),
    url (r'^my_projects/$','my_projects'),

    url (r'^reservation/$','reservation'),      #devices page

    url (r'^report_user/$','report_user'),  #personal time report
    url (r'^report_time/$','report_time'), # general office reports
    url (r'^user_requests/$','user_requests'),#time report for gomel users
    url (r'^reports/$','reports'),           # page to view employee reports



)

urlpatterns +=patterns('timecard.ajax',
    url (r'^upload_logo/$','upload_logo'),
)
