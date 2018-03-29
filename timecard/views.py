# -*- coding: utf-8 -*-
#########################################################################
# TimeCard views module
# author Alex Bogdanovich
# 2012
#########################################################################
from django.core.context_processors import request
from app_classes.switch import switch

from ttk import _dict_from_tcltuple

from timecard.models import User, UserTime, UserPost, UserPostComment, UserDepartament, UserMissedHours, Projects,\
    CalendarDaysOff, Reports, Votes, ProjectThread,Offices, UserProfession, UserRoles, Reservation_Objects, \
    Reservation_Categories, Reservation_History
# from timecard.models import HumbleDoc
from timecard.models import ProjectAppendedEmployeeDoc


# from app_models.project_appended_employee_role import ProjectAppendedEmployeeRoleDoc
from timecard.models import ProjectAppendedEmployeeRoleDoc

from timecard.app_models.project_appended_files_doc import ProjectAppendedFilesDoc
from timecard.app_models.timecard_user import TimecardUser
from timecard.app_models.timecard_projects import TimecardProjects
from timecard.app_models.timecard_user_skill_tag_id import TimecardUserSkillTagId
from timecard.app_models.timecard_positions import TimecardPositions
from timecard.app_models.timecard_users_positions import TimecardUsersPositions


from timecard.models import MyDB

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.core.paginator import InvalidPage
from django.core.paginator import EmptyPage
from timecard import utils, doctordog
from django import template
import logging
import datetime
from django.core.exceptions import ObjectDoesNotExist
import random
import operator
import logging
import pprint
from django.http import HttpResponse
import json
from app_classes.MyLog import MyLog
from django.core.urlresolvers import resolve
from datetime import date

#########################################################################
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from models import Image
from django.core.files.uploadedfile import UploadedFile
from django.template import RequestContext
#importing json parser to generate plugin friendly json response
# from django.utils import simplejson
import json

#for generating thumbnails
#sorl-thumbnails must be installed and properly configured
from sorl.thumbnail import get_thumbnail
from django.views.decorators.csrf import csrf_exempt
import logging
import collections
log = logging
#########################################################################
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
#########################################################################
from timecard.app_models.timecard_customers import TimecardCustomers
from timecard.app_models.timecard_temp_projects import TimecardTempProjects
from timecard.app_models.timecard_users_languages import TimecardUsersLanguages
from timecard.app_models.timecard_languages import TimecardLanguages
from timecard.app_models.timecard_offices import TimecardOffices
from timecard.app_models.timecard_language_skills import TimecardLanguageSkills
from timecard.app_models.timecard_skill_tags import TimecardSkillTags


from timecard.app_models.timecard_skills import TimecardSkills
from timecard.app_models.timecard_users_skills import TimecardUsersSkills
from timecard.app_models.timecard_userprojectassignments import TimecardUserprojectassignments

from bson.objectid import ObjectId
from timecard.app_classes.MyDate import *

import datetime
import time

# my template loading section | modules
template.add_to_builtins('timecard.templatetags.calendar')
template.add_to_builtins('timecard.templatetags.user_info')
template.add_to_builtins('timecard.templatetags.currency')
template.add_to_builtins('timecard.templatetags.weather')
template.add_to_builtins('timecard.templatetags.bash')
template.add_to_builtins('timecard.templatetags.menu')
template.add_to_builtins('timecard.templatetags.truncatechars')
template.add_to_builtins('timecard.templatetags.duty_user')
template.add_to_builtins('timecard.templatetags.spam_module')
template.add_to_builtins('timecard.templatetags.voting')
template.add_to_builtins('timecard.templatetags.check_user_provide_full_info')
template.add_to_builtins('timecard.templatetags.hb_informer')
template.add_to_builtins('timecard.templatetags.who_was_last')

#####################################################

#set page name for top menu selection

def set_menu(request, value):
    request.session['page'] = value
    return request.session['page']

#####################################################

@utils.login_required
@utils.check_access_level([0,2,3,4])
@utils.reporting_conditions_check
def report_user(request):
    """
    That is a view function to initially draw report_user.html
    """
    import time
    set_menu(request,'report_user')

    # user = User.objects.get(id=int(request.session['uid']))
    user = TimecardUser().me(int(request.session['uid']))

    custom_CSS = utils.change_css_on_some_event(user)
    timeshift = int(Offices.objects.get(short_name=user.office).time_shift)
    NOW = int(round(time.time())) + timeshift - 3*3600 #we subtract 3 hours because server is in +3 GMT time zone
    report_year = time.strftime('%Y', time.gmtime(NOW))
    report_week = time.strftime('%W', time.gmtime(NOW))

    # now we can get the first and the last day in current week
    first_day_this_week = int(time.mktime(time.strptime(report_year + ' ' + report_week + ' 1', '%Y %W %w'))) - 3 * 3600# 1- monday
    last_day_this_week = int(time.mktime(time.strptime(report_year + ' ' + report_week + ' 0', '%Y %W %w'))) - 3 * 3600# 0 - sunday

    # now we have to find the estimated time of work hours per current week
    this_week_holidays = CalendarDaysOff.objects.filter(office=user.office, date__range=(first_day_this_week,last_day_this_week)).count()
    work_hours = 56 - this_week_holidays * 8 #and we finally get this week work hours
    my_this_week_reports = Reports.objects.filter(week=report_week, year=report_year, user_id=user.id).order_by('project_name')

    # if there is any reports to show
    reports_to_show= False
    if my_this_week_reports:
        reports_to_show =True
    # if these reports have 'overtime' flag
    overtime = False
    overtimed_hours = 0
    if my_this_week_reports.exclude(overtimed =0):
        overtime = True
        overtimed_hours =sum(my_this_week_reports.values_list('hours',flat = True).distinct())
    # if we delete any reports
    if request.method == 'GET' and 'del_report' in request.GET:
        report_id = request.GET['del_report']
        report_to_delete = Reports.objects.get(id=report_id)
        report_to_delete.delete()
        utils.check_overtime(report_to_delete.week,report_to_delete.year, report_to_delete.user_id, work_hours)
        return redirect('/report_user/')
    # get the list of assigned projects
    projects_assigned = ProjectThread.objects.filter(user_id = user.id, who_unassigned = '').values_list('project_id', flat=True).distinct()
    d = dict(request = request, projects_involved_in = Projects.objects.filter(id__in =projects_assigned, project_opened = 1).order_by('project_name'),
        user = user, my_this_week_reports =my_this_week_reports, reports_to_show = reports_to_show, holidays = this_week_holidays,
        work_hours = work_hours, overtime = overtime, overtimed_hours = overtimed_hours, custom_CSS=custom_CSS)
    return render_to_response('timecard/report_user.html', d, context_instance=RequestContext(request))
###########################################################################
@utils.login_required
@utils.check_access_level([1,3,4])
def reports(request):
    """
    That is a view function to initially draw reports.html
    """
    import time
    report_week=datetime.date.today().isocalendar()[1]
    report_year=datetime.date.today().strftime("%Y")
    # we have to know the estimated time of work hours per current week
    holidays = 0# this value is a quantity of days_off in this week
    YW = str(report_year)+"/"+str(report_week) # format is 'year/week' like '2012/45'
    all_days_off = CalendarDaysOff.objects.all()
    for day_off in all_days_off:
        if time.strftime('%Y/%W', time.gmtime(day_off.date + 3600*24)) == YW:
            # if in this week is any day off
            holidays += 1# we have a day off in this week
    work_hours = 56 - holidays*8
    set_menu(request,'reports')
    # user = User.objects.get(id=int(request.session['uid']))
    user = TimecardUser().me(int(request.session['uid']))
    custom_CSS = utils.change_css_on_some_event(user)
    reports = Reports.objects.all().order_by("-id")
    users = User.objects.all()
    projects_with_reports = Reports.objects.values_list('project_name', flat=True).order_by('project_name').distinct()
    # now we want to now which projects are still opened and which are closed
    reports_dict={}
    for i in projects_with_reports:
        project = Projects.objects.get(project_name = i)
        if project.project_opened == 1:
            reports_dict.update({i:1})
        else:
            reports_dict.update({i:0})
    d = dict(request = request, reports = reports, user=user, work_hours = work_hours,
             users = users, reports_dict = reports_dict,custom_CSS=custom_CSS )
    return render_to_response('timecard/reports.html', d, context_instance=RequestContext(request))
###########################################################################
@utils.login_required
@utils.check_access_level([1,3,4])
def report_time(request):
    l = MyLog().l()
    #first we have to know the years of posted time reports
    import time
    # user = User.objects.get(id=int(request.session['uid']))
    user = TimecardUser().me(int(request.session['uid']))
    # l(user, 'user')
    custom_CSS = utils.change_css_on_some_event(user)
    # l(custom_CSS, 'custom_CSS')
    first_report = list (UserTime.objects.all()[:1])[0] #first record
    last_report =  UserTime.objects.latest('id') # last record
    first_year_report = int(time.strftime ('%Y', time.gmtime(first_report.time)))
    last_year_report = int(time.strftime ('%Y', time.gmtime(last_report.time)))
    year_range = [first_year_report]
    current_year = first_year_report
    # l(current_year, 'current_year')
    while True:
        current_year +=1
        if current_year > last_year_report:
            break
        else:
            year_range.append(current_year)
    #we will show only the last five years
    year_range = year_range[-5:]
    ########
    set_menu(request, "report_time")
    # boss_user = User.objects.get(id=int(request.session['uid']))
    boss_user = TimecardUser().me(int(request.session['uid']))
    # l(boss_user['office'], 'boss_user[office]')

    boss_office = boss_user['office']
    ########
    l(boss_office, 'boss_office')
    # this is used for page redrawing. we have to draw links on the page according to the chosen year
    if request.method == "GET" and "selected_year" in request.GET:
        sel_year = int(request.GET['selected_year'])
        user_list = User.objects.filter(office=boss_office).order_by("surname").order_by("name")
        sel_month = datetime.date.today().month
        reported_month = "%s-%s" % (sel_year, sel_month)
        users = []
        for u in user_list:
            utime = utils.convert_seconds(utils.calc_total_month_hours(u.id, sel_month, sel_year))
            users.append({'name': u.name, 'surname': u.surname, 'utime': utime, 'userid': u.id})
        users.sort(key=operator.itemgetter('name', 'surname'))
        d = dict(user_list=user_list, request=request, users=users, reported_month=reported_month, sel_month=sel_month,
            sel_year = sel_year, year_range = year_range, custom_CSS = custom_CSS)
        return render_to_response('timecard/report_time.html', d, context_instance=RequestContext(request))
    ######

    if request.method == "GET" and "user_report" in request.GET:
        try:

            date = request.GET['user_report_date'].split("-")
            month = int(date[1])
            year = int(date[0])

            user_time = utils.show_user_month_hours(int(request.GET['user_report']), month, year)
            # user = User.objects.get(id=int(request.GET['user_report']))
            user = TimecardUser().me(int(request.GET['user_report']))

            user_month_seconds = utils.calc_total_month_hours(int(request.GET['user_report']), month, year)
            user_month_time = utils.convert_seconds(user_month_seconds)
            reported_user = "%s %s" % (user.name, user.surname)

            generated_report_month = "%s - %02d" % (year, month)

            d = dict(user_time=user_time, user_month_time=user_month_time, request=request, user=user,
                generated_report=True, generated_report_month=generated_report_month, reported_user=reported_user, custom_CSS=custom_CSS)
            return render_to_response('timecard/personal.html', d, context_instance=RequestContext(request))
        except:
            # something isn't ok :( - maybe user isn't in base
            return redirect('/report_time/')

    elif request.method == "GET" and "selected_month" in request.GET:

        sel_month = int(request.GET['selected_month'])
        sel_year = int (request.GET['year'])
        user_list = User.objects.filter(office=boss_office).order_by("surname").order_by("name")
        users = []
        reported_month= "%s-%s" % (sel_year, sel_month)
        for u in user_list:
            utime = utils.convert_seconds(utils.calc_total_month_hours(u.id, sel_month, sel_year))
            users.append({'name': u.name, 'surname': u.surname, 'utime': utime, 'userid': u.id})
        users.sort(key=operator.itemgetter('name', 'surname'))
        d = dict(user_list=user_list, request=request, users=users, reported_month=reported_month, sel_month=sel_month,
            sel_year = sel_year , year_range = year_range, custom_CSS = custom_CSS)

        return render_to_response('timecard/report_time.html', d, context_instance=RequestContext(request))

    elif request.method == "GET" and "edit_u_hours" in request.GET:

        #set time correction mode
        time_correction_mode = True
        #set date
        time_correction_date = request.GET['date']
        #set correction msg
        time_correction_umess = u"Редактирование отработанного времени за отдельный день"

        time_correction_user = request.GET['user']

        #get all hours for the selected day
        #print "user: %s" % (euser.user)
        date = time_correction_date.split("-") #date[0] - YY | #date[1]- mm | #date[2] - dd
        missed_hours_list = utils.get_selected_day_hours(int(time_correction_user), int(date[0]), int(date[1]), int(date[2]))
        month = int(date[1])
        year = int(date[0])

        user_time = utils.show_user_month_hours(int(time_correction_user), month, year)
        # user = User.objects.get(id=int(time_correction_user))
        user = TimecardUser().me(int(time_correction_user))

        office_city = user.office

        user_month_seconds = utils.calc_total_month_hours(int(time_correction_user), month, year)
        user_month_time = utils.convert_seconds(user_month_seconds)

        d = dict(
                user_time=user_time,
                user_month_time=user_month_time,
                request=request,
                user=user,
                time_correction_mode=time_correction_mode,
                time_correction_date=time_correction_date,
                time_correction_umess=time_correction_umess,
                missed_hours_list=missed_hours_list,
                time_correction_user=time_correction_user,
                disable_approve_button = True,
                custom_CSS = custom_CSS,
                office_city = office_city

            )

        return render_to_response('timecard/personal.html', d, context_instance=RequestContext(request))

    else:


        sel_month = datetime.date.today().month
        sel_year = datetime.date.today().year
        user_list = User.objects.filter(office=boss_office).order_by("surname").order_by("name")
        users = []
        reported_month= "%s-%s" % (sel_year, sel_month)


        for u in user_list:
            utime = utils.convert_seconds(utils.calc_total_month_hours(u.id, sel_month, sel_year))

            users.append({'name':u.name, 'surname':u.surname, 'utime': utime, 'userid': u.id})

        users.sort(key=operator.itemgetter('name', 'surname'))

        d = dict(user_list=user_list, request=request, users=users, reported_month=reported_month, sel_month=sel_month,
            sel_year = sel_year, year_range = year_range,custom_CSS = custom_CSS)

        return render_to_response('timecard/report_time.html', d, context_instance=RequestContext(request))


@utils.login_required
@utils.check_access_level([1,3])
def user_requests(request):
    set_menu(request, "user_requests")
    # user = User.objects.get(id=int(request.session['uid']))
    userTimeCard = TimecardUser().me(int(request.session['uid']))
    custom_CSS = utils.change_css_on_some_event(userTimeCard)
    b = request.method == "GET" and "missed_id" in request.GET
    if b:
        try:
            month = datetime.date.today().month
            year = datetime.date.today().year
            euser = UserMissedHours.objects.get(id=int(request.GET['missed_id']))
            if euser.lock_person != "0":
                # editor = User.objects.get(id=int(request.session['uid']))
                editor = TimecardUser().me(int(request.session['uid']))
                if euser.lock_person != editor.avator:
                    return redirect('/user_requests/')

            user_time = utils.show_user_month_hours(euser.user, month, year)
            # user = User.objects.get(id=euser.user)
            userTimeCard = TimecardUser().me(euser.user)

            user_month_seconds = utils.calc_total_month_hours(euser.user, datetime.date.today().month, year)
            user_month_time = utils.convert_seconds(user_month_seconds)

            #set time correction mode
            time_correction_mode = True
            #set time correction id record
            time_correction_record = euser.id
            #set date
            time_correction_date = euser.date
            #set correction msg
            time_correction_umess = euser.umess

            time_correction_user = euser.user

            #set editor in db for other
            # editor = User.objects.get(id=int(request.session['uid']))
            editor = TimecardUser().me(int(request.session['uid']))


            euser.lock_person = editor.avator
            euser.save()

            #get all hours for the selected day
            #print "user: %s" % (euser.user)
            date = time_correction_date.split("-") #date[0] - YY | #date[1]- mm | #date[2] - dd
            missed_hours_list = utils.get_selected_day_hours(euser.user, int(date[0]), int(date[1]), int(date[2]))



            d = dict(user_time=user_time, user_month_time=user_month_time, request=request, user=userTimeCard,
                     time_correction_mode=True, time_correction_date=time_correction_date,
                     time_correction_umess=time_correction_umess, time_correction_record=time_correction_record,
                     missed_hours_list=missed_hours_list, time_correction_user=time_correction_user, custom_CSS = custom_CSS)
            return render_to_response('timecard/personal.html', d, context_instance=RequestContext(request))
        except Exception,e:
            logging.debug('user_request_error: '+str(e))
            return redirect('/user_requests/')
    else:

        # editor = User.objects.get(id=int(request.session['uid']))
        editor = TimecardUser().me(int(request.session['uid']))
        author_avator = editor['avator']
        users_from_whom_show_requests = User.objects.filter(office = editor['office']).values_list('id', flat=True).distinct()
        user_requests = UserMissedHours.objects.filter(status = 0, user__in=users_from_whom_show_requests)
        d = dict(request=request, user_requests=user_requests, author_avator=author_avator, custom_CSS = custom_CSS)

        return render_to_response('timecard/user_requests.html', d, context_instance=RequestContext(request))

###########################################################################
@utils.login_required
def teams(request):
    set_menu(request, "teams")
    # user = User.objects.get(id=int(request.session['uid']))
    user = TimecardUser().me(int(request.session['uid']))
    custom_CSS = utils.change_css_on_some_event(user)
    users = User.objects.all().order_by('dep','name','surname') #UserDepartament
    status_list = []
    #prepare the dict of statuses
    for user in users:
        user_status = [user.id, user.status]
        status_list.append(user_status)
    status = dict(status_list)
    offices=Offices.objects.all()
    d = dict(request = request, users = users, offices = offices, status = status, custom_CSS = custom_CSS)

    return render_to_response('timecard/teams.html', d, context_instance=RequestContext(request))
###########################################################################

@utils.login_required
def reservation(request):
    set_menu(request, "reservation")
    # user = User.objects.get(id=int(request.session['uid']))
    userTimeCard = TimecardUser().me(int(request.session['uid']))
    custom_CSS = utils.change_css_on_some_event(userTimeCard)
    categories = Reservation_Categories.objects.filter(office=userTimeCard['office'])
    objects = Reservation_Objects.objects.filter(category__office=userTimeCard['office'])
    objects_with_history = Reservation_History.objects.filter(obj__category__office=userTimeCard['office']).values_list('obj__name', flat=True).distinct()
    categories_with_objects = Reservation_Objects.objects.filter(category__office=userTimeCard['office']).values_list('category__name', flat=True).distinct()
    categories_with_objects_with_history = Reservation_History.objects.filter(obj__category__office=userTimeCard['office']).values_list('obj__category__name', flat=True).distinct()
    history = Reservation_History.objects.order_by('-id')

    d = dict(request=request, user=userTimeCard, custom_CSS=custom_CSS, categories=categories, objects=objects,
             c_w_o=categories_with_objects, c_w_o_w_h=categories_with_objects_with_history, o_w_h=objects_with_history,
             history=history)

    if request.method == 'GET':
        if 'del_object' in request.GET:
            #we have to clean history before deleting object's data
            object_to_delete = Reservation_Objects.objects.get(id=int(request.GET['del_object']))
            Reservation_History.objects.filter(obj__id=object_to_delete.id).delete()
            object_to_delete.delete()
            return render_to_response('timecard/reservation.html', d, context_instance=RequestContext(request))
        if 'del_category' in request.GET:
            #first we have to delete all the history about object activity, objects within category, and after that only
            # at the end we will delete category itself
            category_to_delete = Reservation_Categories.objects.get(id=int(request.GET['del_category']))
            Reservation_History.objects.filter(obj__category__id=category_to_delete.id).delete()
            Reservation_Objects.objects.filter(category__id=category_to_delete.id).delete()
            category_to_delete.delete()
            return render_to_response('timecard/reservation.html', d, context_instance=RequestContext(request))
        if 'occupy' in request.GET:
            object_to_occupy = Reservation_Objects.objects.get(id=int(request.GET['occupy']))
            # before occupying we have to check that actually object is available
            if object_to_occupy.is_avaliable == True:
                object_to_occupy.user = userTimeCard
                object_to_occupy.is_avaliable = False
                object_to_occupy.save()
                event = Reservation_History(obj=object_to_occupy, status=False, user=(userTimeCard['surname'] + ' ' + userTimeCard['name']))
                event.save()
                #we have to limit size of journal to 100 records for every object
                if Reservation_History.objects.filter(obj=object_to_occupy).count()>100:
                    last_record_we_have_to_delete = Reservation_History.objects.filter(obj=object_to_occupy).reverse()[0]
                    last_record_we_have_to_delete.delete()
        if 'free' in request.GET:
            object_to_free = Reservation_Objects.objects.get(id=int(request.GET['free']))
            # before freeing we have to check that object is actually occupied with current user
            if object_to_free.is_avaliable == False and object_to_free.user == userTimeCard:
                object_to_free.user = userTimeCard
                object_to_free.is_avaliable = True
                object_to_free.save()
                event = Reservation_History(obj=object_to_free, status=True, user=(userTimeCard['surname'] + ' ' + userTimeCard['name']))
                event.save()
                #we have to limit size of journal to 100 records for every object
                if Reservation_History.objects.filter(obj=object_to_free).count()>100:
                    last_record_we_have_to_delete = Reservation_History.objects.filter(obj=object_to_free).reverse()[0]
                    last_record_we_have_to_delete.delete()
    if request.method == 'POST':
        if 'new_category' in request.POST:
            new_category = request.POST['new_category']
            if new_category:
                #first we must check all the categories for the same office are unique
                if not Reservation_Categories.objects.filter(name=new_category, office=userTimeCard['office']):
                    Reservation_Categories(name=new_category, office=userTimeCard['office']).save()
                    return render_to_response('timecard/reservation.html', d, context_instance=RequestContext(request))
                else:
                    message = u"Название категории должно быть уникальным"
                    d.update(message1=message)
                    return render_to_response('timecard/reservation.html', d, context_instance=RequestContext(request))
            else:
                message = u"Введите название для категории"
                d.update(message1=message)
                return render_to_response('timecard/reservation.html', d, context_instance=RequestContext(request))
        if 'new_object' in request.POST:
            new_object = request.POST['new_object']
            if new_object:
                #first we must check that all the objects within same category has unique names
                category = Reservation_Categories.objects.filter(office=userTimeCard['office']).get(name=request.POST['select_category'])
                if not Reservation_Objects.objects.filter(category=category, name=new_object):
                    Reservation_Objects(name=new_object, category=category, user=userTimeCard).save()
                    return render_to_response('timecard/reservation.html', d, context_instance=RequestContext(request))
                else:
                    message = u"Название объектов в пределах одной категории должно быть уникальным"
                    d.update(message2=message)
                    return render_to_response('timecard/reservation.html', d, context_instance=RequestContext(request))
            else:
                message = u"Введите название объекта"
                d.update(message2=message)
                return render_to_response('timecard/reservation.html', d, context_instance=RequestContext(request))
    return render_to_response('timecard/reservation.html', d, context_instance=RequestContext(request))


#############################################################################



@utils.login_required
def main(request):
    l = MyLog().l()
    set_menu(request, "main")
    profile = "default"
    id=int(request.session['uid'])
    timecardUser = TimecardUser()
    user = timecardUser.me(id)

    custom_CSS = utils.change_css_on_some_event(user)
    user_browser = utils.getUA(request) #get UA
    utils.updateUA(user['id'], user_browser) #update UA

    #profile
    if request.method == 'GET' and 'profile' in request.GET:
        try:
            #if user exist then send this id
            # user = User.objects.get(id=int(request.GET['profile']))
            user = TimecardUser().me(int(request.GET['profile']))
            profile = user['id']
        except:
            #if user isn't exist - then send default cmd string
            profile = "default"

    # users = User.objects.all().order_by('name','surname')
    users = TimecardUser().getAllUsers(order_by = 'name')
    skills = TimecardSkills().getAll()
    usersSkillsForMainPage = TimecardUsersSkills().getForMainPageByUserId(user_id = id)
    usersSkillsForMainPage = my_join(usersSkillsForMainPage, skills, 'skill_id', '_id', 'skill_descr__', 'one_to_one')
    users = my_join(users, usersSkillsForMainPage, 'id', 'user_id', 'user_skill__')
    offices=Offices.objects.all()

    d = dict(
                request=request,
                users=users,
                offices = offices,
                custom_CSS = custom_CSS
        )

    if profile or profile == "default":
        #if default or we have a real profile id then send to template
        d['profile'] = profile
        d['user'] = user

    return render_to_response('timecard/main.html', d, context_instance=RequestContext(request))

###########################################################################

@utils.login_required
def duty(request):

    set_menu(request, "duty")
    # user = User.objects.get(id=int(request.session['uid']))
    userTimecard = TimecardUser().me(int(request.session['uid']))
    custom_CSS = utils.change_css_on_some_event(userTimecard)
    month = datetime.date.today().month # current
    year = datetime.date.today().year # current
    duty_list = utils.show_duty_month_users(year, month, userTimecard['office'])
    #get next  month
    if month == 12:
        month_next = 1
        year = datetime.date.today().year + 1 # current

    else:
        month_next = datetime.date.today().month + 1 # next month
        year = datetime.date.today().year

    duty_list_next = []
    if userTimecard['login'] == "ksyomushkina" \
            or userTimecard['login'] == "abogdanovich" \
            or userTimecard['login'] == "asnopchenko" \
            or userTimecard['dep'] == "HRM":
        duty_list_next = utils.show_duty_month_users(year, month_next, userTimecard['office'])

    d = dict(request=request,
             duty_list=duty_list,
             duty_list_next=duty_list_next,
             month=month,
             month_next=month_next,
             user=userTimecard,
             custom_CSS = custom_CSS
    )
    return render_to_response('timecard/duty.html', d, context_instance=RequestContext(request))
###########################################################################

def logout(request):
    error_message = ""
    if request.method == 'GET' and 'logout' in request.GET:
        request.session.flush()
        error_message = u"Вы вышли из TimeTrack"
    d = dict(error_message=error_message)
    return render_to_response('timecard/login.html', d, context_instance=RequestContext(request))

###########################################################################

def login(request):
    try:
        if request.session['uid']:
            return redirect('/main/')
        error_message=''
        #error_message = u"Введите логин и пароль от своей учетной записи"
        if request.method == 'POST' and 'trylogin' in request.POST:
        #check if we have LDAP account
            if utils.ldap_check(request, request.POST['userlogin'], request.POST['userpassword']):
                #need to check TT account if exists
                if utils.tt_accountcheck(request, request.POST['userlogin']):
                #save into DJANGO session as:
                    return redirect('/main/')
                else:
                    error_message = u"Вам завели учетную запись в LDAP, но еще не завели в TimeCard! Обратитесь к администратору :)"
            else:
                error_message = u"Не удалось авторизовать вас через LDAP! В LDAP или отсутствует запись для вас, или указан другой пароль. Обратитесь к администратору :)"

        d = dict(error_message=error_message)
        return render_to_response('timecard/login.html', d, context_instance=RequestContext(request))

    except UnicodeEncodeError:
        error_message = u"Используйте только латинские символы!"
        d = dict(error_message=error_message)
        return render_to_response('timecard/login.html', d, context_instance=RequestContext(request))
    except KeyError:
        error_message = u"Введите логин и пароль"
        #error_message = u"Введите логин и пароль от своей учетной записи"
        if request.method == 'POST' and 'trylogin' in request.POST:
        #check if we have LDAP account
            if utils.ldap_check(request, request.POST['userlogin'], request.POST['userpassword']):
                #need to check TT account if exists
                if utils.tt_accountcheck(request, request.POST['userlogin']):
                #save into DJANGO session as:
                    return redirect('/main/')
                else:
                    error_message = u"Вам завели учетную запись в LDAP, но еще не завели в TimeCard! Обратитесь к администратору :)"
            else:
                error_message = u"!!Не удалось авторизовать вас через LDAP! В LDAP или отсутствует запись для вас, или указан другой пароль. Обратитесь к администратору :)"

        d = dict(error_message=error_message)
        return render_to_response('timecard/login.html', d, context_instance=RequestContext(request))
###########################################################################

@utils.login_required
def events(request):

    set_menu(request, "events")
    # user = User.objects.get(id=int(request.session['uid']))
    user = TimecardUser().me(int(request.session['uid']))
    custom_CSS = utils.change_css_on_some_event(user)
    error_message = ""
    user_hb_list = []
    utils.draw_office_browsers()
    if request.method == 'GET' and 'day_events' in request.GET:
        user_hb_list = utils.get_hb_list(request.GET['day_events'])
    gday = request.GET['day_events'][3:5]
    #draw statistic
    userlist = User.objects.all()
    utils.draw_office_visiting(userlist, gday)
    d = dict(error_message=error_message, user_hb_list=user_hb_list, request=request, day=request.GET['day_events'],
             custom_CSS = custom_CSS)
    return render_to_response('timecard/events.html', d, context_instance=RequestContext(request))
###########################################################################

@utils.login_required
@utils.check_access_level([0,2,3,4])
def personal(request):
    l = MyLog().l()
    p = MyLog().p()
    set_menu(request, "personal")
    year = datetime.date.today().year
    month = datetime.date.today().month
    userId = int(request.session['uid'])
    user = TimecardUser().me(userId)
    custom_CSS = utils.change_css_on_some_event(user)
    user_time = utils.show_user_month_hours(int(request.session['uid']), month, year)
    user_month_seconds = utils.calc_total_month_hours(int(request.session['uid']), month, year)
    user_month_time = utils.convert_seconds(user_month_seconds)
    user_state = utils.get_user_state(user['id'])

    if request.method == 'POST' and 'user_time_off' in request.POST:
        #logout user
        utils.save_user_time(user['id'])
        user.leaveWorkPlace(userId)
        return redirect('/personal/')

    elif request.method == 'POST' and 'user_time_on' in request.POST:
        #login user
        utils.save_user_time(user['id'])
        user.cameToWorkPlace(userId)
        return redirect('/personal/')

    else:
        d = dict(
            user_time=user_time,
            user_month_time=user_month_time,
            request=request,
            user=user,
            user_state=user_state,
            custom_CSS = custom_CSS
        )
        return render_to_response(
            'timecard/personal.html',
            d,
            context_instance=RequestContext(request)
        )
###########################################################################

###########################################################################
@utils.login_required
@utils.check_access_level([3,4])
def project(request):
    l = MyLog().l()
    p = MyLog().p()
    d = {}
    set_menu(request, "project")
    listCustomers = TimecardCustomers().getAllCustomers()

    if 'project_id' in request.GET:
        project_id = request.GET['project_id']

        appliedEmployees, appliedEmployeeIds, notesUsers = \
            ProjectAppendedEmployeeDoc().getAppliedEmployeesToRealProjectByUserId(project_id)
        appliedEmployees = my_join(appliedEmployees, notesUsers, 'id', 'employeeId', 'role_info__')
        projectInfo = TimecardProjects().getProjectById(project_id = project_id)
        projectInfo = addObjectID(projectInfo)

        if isinstance(projectInfo, collections.Iterable):
            if 'customer_id' in projectInfo:
                if isinstance(listCustomers, collections.Iterable):
                    for customer in listCustomers:
                        if isinstance(customer, collections.Iterable):
                            if 'customer_id' in customer:

                                strCustomerId = str(customer['customer_id'])
                                strProjectInfoCustomerId = str(projectInfo['customer_id'])

                                if strCustomerId == strProjectInfoCustomerId:
                                    if not 'selected' in customer:
                                        customer['selected'] = True

        users_ = TimecardUser().getAllUsers( order_by = 'surname' )
        notAppliedOnProjectEmployee = TimecardUser().getNotAppliedOnProjectEmployee(users_, appliedEmployeeIds)
        files = ProjectAppendedFilesDoc().getFilesAppendedOnRealProject(project_id)
        d = dict (
            appliedEmployees = appliedEmployees,
            appliedEmployeeIds = appliedEmployeeIds,
            notesUsers = notesUsers,
            users_ = users_,
            users = users_,
            notAppliedOnProjectEmployee = notAppliedOnProjectEmployee,
            listCustomers = listCustomers,
            projectInfo = projectInfo,
            files = files,

        )
    return render_to_response('timecard/project.html', d, context_instance=RequestContext(request))






###########################################################################
@utils.login_required
@utils.check_access_level([3,4])
def projects(request):
    l = MyLog().l()
    p = MyLog().p()
    listCustomers = TimecardCustomers().getAllCustomers()
    appliedEmployees = None
    userId = int(request.session['uid'])
    tempProjectId = TimecardTempProjects().getTempProjectIdByUserId(userId) # str
    projectAppendedEmployeeDoc = ProjectAppendedEmployeeDoc()
    timecardUser = TimecardUser()
    projectAppendedEmployeeRoleDoc = ProjectAppendedEmployeeRoleDoc()
    employeesRolesOnProject = projectAppendedEmployeeRoleDoc.getAllUsersAppendedOnEmptyProject(userId)
    appliedEmployees, appliedEmployeeIds, notesUsers = projectAppendedEmployeeDoc.getAppliedEmployeesToTempProjectByUserId(userId)
    appliedEmployees = projectAppendedEmployeeDoc.addRoles(appliedEmployees, employeesRolesOnProject)
    me = timecardUser.me(userId)  # TODO: We get Information about current user such way. NO MORE OLD STYLE: [ me = User.objects.get (id = userId) ]
    users_ = timecardUser.getAllUsers( order_by = 'surname' )
    TimecardTempProjects().initTempProjectsForUsers(users_)
    notAppliedOnProjectEmployee = timecardUser.getNotAppliedOnProjectEmployee(users_, appliedEmployeeIds)
    projectAppendedEmployee = projectAppendedEmployeeDoc.getProjectAppendedEmployee(userId)
    projectAppendedFilesDoc = ProjectAppendedFilesDoc()
    files = projectAppendedFilesDoc.getFilesAppendedOnEmptyProject(userId)
    set_menu(request, "projects")
    users = User.objects.all().order_by('dep','name','surname') #UserDepartament
    custom_CSS = utils.change_css_on_some_event(me)
    today = datetime.date.today()
    projects = TimecardProjects().getAllProjects(order_by = 'project_name')
    projects = addObjectIDs(projects)
    users = User.objects.all().order_by('surname')
    threads = ProjectThread.objects.all()
    assigned_projects=ProjectThread.objects.filter(who_unassigned = '').values_list('project_id', flat = True).distinct()

    if request.method == 'GET' and 'close_project' in request.GET:
        pid = request.GET['close_project']
        project = Projects.objects.get(id=pid)
        project.project_opened = 0
        project.save()
        return redirect('/projects/')

    # calculating all the hours per all the reports ever created
    projects_names = Projects.objects.values_list('project_name', flat = True).distinct()
    spent_hours_per_all_projects=[]
    for name in projects_names:
        spent_hours_per_project = sum(Reports.objects.filter(project_name = name).values_list('hours', flat = True))
        spent_hours_per_all_projects.append ([name, spent_hours_per_project])

    spent_hours_per_all_projects = dict (spent_hours_per_all_projects)
    deps = UserDepartament.objects.all()
    rolelist = UserRoles.objects.all()
    reports = Reports.objects.all()

    reports_ = dict(reports)
    m = str(datetime.datetime.now()).split(' ')
    _date = m[0].split('-')
    day = _date[2]
    month = _date[1]
    year = _date[0]

    d = dict(
        request = request,
        projects = projects,
        users = users,
        users_ = users_,
        threads = threads,
        today = today,
        deps = deps,
        assigned_projects = Projects.objects.filter(id__in = assigned_projects),
        me = me,
        rolelist = rolelist,
        spent_hours_per_all_projects = spent_hours_per_all_projects,
        reports = reports,
        custom_CSS = custom_CSS,
        projectAppendedEmployee = projectAppendedEmployee,
        appliedEmployees = appliedEmployees,
        notAppliedOnProjectEmployee = notAppliedOnProjectEmployee,
        employeesRolesOnProject = employeesRolesOnProject,
        files = files,
        listCustomers = listCustomers,
        date = str(day + '/' + month + '/' + year),
    )
    return render_to_response('timecard/projects.html', d, context_instance=RequestContext(request))


###########################################################################
@utils.login_required
def spam(request):
    l = MyLog().l()
    set_menu(request, "spam")
    # user = User.objects.get(id=int(request.session['uid']))
    userTimeCard = TimecardUser().me(int(request.session['uid']))
    custom_CSS = utils.change_css_on_some_event(userTimeCard)
    rand_exp_pic = random.randint(1, 5)
    utils.set_user_spam_counts(int(request.session['uid']))

    if request.method == 'GET' and 'spam' in request.GET:
        post_uid = request.GET['spam']
        try:
            # ttuser = User.objects.get(id=int(request.session['uid']))
            ttuser = TimecardUser().me(int(request.session['uid']))
            post = UserPost.objects.get(id=int(post_uid))
            #post user data
            # post_user = User.objects.get(id=int(post.author))
            post_user = TimecardUser().me(int(post.author))

            post_author_avator = post_user['avator']
            if post_author_avator == "":
                post_author_avator = "noavator.jpg"
            post_author_name = "%s %s" % (post_user['name'], post_user['surname'])

            #comments list
            comments = UserPostComment.objects.filter(post_id=int(post_uid)).order_by("created")
            comments_count = len(comments)
            comments_list = []

            if comments_count > 0:
                #prepare the list of dic of comments
                for rec in comments:
                    comment_item = {}
                    try:
                        # user = User.objects.get(id=int(rec.author))
                        user = TimecardUser().me(int(rec.author))

                        user_avator = user.avator
                        if user_avator == "":
                            user_avator = "noavator.jpg"
                        author_id = user.id
                        author_name = "%s %s" % (user['name'], user['surname'])

                    except ObjectDoesNotExist:
                        user_avator = "deleted_tt_user.png"
                        author_name = "Deleted TT user"

                    comment_item['id'] = rec.id
                    comment_item['body'] = rec.body
                    comment_item['author_avator'] = user_avator
                    comment_item['author_name'] = author_name
                    comment_item['author_id'] = author_id
                    comment_item['created'] = rec.created

                    #make the list of all comments for post
                    comments_list.append(comment_item)

                #group the list of comments by id
                comments_list_grouped = utils.group_list_spam(comments_list)

                d = dict(comments=comments_list_grouped,
                         post=post,
                         request=request,
                         post_author_avator=post_author_avator,
                         post_author_name=post_author_name,
                         user=ttuser,
                         custom_CSS = custom_CSS
                )
                return render_to_response(
                    'timecard/spam_comments.html',
                    d,
                    context_instance=RequestContext(request)
                )
            else:
                d = dict(
                        post=post,
                        request=request,
                        post_author_avator=post_author_avator,
                        post_author_name=post_author_name,
                        custom_CSS = custom_CSS
                )
                return render_to_response(
                    'timecard/spam_comments.html',
                    d,
                    context_instance=RequestContext(request)
                )

        except:
            return redirect('/spam/')

    elif request.method == 'POST' and 'add_newpost' in request.POST:
        post_body = request.POST['newpost']
        post_author = request.session['uid']
        # l(post_author, 'post_author')
        utils.save_spam_post(request, post_body, post_author)
        return redirect('/spam/')
    total_counts = UserPost.objects.all().count()#5:10]
    pages = total_counts / utils.SPAM_PAGE_MSG

    try:
        showpage = int(request.GET.get("page", '1'))
    except ValueError:
        showpage = 1

    page_start = showpage * utils.SPAM_PAGE_MSG - utils.SPAM_PAGE_MSG
    page_end = showpage * utils.SPAM_PAGE_MSG

    spam_list  = UserPost.objects.all().order_by("-created")[page_start:page_end]
    posts = UserPost.objects.all().order_by("-created")
    posts_list = []

    paginator = Paginator(posts, utils.SPAM_PAGE_MSG)
    try:
        page = int(request.GET.get("page", '1'))
    except ValueError:
        page = 1
    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)

    for rec in spam_list:
        spam = {}
        try:
            # user = User.objects.get(id=int(rec.author))
            user = TimecardUser().me(int(rec.author))

            user_avator = user['avator']
            if user_avator == "":
                user_avator = "noavator.jpg"
            author_id = rec.author
            author_name = "%s %s" % (user['name'], user['surname'])
        except ObjectDoesNotExist:
            user_avator = "deleted_tt_user.png"
            author_name = "Deleted TT user"

        comments = UserPostComment.objects.filter(post_id=rec.id).count()

        spam['id'] = rec.id
        spam['body'] = rec.body
        spam['author_avator'] = user_avator
        spam['author_id'] = author_id
        spam['author_name'] = author_name
        spam['comments'] = comments
        spam['created'] = rec.created

        posts_list.append(spam)

    # user = User.objects.get(id=int(request.session['uid']))
    user = TimecardUser().me(int(request.session['uid']))
    #group
    posts_list_grouped = utils.group_list_spam(posts_list)

    d = dict(posts=posts, request=request, posts_list=posts_list_grouped, rand_exp_pic=rand_exp_pic, user=user,
             custom_CSS = custom_CSS)

    return render_to_response('timecard/spam.html', d, context_instance=RequestContext(request))
###########################################################################

@utils.login_required
def settings(request):

    l = MyLog().l()
    p = MyLog().p()
    user_id = int(request.session['uid'])
    allPositions = TimecardPositions().getAll()
    usersPositions = TimecardUsersPositions().getByUserId(user_id = user_id)
    usersPositions = my_join(
        usersPositions,
        allPositions,
        str(TimecardUsersPositions.position_id_),
        str(TimecardPositions._id),
        'description__',
        'one_to_one'
    )
    notAppliedPositions = TimecardUsersPositions(
    ).clearListFromAppliedPositions(
        usersPositions = usersPositions,
        allPositions = allPositions
    )

    allSkills = TimecardSkills().getAll()
    allSkills = TimecardSkills().prepareForTemplate(allSkills = allSkills)

    usersSkills = TimecardUsersSkills().getByUserId(user_id = user_id)
    # FIXME: Method setNamesToSkills() depends on previous operations. SImply DON'T FIX place of this method
    usersSkills = TimecardUsersSkills().setNamesToSkills(usersSkills = usersSkills, allSkills = allSkills)
    notAppliedSkills = TimecardUsersSkills().clearListFromAppliedSkills(usersSkills = usersSkills, allSkills = allSkills)
    allLanguages = TimecardLanguages().getAll()
    allLanguages = TimecardLanguages().prepareForTemplate(allLanguages = allLanguages)
    set_menu(request, "settings")
    mod1_label = "show module"
    mod2_label = "show module"
    mod3_label = "show module"
    user = TimecardUser().me(user_id)

    custom_CSS = utils.change_css_on_some_event(user)
    m1 = utils.get_modules(user['id'], "mod1")
    if m1:
        mod1_label = "hide module"
    m2 = utils.get_modules(user['id'], "mod2")
    if m2:
        mod2_label = "hide module"
    m3 = utils.get_modules(user['id'], "mod3")
    if m3:
        mod3_label = "hide module"

    if user['avator'] == "":
        user_avator = "noavator.jpg"
    else:
        user_avator = user['avator']

    month_num = [u'%d' % x for x in range(1,13)]
    day_num = [u'%d' % x for x in range(1,32)]

    if request.method == 'GET' and 'drop_voice' in request.GET:
        # user_ = User.objects.get(id = request.GET['drop_voice'])
        user_ = TimecardUser().me( request.GET['drop_voice'])

        my_previous_choice = user_.voted
        my_voting = Votes.objects.filter(office=user_['office']).latest('id')

        if my_previous_choice == 1:
            my_voting.votes_yes -=1
            # now we have to extract uid from records about voting
            t = my_voting.votes_yes_who.split(' ')
            t.pop(t.index(str(user_['id'])))
            my_voting.votes_yes_who = ' '.join(t)
        if my_previous_choice == 2:
            my_voting.votes_no -=1
            t = my_voting.votes_no_who.split(' ')
            t.pop(t.index(str(user_['id'])))
            my_voting.votes_no_who = ' '.join(t)
        if my_previous_choice ==3:
            my_voting.votes_dontcare -=1
            t = my_voting.votes_dontcare_who.split(' ')
            t.pop(t.index(str(user_['id'])))
            my_voting.votes_dontcare_who = ' '.join(t)
        user_['voted'] = 0
        user_.my_save()
        my_voting.save()
        return redirect('/settings/')

    d = dict(
            request=request,
            user=user,
            user_avator=user_avator,
            month_num=month_num,
            day_num=day_num,
            mod1_label=mod1_label,
            mod2_label=mod2_label,
            mod3_label=mod3_label,
            custom_CSS = custom_CSS,
            allLanguages = allLanguages,
            allSkills = allSkills,
            usersSkills = usersSkills,
            notAppliedSkills = notAppliedSkills,
            notAppliedPositions = notAppliedPositions,
            usersPositions = usersPositions
    )
    return render_to_response('timecard/settings.html', d, context_instance=RequestContext(request))
###########################################################################

@utils.login_required
@utils.check_access_level([2,3])
def admin(request):
    l = MyLog().l()
    p = MyLog().p()
    d = {}

    allSkilltags = TimecardSkillTags().getAll()
    allUsersSkilltagIds = TimecardUserSkillTagId().getAll()
    user_id = int(request.session['uid'])
    userMe = TimecardUser().me(user_id)
    set_menu(request, "admin")
    year=datetime.date.today().year
    month=datetime.date.today().month
    day=datetime.date.today().day
    today_day = "%s-%02d-%s" % (year, month, day)
    proflist = UserProfession.objects.all()
    roleslist = UserRoles.objects.all()
    deplist = UserDepartament.objects.all()
    allOffices = TimecardOffices().getAll()
    users = TimecardUser().getAllUsers( order_by = 'surname' )
    users = TimecardUser().setOfficeName( users = users, allOffices = allOffices )

    roles = ProjectAppendedEmployeeRoleDoc().getAllUsersAppendedOnProjects()
    projs = TimecardProjects().getAllProjects()
    roles = my_join(roles, projs, 'projectId', '_id', 'project_info__', 'one_to_one')
    users = my_join(users, roles, 'id', 'employeeId', 'roles_info__')
    languageSkills = TimecardLanguageSkills().getAllLanguageSkills()
    allUsersLanguages = TimecardUsersLanguages().getAllUsersLanguages()

    users = TimecardUsersLanguages().attachLanguageSkillsToUsers(
        users = users,
        allUsersLanguages = allUsersLanguages,
        languageSkills = languageSkills
    )

    allSkills = TimecardSkills().getAll()
    allSkills = TimecardSkills().prepareForTemplate(allSkills = allSkills)
    usersSkills = TimecardUsersSkills().getAllUsersSkills()
    # FIXME: Method setNamesToSkills() depends on previous operations. SImply DON'T FIX place of this method
    usersSkills = TimecardUsersSkills().setNamesToSkills(usersSkills = usersSkills, allSkills = allSkills)

    users = TimecardUsersSkills().attachSkillsToUsers(
        users = users,
        usersSkills = usersSkills,
        allSkills = allSkills,
    )
    groupedUsers = TimecardUser().groupBy(users=users, group_by='office')
    groupedUsers = TimecardUser().setCurrentLocationOrder(me=userMe, groupedUsers = groupedUsers)

    offices = Offices.objects.all()
    votes = Votes.objects.all().order_by('-id')
    current_user = TimecardUser().me(int(request.session['uid']))
    custom_CSS = utils.change_css_on_some_event(current_user)
    if request.method == 'GET' and 'del_user' in request.GET:
        user_id = request.GET['del_user']
        try:
            # user_rec = User.objects.get(id=user_id)
            # FIXME: If user is not in DB ... i don't really know what to do
            user_rec = TimecardUser().me(user_id)

            # also we have to unassign user from all project assignments
            user_current_projects = ProjectThread.objects.filter(user_id = user_id, who_unassigned = '')
            for project in user_current_projects:
                project.who_unassigned = u"Пользователь удален"
                project.save()

            #and also we have to remove user from all votings
            user_possible_votings = Votes.objects.filter(office = user_rec.office)
            for u_p_v in user_possible_votings:
                guys_who_voted_yes = u_p_v.votes_yes_who.split(' ')
                guys_who_voted_no = u_p_v.votes_no_who.split(' ')
                guys_who_voted_dontcare = u_p_v.votes_dontcare_who.split(' ')
                if str(user_id) in guys_who_voted_yes:
                    u_p_v.votes_yes -= 1
                    guys_who_voted_yes.pop(guys_who_voted_yes.index(str(user_id)))
                    u_p_v.votes_yes_who = ' '.join (guys_who_voted_yes)
                    u_p_v.save()
                if str(user_id) in guys_who_voted_no:
                    u_p_v.votes_no -= 1
                    guys_who_voted_no.pop(guys_who_voted_no.index(str(user_id)))
                    u_p_v.votes_no_who = ' '.join(guys_who_voted_no)
                    u_p_v.save()
                if str (user_id) in guys_who_voted_dontcare:
                    u_p_v.votes_dontcare -=1
                    guys_who_voted_dontcare.pop(guys_who_voted_dontcare.index(str(user_id)))
                    u_p_v.votes_dontcare_who = ' '.join(guys_who_voted_dontcare)
                    u_p_v.save()
            user_rec.delete()


            subject = u"[TT] Из TimeCard удален пользователь %s %s" % (user_rec.name, user_rec.surname)
            message = u"%s %s был удален из TimeCard \n\r" % (user_rec.name, user_rec.surname)

            for office in offices:
                if user_rec.office == office.short_name:
                    datatuple = ((subject, message, utils.ROOT_EMAIL, [office.mass_email]),)

            utils.mail(datatuple)
            return redirect('/admin/')
        except:
            return redirect('/admin/')
    if request.method == 'GET' and 'del_voting' in request.GET:
        try:
            voting_id = request.GET['del_voting']
            voting = Votes.objects.get(id = voting_id)

            voting.delete()
            return redirect('/admin/')
        except:
            return redirect('/admin/')

    if request.method == 'GET' and 'del_dep' in request.GET:
        data_id = request.GET['del_dep']
        dep_to_delete = UserDepartament.objects.get(id = data_id)
        User.objects.filter(dep = dep_to_delete.name).update(dep='')
        dep_to_delete.delete()
        return redirect ('/admin/')
    if request.method == 'GET' and 'del_prof' in request.GET:
        data_id = request.GET['del_prof']
        prof_to_delete = UserProfession.objects.get(id = data_id)
        User.objects.filter(profession = prof_to_delete.name).update(profession='')
        prof_to_delete.delete()
        return redirect ('/admin/')
    if request.method == 'GET' and 'del_role' in request.GET:
        data_id = request.GET['del_role']
        role_to_delete = UserRoles.objects.get(id = data_id)
        role_to_delete.delete()
        ProjectThread.objects.filter(user_role=data_id).update(user_role=None)
        return redirect ('/admin/')
    allUsersTagIdsWithUsers = my_join(
        allUsersSkilltagIds,
        users,
        str(TimecardUserSkillTagId.user_id_),
        'id',
        'users_with_skill__'
    )
    skillTagsWithUsers = my_join(
        allSkilltags,
        allUsersTagIdsWithUsers,
        '_id',
        str(TimecardUserSkillTagId.skill_tag_id_),
        'users_skill_tag_ids__'
    )

    d = dict(
        request=request,
        users=users,
        today_day=today_day,
        deplist=deplist,
        proflist = proflist,
        roleslist=roleslist,
        offices=offices,
        votes = votes,
        current_user = current_user,
        custom_CSS = custom_CSS,
        groupedUsers = groupedUsers,

        skillTagsWithUsers = skillTagsWithUsers,
    )
    return render_to_response('timecard/admin.html', d, context_instance=RequestContext(request))

###########################################################################
@utils.login_required
@utils.check_access_level([3,4])
def image_view(request):
    items = Image.objects.all()
    return render_to_response('images.html', {'items':items})

@utils.login_required
@utils.check_access_level([3,4])
def multiuploader_delete(request, pk):
    if request.method == 'POST':
        image = get_object_or_404(Image, pk=pk)
        image.delete()
        return HttpResponse(str(pk))
    else:
        return HttpResponseBadRequest('Only POST accepted')

@utils.login_required
@utils.check_access_level([3,4])
def projects_upload_files_to_real_project(request):
    l = MyLog().l()
    p = MyLog().p()
    userId = int(request.session['uid'])
    result = []
    response_data = json.dumps(result)
#  -----------------------------------------------------------
    responseObject = {}
    responseObject['objectId'] = None
    responseObject['status'] = 'Received Request to main multiuploader view.'
    if request.method == 'POST':
        responseObject['status'] = 'Received POST to main multiuploader view.'

        if request.FILES == None:
            responseObject['error'] = 'Must have files attached!'

        file = request.FILES.get(u'uploaded_file')
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size

        if 'projectId' in request.POST:
            projectId = request.POST['projectId']
            if len(projectId) == len('5419872e4f452d5032deb488'):
                content = ContentFile(file.read())

                _path = 'projects_data/' + projectId + '/' + filename
                path = default_storage.save(_path, content)
                projectAppendedFilesDoc = ProjectAppendedFilesDoc()
                objectId = projectAppendedFilesDoc.appendFileOnRealProject(userId, filename, projectId)
                responseObject['name'] = filename
                responseObject['size'] = file_size
                responseObject['url'] = '/media/' + _path
                responseObject['filename'] = filename
                responseObject['objectId'] = objectId

                if type(objectId) == ObjectId:
                    responseObject['objectId'] = str(objectId)

        result.append(responseObject);
        response_data = json.dumps(result)

    if responseObject['objectId'] != None:
        resp = HttpResponse(response_data, content_type='application/json')
    else:
        resp = HttpResponseBadRequest("File don\'t upload")

    return resp


@utils.login_required
@utils.check_access_level([3,4])
def projects_upload_files_to_temp_project(request):
    l = MyLog().l()
    p = MyLog().p()
    userId = int(request.session['uid'])
    result = []

    responseObject = {}
    responseObject = {'status': 'Received Request to main multiuploader view.'}

    if request.method == 'POST':
        responseObject = {'status': 'Received POST to main multiuploader view.'}
        if request.FILES == None:
            responseObject = {'error': 'Must have files attached!'}

        file = request.FILES.get(u'uploaded_file')
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size
        tempProjectId = TimecardTempProjects().getTempProjectIdByUserId(userId) # str

        if type(tempProjectId) == str:
            content = ContentFile(file.read())
            _path = 'projects_data/' + tempProjectId + '/' + filename
            path = default_storage.save(_path, content)
            projectAppendedFilesDoc = ProjectAppendedFilesDoc()
            objectId = projectAppendedFilesDoc.appendFileOnEmptyProject(userId, filename)

            responseObject = {
                "name": filename,
                "size": file_size,
                "url": '/media/' + _path,
                "delete_url": '/',
                "status": 1,
                "objectId": ""
            }
            if type(objectId) == ObjectId:
                responseObject['objectId'] = str(objectId)

        else:
            responseObject = {
                "name": filename,
                "size": file_size,
                "url": '/media/',
                "delete_url": '/',
                "status": 0
            }
    result.append(responseObject);
    response_data = json.dumps(result)
    return HttpResponse(response_data, content_type='application/json')


@utils.login_required
@utils.check_access_level([3,4])
def update_employee_role_on_empty_project(request):
    l = MyLog().l()
    doc = None
    if request.method == 'POST':
        appenderId = None
        # if isinstance(request.session, collections.Iterable):
        if 'uid' in request.session:
            appenderId = int(request.session['uid'])

        employeeId = None
        if isinstance(request.POST, collections.Iterable):
            if 'userId' in request.POST:
                employeeId = int(request.POST['userId'])

        roleOnProject = request.POST['roleOnProject']
        startDayOnProject = request.POST['startDayOnProject']
        finishDayOnProject = request.POST['finishDayOnProject']
        compare = MyDate().compare(startDayOnProject, finishDayOnProject, '/')
        isValidStartDate = MyDate().isValidDate(startDayOnProject)

        # If start date before end date or one of the date is not set
        if (compare == 1 or finishDayOnProject == '') and isValidStartDate:
            if appenderId != None and employeeId != None:
                doc = ProjectAppendedEmployeeRoleDoc()\
                    .updateEmployeeRoleOnProject(
                        appenderId,
                        employeeId,
                        roleOnProject,
                        startDayOnProject,
                        finishDayOnProject
                    )
    responseDoc = {}

    if doc != None:
        responseDoc['status'] = True
    else:
        responseDoc['status'] = False

    responseDoc['appenderId'] = appenderId
    responseDoc['employeeId'] = employeeId
    responseDoc['roleOnProject'] = roleOnProject
    responseDoc['startDayOnProject'] = startDayOnProject
    responseDoc['finishDayOnProject'] = finishDayOnProject
    response_data = json.dumps(responseDoc)
    return HttpResponse(response_data, content_type='application/json')

@utils.login_required
@utils.check_access_level([3,4])
def update_employee_role_on_real_project(request):
    l = MyLog().l()
    doc = None
    responseDoc = {}
    if request.method == 'POST':
        appenderId = None
        # if isinstance(request.session, collections.Iterable):
        if 'uid' in request.session:
            appenderId = int(request.session['uid'])

        employeeId = toInt(getVal(request.POST, 'userId'))
        projectId = getVal(request.POST, 'projectId')
        roleOnProject = getVal(request.POST, 'roleOnProject')
        startDayOnProject = getVal(request.POST, 'startDayOnProject')
        finishDayOnProject = getVal(request.POST, 'finishDayOnProject')

        compare = MyDate().compare(startDayOnProject, finishDayOnProject, '/')
        isValidStartDate = MyDate().isValidDate(startDayOnProject)

        # If start date before end date or one of the date is not set
        if (compare == 1 or finishDayOnProject == '') and isValidStartDate == True:
            if appenderId != None and projectId != None and type(employeeId) == int:
                doc = ProjectAppendedEmployeeRoleDoc() \
                    .updateEmployeeRoleOnRealProject(
                    appenderId,
                    projectId,
                    employeeId,
                    roleOnProject,
                    startDayOnProject,
                    finishDayOnProject
                )

    if doc != None:
        responseDoc['status'] = True
    else:
        responseDoc['status'] = False

    responseDoc['appenderId'] = appenderId
    responseDoc['projectId'] = str(projectId)
    responseDoc['employeeId'] = employeeId
    responseDoc['roleOnProject'] = roleOnProject
    responseDoc['startDayOnProject'] = startDayOnProject
    responseDoc['finishDayOnProject'] = finishDayOnProject

    response_data = json.dumps(responseDoc)

    return HttpResponse(response_data, content_type='application/json')



@utils.login_required
@utils.check_access_level([3,4])
def remove_employee_from_empty_project(request):
    rA = None
    if request.method == 'POST':
        userId = int(request.session['uid'])
        employeeId = request.POST['userId']
        rA = ProjectAppendedEmployeeRoleDoc().removeEmployeeFromEmptyProject(userId, employeeId)
    result = {}
    if 'ok' in rA:
        if rA['ok'] == 1:
            result['removeStatus'] = True
        else:
            result['removeStatus'] = False
    response_data = json.dumps(result)
    return HttpResponse(response_data, content_type='application/json')


@utils.login_required
@utils.check_access_level([3,4])
def add_employee_to_real_project_project(request):
    l = MyLog().l()
    if request.method == 'POST':
        userId = int(request.session['uid'])

        employeeId = None
        if 'userId' in request.POST:
            employeeId = request.POST['userId']

        if type(employeeId) == unicode:
            employeeId = int(employeeId)

        projectId = None
        if 'projectId' in request.POST:
            projectId = request.POST['projectId']

        roleOnProject = request.POST['roleOnProject']
        startDate = ''
        finishDate = ''

        responseInsert = ProjectAppendedEmployeeRoleDoc().appendUserOnRealProject(
            userId,
            projectId,
            employeeId,
            roleOnProject,
            startDate,
            finishDate
        )
    responseObject = {
        "status": responseInsert
    }
    response_data = json.dumps(responseObject)

    return HttpResponse(response_data, content_type='application/json')
    # return HttpResponseBadRequest("FIXME: I don't DO ANYTHING: [ " + response_data + " ] ")



@utils.login_required
@utils.check_access_level([3,4])
def add_employee_to_project(request):
    l = MyLog().l()

    if request.method == 'POST':
        userId = int(request.session['uid'])
        employeeId = request.POST['userId']
        roleOnProject = request.POST['roleOnProject']

        startDate = ''
        finishDate = ''

        projectAppendedEmployeeRoleDoc = ProjectAppendedEmployeeRoleDoc()
        responseInsert = projectAppendedEmployeeRoleDoc.appendUserOnEmptyProject(
            userId,
            employeeId,
            roleOnProject,
            startDate,
            finishDate
        )
    result = []
    responseObject = {
        "status": str(responseInsert)
    }
    result.append(responseObject)
    response_data = json.dumps(result)
    return HttpResponse(response_data, content_type='application/json')

# TODO: Turn ON bash.im when all was ready :)


@utils.login_required
@utils.check_access_level([3,4])
def get_all_uploaded_files_objectids(request):
    result = []
    if request.method == 'POST':
        userId = int(request.session['uid'])
        # fileId = request.POST['fileId']
        result = ProjectAppendedFilesDoc().getFilesIdsAppendedOnEmptyProject(userId)
    response_data = json.dumps(result)
    return HttpResponse(response_data, content_type='application/json')



@utils.login_required
@utils.check_access_level([3,4])
def get_all_uploaded_files_objectids_real_project(request):
    result = []
    if request.method == 'POST':
        userId = int(request.session['uid'])
        projectId = request.POST['projectId']
        result = ProjectAppendedFilesDoc().getFilesIdsAppendedOnRealProject(projectId)
    response_data = json.dumps(result)
    return HttpResponse(response_data, content_type='application/json')

@utils.login_required
@utils.check_access_level([3,4])
def update_file_description_for_empty_project(request):
    l = MyLog().l()
    result = {}
    responseObject = {
        "status": 'status'
    }
    if request.method == 'POST':
        l(request.method, 'request.method')
        userId = None
        # if iterable(request.session):
        if 'uid' in request.session:
            userId = int(request.session['uid'])

        if userId != None:
            fileId = getSimpleVal(request.POST, 'fileId')

            if fileId != None:
                description = getSimpleVal(request.POST, 'description')
                result = ProjectAppendedFilesDoc().updateFileDescription(userId, fileId, description)
                result['userId'] = userId
                result['fileId'] = fileId
                result['description'] = description

    response_data = json.dumps(result)
    return HttpResponse(response_data, content_type='application/json')

@utils.login_required
@utils.check_access_level([3,4])
def update_file_description_for_real_project(request):
    result = None
    responseObject = {
        "status": False
    }

    if request.method == 'POST':
        userId = int(request.session['uid'])
        fileId = request.POST['fileId']
        projectId = request.POST['projectId']
        description = request.POST['description']
        result = ProjectAppendedFilesDoc().updateFileDescriptionRealProject(userId, projectId, fileId, description)
        if 'updatedExisting' in result:
            if result['updatedExisting'] == True:
                responseObject['status'] = True

        responseObject['fileId'] = fileId
        responseObject['userId'] = userId
        responseObject['description'] = description

    response_data = json.dumps(responseObject)
    return HttpResponse(response_data, content_type='application/json')


@utils.login_required
def add_language_to_user(request):
    result = None
    responseObject = {}

    if request.method == 'POST':
        userId = int(request.session['uid'])
        user = TimecardUser().me(userId)
        language_id = request.POST['languageId']
        language_written_skills_value = None
        language_spoken_skills_value = None
        insertResult = None

        if user[TimecardUser.can_edit_language_skill_] == 1:
            insertResult = TimecardUsersLanguages().add(
                user_id = userId,
                language_id = language_id,
                language_written_skills_value = language_written_skills_value,
                language_spoken_skills_value = language_spoken_skills_value,
            )

        responseObject['language_name'] = TimecardLanguages().getNameByLanguageId(language_id = language_id)
        if type(insertResult) == ObjectId:
            responseObject['insertResult'] = str(insertResult)
        else:
            responseObject['insertResult'] = 0

    response_data = json.dumps(responseObject)
    return HttpResponse(response_data, content_type='application/json')

@utils.login_required
def update_user_language(request):
    result = None
    responseObject = {}
    updateResult = []

    if request.method == 'POST':
        userId = int(request.session['uid'])
        user = TimecardUser().me(userId)
        language_id = request.POST['languageId']
        writtenSkillsValue = request.POST['writtenSkillsValue']
        spokenSkillsValue = request.POST['spokenSkillsValue']

        if user[TimecardUser.can_edit_language_skill_] == 1:
            updateResult = TimecardUsersLanguages()._update_(
                user_id = userId,
                language_id = language_id,
                language_written_skills_value = writtenSkillsValue,
                language_spoken_skills_value = spokenSkillsValue,
            )
        responseObject['language_id'] = language_id

        if 'updatedExisting' in  updateResult and updateResult['updatedExisting'] == True:
            responseObject['updateResult'] = 1
        else:
            responseObject['updateResult'] = 0

    response_data = json.dumps(responseObject)
    return HttpResponse(response_data, content_type='application/json')


@utils.login_required
def get_all_user_languages(request):
    result = None
    allUserLanguages = []
    responseObject = {}
    responseObject['allUserLanguages'] = allUserLanguages
    if request.method == 'POST':
        userId = int(request.session['uid'])
        allUserLanguages = TimecardUsersLanguages().getAllUserLanguages(user_id = userId)
        responseObject['allUserLanguages'] = allUserLanguages

    response_data = json.dumps(responseObject)
    return HttpResponse(response_data, content_type='application/json')

@utils.login_required
def remove_user_language(request):
    result = None
    responseObject = {}
    removeResult = {}

    if request.method == 'POST':
        userId = int(request.session['uid'])
        user = TimecardUser().me(userId)
        language_id = request.POST['language_id']

        if user[TimecardUser.can_edit_language_skill_] == 1:
            removeResult = TimecardUsersLanguages().remove_user_language(user_id = userId, language_id = language_id)
        responseObject['language_id'] = language_id
        language_name = TimecardLanguages().getNameByLanguageId(language_id = language_id)
        responseObject['language_name'] = language_name

        if 'ok' in removeResult and removeResult['ok'] == 1:
            responseObject['removeResult'] = 1
        else:
            responseObject['removeResult'] = 0

    response_data = json.dumps(responseObject)
    return HttpResponse(response_data, content_type='application/json')


@utils.login_required
@utils.check_access_level([3,4])
def block_language_updating(request):
    response = None
    blockResult = None
    responseObject = {}
    responseObject['blockResult'] = None
    responseObject['userId'] = None

    if request.method == 'POST':
        userId = int(request.session['uid'])
        employeeId = request.POST['userId']

        responseObject['userId'] = employeeId
        blockResult = TimecardUser().blockLanguageEditByUserId(employeeId)

    responseObject['blockResult'] = blockResult
    response_data = json.dumps(responseObject)
    return HttpResponse(response_data, content_type='application/json')

@utils.login_required
@utils.check_access_level([3,4])
def unblock_language_updating(request):
    unblockResult = False
    response = None

    responseObject = {}
    responseObject['unblockResult'] = None
    responseObject['userId'] = None

    if request.method == 'POST':
        userId = int(request.session['uid'])
        employeeId = request.POST['userId']
        responseObject['userId'] = employeeId
        unblockResult = TimecardUser().unblockLanguageEditByUserId(employeeId)

    responseObject['unblockResult'] = unblockResult
    response_data = json.dumps(responseObject)
    return HttpResponse(response_data, content_type='application/json')



@utils.login_required
def add_skill_to_user(request):
    l = MyLog().l()
    p = MyLog().p()
    addResult = False
    response = None

    responseObject = {}
    responseObject['addResult'] = False
    responseObject['skillId'] = None
    responseObject['skillName'] = None
    responseObject['skillDescription'] = None

    if request.method == 'POST':
        userId = int(request.session['uid'])
        skillId = request.POST['skillId']
        responseObject['skillId'] = skillId
        responseObject['skillDescription'] = ''
        me = TimecardUser().me(userId)

        canEdit = False
        if isinstance(me, collections.Iterable):
            if TimecardUser.can_edit_skill_ in me:
                if me[TimecardUser.can_edit_skill_] == 1:
                    canEdit = True

        if canEdit == True:
            addResult = TimecardUsersSkills().add(skillId = skillId, userId = userId)

        skillName = TimecardSkills().getSkillNameById(skillId = skillId);
        responseObject['skillName'] = skillName
    responseObject['addResult'] = str(addResult)
    response_data = json.dumps(responseObject)
    return HttpResponse(response_data, content_type='application/json')

@utils.login_required
def update_skill_to_user(request):
    updateResult = False
    response = None

    l = MyLog().l()
    responseObject = {}
    responseObject['updateResult'] = None
    responseObject['skillId'] = None
    responseObject['skillName'] = None
    responseObject['description'] = None
    if request.method == 'POST':
        userId = int(request.session['uid'])
        skillId = getSimpleVal(request.POST, 'skillId')
        responseObject['skillId'] = skillId
        description = getSimpleVal(request.POST, 'description')
        responseObject['description'] = description
        me = TimecardUser().me(userId)
        canEdit = False
        if isinstance(me, collections.Iterable):
            if TimecardUser.can_edit_skill_ in me:
                if me[TimecardUser.can_edit_skill_] == 1:
                    canEdit = True
            else:
                canEdit = True

        if canEdit == True:
            updateResult = TimecardUsersSkills()._update_(
                skillId = skillId,
                userId = userId,
                description = description
            )
            theseSkillTagIds = TimecardSkillTags().addNewTags(description = description)
            addedResult = TimecardUserSkillTagId().addSkillTagIdsToUser(userId, skillId, theseSkillTagIds)

    if type(updateResult) == dict:
        if 'updatedExisting' in updateResult:
            updateResult = updateResult['updatedExisting']
    responseObject['updateResult'] = updateResult
    response_data = json.dumps(responseObject)
    return HttpResponse(response_data, content_type='application/json')

@utils.login_required
def remove_skill(request):
    unblockResult = None
    response = None
    removeResult = False
    responseObject = {}
    responseObject['removeResult'] = None
    responseObject['skillId'] = None
    responseObject['skillName'] = None

    if request.method == 'POST':
        userId = int(request.session['uid'])
        skillId = request.POST['skillId']
        responseObject['skillId'] = skillId
        skillName = TimecardSkills().getSkillNameById(skillId = skillId)
        responseObject['skillName'] = skillName
        me = TimecardUser().me(userId)
        canEdit = False
        if isinstance(me, collections.Iterable):
            if TimecardUser.can_edit_skill_ in me:
                if me[TimecardUser.can_edit_skill_] == 1:
                    canEdit = True

        if canEdit == True:
            removeResult = TimecardUsersSkills()._remove_(skillId = skillId, userId = userId)

    responseObject['removeResult'] = removeResult
    response_data = json.dumps(responseObject)
    return HttpResponse(response_data, content_type='application/json')



@utils.login_required
@utils.check_access_level([3,4])
def block_editing_skills(request):
    blockResult = None
    response = None
    responseObject = {}
    responseObject['blockResult'] = None
    responseObject['userId'] = None

    if request.method == 'POST':
        userId = int(request.session['uid'])
        employeeId = request.POST['userId']
        responseObject['userId'] = employeeId
        blockResult = TimecardUser().blockSkillEditByUserId(employeeId)

    responseObject['blockResult'] = blockResult
    response_data = json.dumps(responseObject)
    return HttpResponse(response_data, content_type='application/json')

@utils.login_required
@utils.check_access_level([3,4])
def unblock_editing_skills(request):
    unblockResult = None
    response = None
    responseObject = {}
    responseObject['unblockResult'] = None
    responseObject['userId'] = None

    if request.method == 'POST':
        userId = int(request.session['uid'])
        employeeId = request.POST['userId']
        responseObject['userId'] = employeeId
        unblockResult = TimecardUser().unblockSkillEditByUserId(employeeId)

    responseObject['unblockResult'] = unblockResult
    response_data = json.dumps(responseObject)
    return HttpResponse(response_data, content_type='application/json')

@utils.login_required
def showing_skill_on_main_page(request):
    responseObject = {}
    responseObject['skillId'] = None
    responseObject['action'] = None
    responseObject['actionResult'] = None

    if request.method == 'POST':
        result = False
        userId = int(request.session['uid'])
        skillId = request.POST['skillId']
        responseObject['skillId'] = skillId
        action = request.POST['action']
        responseObject['action'] = action
        me = TimecardUser().me(userId)
        canEdit = False
        if isinstance(me, collections.Iterable):
            if TimecardUser.can_edit_skill_ in me:
                if me[TimecardUser.can_edit_skill_] == 1:
                    canEdit = True

        if canEdit == True:
            for case in switch(action):
                if case('set'):
                    # l('we_activate_this')
                    result = TimecardUsersSkills().activateShowOnMainPage(skillId = skillId, userId = userId)
                    break
                if case('unset'):
                    # l('we_deactivate_this')
                    result = TimecardUsersSkills().deactivateShowOnMainPage(skillId = skillId, userId = userId)
                    break
                if case(): # default
                    pass
    responseObject['actionResult'] = result
    response_data = json.dumps(responseObject)
    return HttpResponse(response_data, content_type='application/json')


@utils.login_required
@utils.check_access_level([3,4])
def update_project(request):
    addResult = False
    l = MyLog().l()
    p = MyLog().p()
    responseObject = {}
    msg = ''
    updateResult = False

    if request.method == 'POST':
        result = False
        userId = int(request.session['uid'])
        projectId = getSimpleVal(request.POST, 'projectId')
        project_name = getSimpleVal(request.POST, 'project_name')
        project_desc = getSimpleVal(request.POST, 'project_desc')
        project_desc_for_customer = getSimpleVal(request.POST, 'project_desc_for_customer')
        customer = getSimpleVal(request.POST, 'customer')
        customer_feedback = getSimpleVal(request.POST, 'customer_feedback')
        service = getSimpleVal(request.POST, 'service')
        industry = getSimpleVal(request.POST, 'industry')
        solution_highlight = getSimpleVal(request.POST, 'solution_highlight')
        development_tools_and_technologies = getSimpleVal(request.POST, 'development_tools_and_technologies')
        development_time = getSimpleVal(request.POST, 'development_time')
        start_date = getSimpleVal(request.POST, 'start_date')
        finish_date = getSimpleVal(request.POST, 'finish_date')
        project_is_in_pause = getSimpleVal(request.POST, 'project_is_in_pause')
        compareResult = MyDate().compare(start_date, finish_date, '/')
        isValidStartDate = MyDate().isValidDate(start_date)
        employeeOnProject = ProjectAppendedEmployeeRoleDoc().getEmployeeIdsOnRealProject_(userId, projectId)
        isValidAllStartsDays = ProjectAppendedEmployeeRoleDoc().hasEmployeeValidStartDayOnRealProject(projectId)

        if isValidAllStartsDays == True \
                and project_name != ''\
                and employeeOnProject \
                and (compareResult == 1 or finish_date == '') \
                and isValidStartDate == True:

            updateResult = TimecardProjects().updateProject(
                        projectId = projectId,
                        project_name=project_name,
                        project_desc=project_desc,
                        project_desc_for_customer = project_desc_for_customer,
                        customer_id = customer,
                        customer_feedback = customer_feedback,
                        service = service,
                        industry = industry,
                        solution_highlight = solution_highlight,
                        development_tools_and_technologies = development_tools_and_technologies,
                        development_time = development_time,
                        start_date = start_date,
                        finish_date = finish_date,
                        project_is_in_pause = project_is_in_pause,
                        creator_id = userId,
                        project_opened=1
            )

    responseObject['updateResult'] = updateResult
    responseObject['isValidAllStartsDays'] = isValidAllStartsDays
    if updateResult:
        responseObject['msg'] = 'Проект обновлен'
    else:
        responseObject['err'] = 'Заполните все поля помеченные звездочкой. Проверьте даты старта работы всех сотрудников на проекте.'
    response_data = json.dumps(responseObject)
    return HttpResponse(response_data, content_type='application/json')

@utils.login_required
@utils.check_access_level([3,4])
def add_project(request):
    addResult = False
    l = MyLog().l()
    p = MyLog().p()
    responseObject = {}

    if request.method == 'POST':
        result = False
        userId = int(request.session['uid'])
        project_name = request.POST['project_name']
        project_desc = request.POST['project_desc']
        project_desc_for_customer = request.POST['project_desc_for_customer']
        customer = request.POST['customer']
        customer_feedback = request.POST['customer_feedback']
        service = request.POST['service']
        industry = request.POST['industry']
        solution_highlight = request.POST['solution_highlight']
        development_tools_and_technologies = request.POST['development_tools_and_technologies']
        development_time = request.POST['development_time']
        start_date = request.POST['start_date']
        finish_date = request.POST['finish_date']
        project_is_in_pause = request.POST['project_is_in_pause']
        msg = ''
        err = ''
#/////////////////////////////////////////////////////////////////////////////////////////////////////////
        compareResult = MyDate().compare(start_date, finish_date, '/')
        validStartDate = MyDate().isValidDate(start_date)
        employeeIdsOnProject = ProjectAppendedEmployeeRoleDoc().getEmployeeIdsOnEmptyProject_(userId)
        isValidAllStartsDays = ProjectAppendedEmployeeRoleDoc().hasEmployeeValidStartDayOnEmptyProject(userId)

        if(isValidAllStartsDays == True
           and validStartDate == True
           and project_name != ''
           and employeeIdsOnProject
           and (compareResult == 1 or finish_date == '')
                ):
            # and (project_desc != '')\
            # and (customer != '')\  #  TODO: WHen select box was ready -- Un comment it
            tempProjectId = TimecardTempProjects().getTempProjectIdByUserId(userId) # str
            insertedProjectId = TimecardProjects().insertNewProject(
                        temp_project_id = tempProjectId,
                        project_name=project_name,
                        project_desc=project_desc,
                        project_desc_for_customer = project_desc_for_customer,
                        customer_id = customer,
                        customer_feedback = customer_feedback,
                        service = service,
                        industry = industry,
                        solution_highlight = solution_highlight,
                        development_tools_and_technologies = development_tools_and_technologies,
                        development_time = development_time,
                        start_date = start_date,
                        finish_date = finish_date,
                        project_is_in_pause = project_is_in_pause,
                        creator_id = userId,
                        project_opened=1
            )
            if insertedProjectId != None:
                # Every should have tempProjectID: TT can apply employee everytime when it neccessary
                resultGenerationNewTempProjectId = TimecardTempProjects()
                resultGenerationNewTempProjectId = TimecardTempProjects().generateNewTempProjectIdForUserId(userId) # str
                resultDoc = ProjectAppendedEmployeeDoc().bindEmployeeToProject(userId, insertedProjectId)
                resultRoleDoc = ProjectAppendedEmployeeRoleDoc().bindEmployeeToProject(userId, insertedProjectId)
                resultFilesDoc = ProjectAppendedFilesDoc().bindFilesToProject(userId, insertedProjectId)
                projectCreationStatus = 1
                msg = u"Новый проект [ %s ] добавлен [%s]" %(project_name, insertedProjectId)
                addResult = True
            else:
                err = u"Произошла ошибка при создании проекта"
        else:
            if not employeeIdsOnProject:
                err = u"Добавьте хотя бы одного человека на проект"
            else:
                err = u"Заполните корректно все поля помеченные звездочкой чтобы создать проект. Проверьте даты начала работы сотрудников на проекте"

            if type(compareResult) == int and compareResult == 0:
                err = err + u"Дата старта и окончания проекта совпадают."

            if compareResult == -1:
                err = err + u" Неверные даты старта и окончания проекта."
#/////////////////////////////////////////////////////////////////////////////////////////////////////////
    responseObject['addResult'] = addResult
    responseObject['msg'] = msg
    responseObject['err'] = err
    # responseObject['validStartDate'] = validStartDate
    responseObject['isValidAllStartsDays'] = isValidAllStartsDays
    response_data = json.dumps(responseObject)
    return HttpResponse(response_data, content_type='application/json')

###########################################################################
@utils.login_required
def my_projects(request):
    l = MyLog().l()
    p = MyLog().p()
    set_menu(request, "my_projects")
    rolesOnProjects = []
    allProjects = []
    if request.method == 'GET':
        employeeId = int(request.session['uid'])
        allProjects = TimecardProjects().getAllProjects()
        rolesOnProjects = ProjectAppendedEmployeeRoleDoc().getRolesByEmployeeId(employeeId = employeeId)
        rolesOnProjects = my_join(
            rolesOnProjects,
            allProjects,
            str(ProjectAppendedEmployeeRoleDoc.projectId),
            '_id',
            'projects__'
        )
    dictionary = {}
    dictionary[ 'rolesOnProjects' ] = rolesOnProjects
    return render_to_response(
        'timecard/my_projects.html',
        dictionary,
        context_instance=RequestContext(request)
    )

@utils.login_required
def update_work_period_on_project(request):
    l = MyLog().l()
    p = MyLog().p()
    updateResult = False
    response = None
    responseObject = {}
    responseObject['updateResult'] = None
    responseObject['startDate'] = None
    responseObject['skillName'] = None
    responseObject['description'] = None

    if request.method == 'POST':
        # userId = int(request.session['uid'])
        projectRoleId = responseObject['projectRoleId'] = request.POST['projectRoleId']
        startDayOnProject = responseObject['startDate'] = request.POST['startDate']
        finishDayOnProject = responseObject['finishDate'] = request.POST['finishDate']

        # me = TimecardUser().me(userId)
        # canEdit = False
        # if isinstance(me, collections.Iterable):
        #     if TimecardUser.can_edit_skill_ in me:
        #         if me[TimecardUser.can_edit_skill_] == 1:
        #             canEdit = True

        canEdit = True
        if canEdit == True:
            updateResult = ProjectAppendedEmployeeRoleDoc().updateEmployeeWorkPeriodOnProject(
                projectRoleId = projectRoleId,
                startDayOnProject = startDayOnProject,
                finishDayOnProject = finishDayOnProject
            )
    if type(updateResult) == dict:
        if 'updatedExisting' in updateResult:
            updateResult = updateResult['updatedExisting']

    responseObject['updateResult'] = updateResult
    response_data = json.dumps(responseObject)
    return HttpResponse(response_data, content_type='application/json')

@utils.login_required
def add_position_to_user(request):
    l = MyLog().l()
    p = MyLog().p()
    updateResult = False
    addResult = False
    responseObject = {}
    responseObject['addResult'] = False
    responseObject['positionId'] = None
    responseObject['positionName'] = None

    if request.method == 'POST':
        positionId = getSimpleVal(request.POST, 'positionId')
        userId = int(request.session['uid'])
        # me = TimecardUser().me(userId)
        responseObject['positionId'] = positionId
        addResult = TimecardUsersPositions().addPositionToUser(userId = userId, positionId = positionId)
        if isValidObjectId(addResult):
            addResult = True
            responseObject['positionName'] = TimecardPositions().getPositionNameById(positionId = positionId)
    responseObject['addResult'] = addResult
    response_data = json.dumps(responseObject)
    return HttpResponse(response_data, content_type='application/json')

@utils.login_required
def remove_position_from_user(request):
    l = MyLog().l()
    result = None
    responseObject = {}
    removeResult = False

    if request.method == 'POST':
        userId = int(request.session['uid'])
        user = TimecardUser().me(userId)
        positionId = getSimpleVal(request.POST, 'positionId')

        if True or user[TimecardUser.can_edit_position_skill_] == 1:
            removeResult = TimecardUsersPositions().remove_position_from_user(
                userId = userId,
                positionId = positionId
            )
        responseObject['positionId'] = positionId
        position_name = TimecardPositions().getNameByPositionId(positionId = positionId);
        responseObject['positionName'] = position_name
        responseObject['removeResult'] = removeResult
    response_data = json.dumps(responseObject)
    return HttpResponse(response_data, content_type='application/json')

@utils.login_required
def show_position_on_main_page(request):

    l = MyLog().l()
    responseObject = {}
    responseObject['skillId'] = None
    responseObject['action'] = None
    responseObject['actionResult'] = None
    if request.method == 'POST':
        result = False
        positionId = getSimpleVal(request.POST, 'positionId')
        action = getSimpleVal(request.POST, 'action')
        userId = int(request.session['uid'])
        me = TimecardUser().me(userId)
        k  = str(TimecardUser.can_edit_position_skill_)
        canEdit = getVal(me, k)

        if canEdit == True:
            for case in switch(action):
                if case('set'):
                    result = TimecardUsersPositions().activateShowOnMainPage(
                        positionId = positionId,
                        userId = userId
                    )
                    break
                if case('unset'):
                    result = TimecardUsersPositions().deactivateShowOnMainPage(
                        positionId = positionId,
                        userId = userId
                    )
                    break
                if case(): # default
                    pass
    responseObject['actionResult'] = result
    response_data = json.dumps(responseObject)
    return HttpResponse(response_data, content_type='application/json')



def close_project(request):
    l = MyLog().l()
    unblockResult = None
    response = None
    removeResult = False
    responseObject = {}
    responseObject['closeResult'] = None
    responseObject['projectId'] = None
    responseObject['projectName'] = None
    if request.method == 'POST':
        userId = int(request.session['uid'])
        projectId = getSimpleVal(request.POST, 'projectId')
        responseObject['skillId'] = projectId
        projectName = TimecardProjects().getProjectNameById(projectId = projectId)
        responseObject['projectName'] = projectName
        me = TimecardUser().me(userId)
        closeResult = TimecardProjects().close(projectId = projectId, userId = userId)
    responseObject['closeResult'] = closeResult
    if closeResult == True:
        responseObject['msg'] = 'Проект ' + projectName.encode('utf-8') + ' закрыт'
    response_data = json.dumps(responseObject)
    return HttpResponse(response_data, content_type='application/json')
