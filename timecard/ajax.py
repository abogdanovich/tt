# -*- coding: utf-8 -*-
#########################################################################
# TimeCard ajax requests
# author Alex Bogdanovich
# 2012
#
#
# feature support and improvements Mikalai Yurkin
# 2013
#########################################################################

from datetime import *

from dajax.core import Dajax
# from django.utils import simplejson
import json as simplejson

from dajaxice.decorators import dajaxice_register
from timecard.models import User, UserTime, UserPost, UserPostComment, UserMissedHours, Boss_notice, Projects, Reports,\
    Votes, ProjectThread, Offices, UserProfession, UserDepartament, UserRoles, Reservation_Objects
from timecard import utils
import settings
import os
from django.shortcuts import render_to_response
from django.template import RequestContext
import random
from timecard.models import TimecardProjects
from timecard.models import ProjectAppendedEmployeeDoc


# from app_models.project_appended_employee_role import ProjectAppendedEmployeeRoleDoc
from timecard.models import ProjectAppendedEmployeeRoleDoc



from timecard.app_models.project_appended_files_doc import ProjectAppendedFilesDoc
from app_models.timecard_temp_projects import TimecardTempProjects
from timecard.app_classes.MyDate import *
#######################################################################

@dajaxice_register
def dajaxice_example(request, testfield):
    return simplejson.dumps({'message':'Hello from Python! ' + testfield})


def upload_logo(request):

    ext = ".jpg"
    user = User.objects.get(id=int(request.session['uid']))
    avator_out_name = "%s_temp%s" % (user.login, ext)
    alloved_files = (".jpg", ".jpeg", ".png", ".JPEG", ".JPG", ".bmp", ".BMP", ".PNG")

    path = "%suserpic/" % (settings.MEDIA_ROOT)
    path_web = "%suserpic/" % (settings.MEDIA_URL)

    if not os.path.isdir(path):
        try:
            os.makedirs(path)
        except:
            excepttext = "Error: could not create directory to upload files!"
            print excepttext
            return excepttext

    for image_file in request.FILES:
        filename = request.FILES[image_file].name
        name, ext = os.path.splitext(filename)
        if ext not in alloved_files:
            continue

        if filename == "":
            continue

    f = request.FILES[image_file]
    destination = open(path + avator_out_name, 'wb')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

    content = {
        "image": "%s%s" % (path_web, avator_out_name),
    }

    utils.img_resize(path+avator_out_name)

    #move this section for user - when press SAVE button

    return render_to_response("timecard/refresh_uploaded_images.html", content, context_instance=RequestContext(request))

#######################################################################

@dajaxice_register
def user_change_mod(request, mod, button):
    dajax = Dajax()

    module = utils.set_modules(int(request.session['uid']), mod)
    #dajax.alert(module)
    if module == 1:
        #assign button label
        dajax.script("$('#"+button+"').attr('value', 'hide module')")
        msg = "%s is updated" % mod

    else:
        #assign button label
        dajax.script("$('#"+button+"').attr('value', 'show module')")
        msg = "%s is updated" % mod

    dajax.assign('#msg_area_mod', 'innerHTML', msg)

    return dajax.json()

#######################################################################

@dajaxice_register
def show_user_details(request, uid):
    dajax = Dajax()
    user = User.objects.get(id=uid)

    str1 = ""
    str2 = ""
    str3 = ""
    str4 = ""
    str5 = ""
    str6 = ""

    if user.avator != "":
        rand = random.randint(1, 999999)
        str1 = "<div style='max-height: 150px; width: 150px; overflow: auto;'><img src='%suserpic/%s?v=%s' class='active' width='100px'/></div><br/><br/>" % (settings.MEDIA_URL, user.avator, rand)
    else:
        if user.fb != "":
            str1 = "<div style='max-height: 150px; width: 150px; overflow: auto;'><img src='https://graph.facebook.com/%s/picture?type=large' class='active' width='100px' height='100px'/></div><br/><br/>" % (user.fb)
        else:
            str1 = "<img src='%suserpic/noavator.jpg' class='active' /></div><br/><br/>" % (settings.MEDIA_URL)

    str2 = "<h2>%s %s</h2>" % (user.name, user.surname)
    str3 = "%s | %s <br/>" % (user.dep, user.group)
    str4 = "%s<br/>" % (user.phone)
    str5 = "B-day: %s<br/><br/>" % (user.hb)
    str6 = "<a href='skype:%s?chat'><img src='%sicons/skype.png' /></a>\
    <a href='http://twitter.com/%s' target='blank'><img src='%sicons/twitter.png' /></a>\
    <a href='mailto:%s'><img src='%sicons/email.png' /></a>\
    <a href='http://facebook.com/%s' target='blank'><img src='%sicons/facebook.png' /></a>\
    <br/>" % (user.skype, settings.MEDIA_URL, user.twitter, settings.MEDIA_URL, user.email, settings.MEDIA_URL, user.fb, settings.MEDIA_URL)

    user_details = "%s%s%s%s%s%s" % (str1, str2, str3, str4, str5, str6)

    dajax.assign('#user_details_area', 'innerHTML', user_details)

    return dajax.json()

#######################################################################

@dajaxice_register
def save_spam_comment(request, post_id, comment_post):
    dajax = Dajax()
    user = User.objects.get(id=int(request.session['uid']))
    user_name = u'%s %s' % (user.name, user.surname)
    comment = u'%s' % (comment_post)
    comment = "<br/>".join(comment.split("\n"))
    post_created = utils.save_spam_comment(request, int(post_id), comment_post)
    date = post_created.strftime('%A %d | %H:%M')
    dajax.script("$('.comment:last').append('<div class=\"comment\"> <i> " + user_name + " | " + date + "  </i> <div style=\"margin-top: 5px; border: 1px dotted #5C5C5C; padding: 5px; background-color: #E0E0E0\" class=\"rnd\"> " + comment + " </div></div>');")
    dajax.script("$('#comment_post').val('')")
    return dajax.json()
#######################################################################

@dajaxice_register
def save_user_avatar(request, uid):
    dajax = Dajax()
    try:
        user = User.objects.get(id=int(uid))
        ext = ".jpg"
        path = "%suserpic/" % (settings.MEDIA_ROOT)
        path_web = "%suserpic/" % (settings.MEDIA_URL)

        avator_in_name = "%s%s_temp%s" % (path, user.login, ext)
        avator_out_name = path + user.login + ext

        utils.img_save(avator_in_name, avator_out_name)
        user.avator = user.login + ext
        user.save()

        rand = random.randint(1, 999999)
        user_live_pic = "%s%s_temp%s?v=%s" % (path_web, user.login, ext, rand)
        dajax.assign('#original_user_pic','src',user_live_pic)
        dajax.assign('#user_avator','src',user_live_pic)
        msg = u"Аватарка обновлена"
        dajax.assign('#msg_area_pic', 'innerHTML', msg)
    except:
        dajax.alert(u'Обновите страницу и попробуйте снова')

    return dajax.json()

#######################################################################

@dajaxice_register
def user_image_rotate(request, uid):
    dajax = Dajax()

    user = User.objects.get(id=uid)
    ext = ".jpg"
    path = "%suserpic/" % (settings.MEDIA_ROOT)
    path_web = "%suserpic/" % (settings.MEDIA_URL)

    avator_in_name = "%s%s_temp%s" % (path, user.login, ext)

    utils.img_rotate(avator_in_name)
    rand = random.randint(1, 999999)
    user_live_pic = "%s%s_temp%s?v=%s" % (path_web, user.login, ext, rand)
    dajax.assign('#card_logotype','src',user_live_pic)

    return dajax.json()

#######################################################################

@dajaxice_register
def user_image_filters(request, uid, filters_type):
    dajax = Dajax()
    user = User.objects.get(id=uid)
    ext = ".jpg"
    path = "%suserpic/" % (settings.MEDIA_ROOT)
    path_web = "%suserpic/" % (settings.MEDIA_URL)
    avator_in_name = "%s%s_temp%s" % (path, user.login, ext)
    fname = filters_type
    utils.img_filters(avator_in_name, fname)
    rand = random.randint(1, 999999)
    user_live_pic = "%s%s_temp%s?v=%s" % (path_web, user.login, ext, rand)
    dajax.assign('#card_logotype','src',user_live_pic)
    return dajax.json()

#######################################################################

@dajaxice_register
def set_day_off(request, dt, office):
    dajax = Dajax()
    dayoff = dict(c_yearoff=dt[:4], c_monthoff=dt[5:7], c_dayoff=dt[8:10])
    #print dayoff
    if utils.save_calendar_dayoff(dayoff,office):
        msg = u"Выставлен выходной: %s" % dt
    else:
        msg = u"Выставлен рабочий день: %s" % dt
    dajax.assign('#msg_area_dayoff', 'innerHTML', msg)
    return dajax.json()

#######################################################################

@dajaxice_register
def save_duty_date(request, dt, user, button_id):
    dajax = Dajax()
    if utils.save_duty_user(dt, user):
        dajax.script("$('#td_"+button_id+"').css({'background-color' : 'red'})")
    else:
        dajax.script("$('#td_"+button_id+"').css({'background-color' : 'white'})")

    return dajax.json()

#######################################################################

@dajaxice_register
def approve_corrected_time(request, record, button_id):
    dajax = Dajax()
    record_data = UserMissedHours.objects.get(id=record)
    #send request
    subject = u"[TT] Запрос на коррекцию часов удовлетворен"
    message = u"Ваши часы были исправлены. \n\r Ваш запрос от [ %s ] с сообщением: \n %s" % (record_data.date, record_data.umess)

    #get user db data
    user = User.objects.get(id=record_data.user)
    datatuple = (
        (subject, message, utils.TT_EMAIL_SYSTEM, [user.email]),
    )
    utils.mail(datatuple)
    record_data.status = 1
    record_data.save()
    dajax.script("$('#"+button_id+"').hide()")
    dajax.assign('#msg_area_editor', 'innerHTML', u'Корректировка времени выполнена и сотрудник извещен об этом. <a href="/user_requests/">BACK</a>')

    return dajax.json()

#######################################################################

@dajaxice_register
def add_corrected_time(request, uid, date, time):
    dajax = Dajax()
    try:
        user = User.objects.get(id = uid)
        #we must use this timeshift because other offices may use other time zone
        #but we want to show them user time accordingly to their local time, not the server time

        #time has simple hh:mm - need convert into YYY-MM-DD HH:MM:SS -> int format
        sdate = date.split("-")
        stime = time.split(":")
        yy = int(sdate[0])
        mm = int(sdate[1])
        dd = int(sdate[2])
        h = int(stime[0])
        m = int(stime[1])
        dt = datetime.datetime(yy,mm,dd,h,m)
        dt = dt - datetime.timedelta(hours=3)  # GMS+3 offset for UTC time
        sdate = dt.strftime('%Y-%m-%d %H:%M')
        corrected_time = utils.get_unix_strdtime(sdate)
        utime = UserTime(user_id=uid, time=corrected_time)
        utime.save()
        user.status = utils.get_user_state(uid)
        user.save()
        msg = '<div style="display: inline; background-color: #FF9999; padding: 5px; width: 60px; height: 10px; ' \
              'border: groove 1px gray;">%02d:%02d</div>&nbsp;' % (h,m)  # here we have to add timeshift
        dajax.append('#missed_time_area', 'innerHTML', msg)
    except ValueError:
        dajax.alert(u'Выставлены некорректные значения! Часы [0..23], минуты [0..59]')

    return dajax.json()

#######################################################################

@dajaxice_register
def delete_spam_comment(request, post_id, button_id):
    dajax = Dajax()

    post = UserPostComment.objects.get(id=post_id)
    post.delete()

    dajax.script("$('#"+button_id+"').hide()")

    return dajax.json()

#######################################################################

@dajaxice_register
def delete_spam_post(request, post_id, button_id):
    dajax = Dajax()

    post = UserPost.objects.get(id=post_id)
    post.delete()

    dajax.script("$('#"+button_id+"').hide()")

    return dajax.json()

#######################################################################

@dajaxice_register
def delete_record(request, time_id, button_id):
    dajax = Dajax()

    time = UserTime.objects.get(id=time_id)
    uid = time.user_id
    time.delete()
    user = User.objects.get(id = uid)
    user.status = utils.get_user_state(uid)
    user.save()

    dajax.assign('#'+button_id, 'innerHTML', '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
    dajax.script("$('#"+button_id+"').hide()")

    return dajax.json()

#######################################################################

@dajaxice_register
def make_pm(request, uid, button_id):
    dajax = Dajax()

    user = User.objects.get(id=uid)
    #send request
    user.accessLevel = 4 # make project manager
    user.save()
    dajax.alert(user.login + u' получил уровень доступа Проект Менеджер')

    dajax.script("$('#"+button_id+"').attr('disabled', true)")

    dajax.script("$('#make_user_button_"+str(uid)+"').attr('disabled', false)")
    dajax.script("$('#make_boss_button_"+str(uid)+"').attr('disabled', false)")
    dajax.script("$('#make_admin_button_"+str(uid)+"').attr('disabled', false)")
    dajax.script("$('#make_root_button_"+str(uid)+"').attr('disabled', false)")

    return dajax.json()

#######################################################################

@dajaxice_register
def make_root(request, uid, button_id):
    dajax = Dajax()

    user = User.objects.get(id=uid)
    #send request
    user.accessLevel = 3 # make root
    user.save()
    dajax.alert(user.login + u' получил уровень доступа Root (полный доступ)')

    dajax.script("$('#"+button_id+"').attr('disabled', true)")

    dajax.script("$('#make_user_button_"+str(uid)+"').attr('disabled', false)")
    dajax.script("$('#make_boss_button_"+str(uid)+"').attr('disabled', false)")
    dajax.script("$('#make_admin_button_"+str(uid)+"').attr('disabled', false)")
    dajax.script("$('#make_pm_button_"+str(uid)+"').attr('disabled', false)")
    utils.alert_mail(uid, alert_type="accessLevel")
    return dajax.json()

#######################################################################

@dajaxice_register
def make_admin(request, uid, button_id):
    dajax = Dajax()

    user = User.objects.get(id=uid)
    #send request
    user.accessLevel = 2 # make admin
    user.save()
    dajax.alert(user.login + u' получил уровень доступа Администратор')

    dajax.script("$('#"+button_id+"').attr('disabled', true)")

    dajax.script("$('#make_user_button_"+str(uid)+"').attr('disabled', false)")
    dajax.script("$('#make_boss_button_"+str(uid)+"').attr('disabled', false)")
    dajax.script("$('#make_pm_button_"+str(uid)+"').attr('disabled', false)")
    dajax.script("$('#make_root_button_"+str(uid)+"').attr('disabled', false)")
    utils.alert_mail(uid, alert_type="accessLevel")
    return dajax.json()

#######################################################################

@dajaxice_register
def make_boss(request, uid, button_id):
    dajax = Dajax()

    user = User.objects.get(id=uid)
    #send request
    user.accessLevel = 1 # make boss
    user.save()
    dajax.alert(user.login + u' получил уровень доступа Руководитель офиса')

    dajax.script("$('#"+button_id+"').attr('disabled', true)")

    dajax.script("$('#make_user_button_"+str(uid)+"').attr('disabled', false)")
    dajax.script("$('#make_pm_button_"+str(uid)+"').attr('disabled', false)")
    dajax.script("$('#make_admin_button_"+str(uid)+"').attr('disabled', false)")
    dajax.script("$('#make_root_button_"+str(uid)+"').attr('disabled', false)")
    utils.alert_mail(uid, alert_type="accessLevel")
    return dajax.json()

#######################################################################

@dajaxice_register
def make_user(request, uid, button_id):
    dajax = Dajax()

    user = User.objects.get(id=uid)
    #send request
    user.accessLevel = 0 # make user
    user.save()
    dajax.alert(user.login + u' получил уровень доступа Пользователь')

    dajax.script("$('#"+button_id+"').attr('disabled', true)")

    dajax.script("$('#make_pm_button_"+str(uid)+"').attr('disabled', false)")
    dajax.script("$('#make_boss_button_"+str(uid)+"').attr('disabled', false)")
    dajax.script("$('#make_admin_button_"+str(uid)+"').attr('disabled', false)")
    dajax.script("$('#make_root_button_"+str(uid)+"').attr('disabled', false)")

    return dajax.json()

#######################################################################

@dajaxice_register
def save_boss_notice(request, user, date, notice):

    dajax = Dajax()

    if notice == "":
        notice = " "
    #save boss notice
    try:
        boss_notice = Boss_notice.objects.get(user=user, date=date)
        boss_notice.notice = notice
        boss_notice.save()
    except Boss_notice.DoesNotExist:
        boss_notice = Boss_notice(user=user, date=date, notice=notice)
        boss_notice.save()
    dajax.script('$("#dialog_correct_my_hours").hide();')
    dajax.assign('#msg_area', 'innerHTML', u'Ваша отметка сохранена. Обновите страницу.')
    return dajax.json()

#######################################################################

@dajaxice_register
def show_boss_notice(request, date):

    dajax = Dajax()

    dajax.assign('#correct_user_date', 'innerHTML', date)
    dajax.script("$('#correct_user_date_input').attr('value', '"+date+"')")
    dajax.script("$('#correct_time').attr('value', '')")
    dajax.assign('#correction_txt_label', 'innerHTML', 'Notice')

    dajax.script('$("#sendrequestbuttom").hide();')
    dajax.script('$("#save_boss_notice").show();')

    dajax.script('$("#dialog_correct_my_hours").show();')

    return dajax.json()

#######################################################################

@dajaxice_register
def show_correct_dialog(request, correct_date):

    dajax = Dajax()
    dajax.assign('#correct_user_date', 'innerHTML', correct_date)
    dajax.script("$('#correct_user_date_input').attr('value', '"+correct_date+"')")
    dajax.script('$("#dialog_correct_my_hours").show();')
    return dajax.json()

#######################################################################

@dajaxice_register
def send_time_correction(request, dt, uid, msg):
    dajax = Dajax()

    user = User.objects.get(id=uid)
    offices = Offices.objects.all()
    #send request

    dajax.script('$("#dialog_correct_my_hours").hide();')
    dajax.assign('#msg_area', 'innerHTML', u'Ваш запрос отправлен! Копия запроса отправлена и вам. Ожидайте :)')

    #add record to db

    user_rec = UserMissedHours(user=user.id, umess=msg, date=dt, status=0, lock_person=0)
    user_rec.save()

    subject = u"[TT] Коррекция времени для %s %s " % (user.name, user.surname)
    message = u"Дата: %s \n\r Сообщение: \n\r %s \r\n" % (dt, msg)

    datatuple = ((subject, message, utils.TT_EMAIL_SYSTEM, [user.email]),)
    utils.mail(datatuple)

    subject = u"[TT] Скорректировать время для %s %s " % (user.name, user.surname)
    #very dirty hack
    if user.office == 'UL':
        message = u"Дата: %s \n\r Сообщение: \n\r %s \r\n Ссылка на редактирование часов: https://tt.ximad.com/user_requests/?missed_id=%s" % (dt, msg, user_rec.id)
    else:
        message = u"Дата: %s \n\r Сообщение: \n\r %s \r\n Ссылка на редактирование часов: https://tt.minsk.ximxim.com/user_requests/?missed_id=%s" % (dt, msg, user_rec.id)

    for office in offices:
        if user.office == office.short_name:
            datatuple = ((subject, message, utils.TT_EMAIL_SYSTEM, [office.boss_email]),(subject, message, utils.TT_EMAIL_SYSTEM, [utils.ROOT_EMAIL]),)

    utils.mail(datatuple)
    return dajax.json()

#######################################################################

@dajaxice_register
def add_new_assignment(request, dt, user, button_id):
    dajax = Dajax()

    #get project id
    if int(request.session['selected_project_assignment']) != 0:
        project_id = int(request.session['selected_project_assignment'])#random.randint(1, 9)
    else:
        dajax.alert(u"Выберите выше название проекта")

    if utils.save_user_assignment(dt, user, project_id):
        color = utils.get_project_color(project_id)
        dajax.script("$('#td_"+button_id+"').css({'background-color' : '"+color+"'})")

    else:
        dajax.script("$('#td_"+button_id+"').css({'background-color' : 'white'})")

    return dajax.json()

#######################################################################

@dajaxice_register
def apply_list_users_to_new_project(request, project_appended_employee):

    ids = project_appended_employee.split(',')

    userId = int(request.session['uid'])
    # me = User.objects.get(userId)
    projectAppendedEmployeeDoc = ProjectAppendedEmployeeDoc()
    projectAppendedEmployeeDoc.apllyEmployeeOnEmptyProject(userId, project_appended_employee)
    dajax = Dajax()
    msg = u"Список пользователей %s" % (project_appended_employee)
    dajax.assign('#msg_project', 'innerHTML', msg)

    return dajax.json()



# FIXME:  deprecated since 11 September 2014: Do not need to use it
@dajaxice_register
def add_new_project(
                    request
                    ,
                    project_name, project_desc,
                    project_desc_for_customer,


                    customer,
                    customer_feedback,
                    service,
                    industry,
                    solution_highlight,
                    development_tools_and_technologies,
                    development_time,
                    start_date,
                    finish_date,
                    project_is_in_pause
):
    dajax = Dajax()
    # userId = int(request.session['uid'])
    # l = MyLog().l()
    # p = MyLog().p()
    #
    # p(request, 'request')
    #
    # compareResult = MyDate().compare(start_date, finish_date, '/')
    # #  and (compareResult == 1 or compareResult == False)
    # # l(compareResult, 'compareResult')
    #
    #
    # employeeOnProject = ProjectAppendedEmployeeRoleDoc().getEmployeeIdsOnEmptyProject_(userId)
    #
    # if      (project_name != '' and employeeOnProject and (compareResult == 1 or compareResult == False)):
    #         # and (project_desc != '')\
    #         # and (customer != '')\  #  TODO: WHen select box was ready -- Un comment it
    #
    #     tempProjectId = TimecardTempProjects().getTempProjectIdByUserId(userId) # str
    #     project = TimecardProjects(
    #                 temp_project_id = tempProjectId,
    #                 project_name=project_name,
    #                 project_desc=project_desc,
    #                 project_desc_for_customer = project_desc_for_customer,
    #                 customer = customer,
    #                 customer_feedback = customer_feedback,
    #                 service = service,
    #                 industry = industry,
    #                 solution_highlight = solution_highlight,
    #                 development_tools_and_technologies = development_tools_and_technologies,
    #                 development_time = development_time,
    #                 start_date = start_date,
    #                 finish_date = finish_date,
    #                 project_is_in_pause = project_is_in_pause,
    #                 creator_id = userId,
    #                 project_opened=1
    #     )
    #
    #     insertedProjectId = project.getInsertedDocId()
    #
    #     if insertedProjectId != None:
    #         resultGenerationNewTempProjectId = TimecardTempProjects().generateNewTempProjectIdForUserId(userId) # str
    #         l(resultGenerationNewTempProjectId, 'resultGenerationNewTempProjectId')
    #
    #         resultDoc = ProjectAppendedEmployeeDoc().bindEmployeeToProject(userId, insertedProjectId)
    #         resultRoleDoc = ProjectAppendedEmployeeRoleDoc().bindEmployeeToProject(userId, insertedProjectId)
    #         resultFilesDoc = ProjectAppendedFilesDoc().bindFilesToProject(userId, insertedProjectId)
    #         projectCreationStatus = 1
    #
    #         msg = u"Новый проект [ %s ] добавлен [%s]" %(project_name, insertedProjectId)
    #         dajax.assign('#msg_area_project', 'innerHTML', msg)
    #         dajax.assign('#msg_hidden_project_create', 'innerHTML', projectCreationStatus)
    #     else:
    #         msg = u"Произошла ошибка при создании проекта"
    #         dajax.assign('#msg_area_project_error', 'innerHTML', msg)
    #
    # else:
    #     if not employeeOnProject:
    #         msg = u"Добавьте хотя бы одного человека на проект"
    #     else:
    #         msg = u"Заполните все поля помеченные звездочкой чтобы создать проект"
    #
    #     if type(compareResult) == int and compareResult == 0:
    #         msg = msg + u"<br> Дата старта и окончания проекта совпадают."
    #
    #     if compareResult == -1:
    #         msg = msg + u"<br> Неверные даты старта и окончания проекта."
    #
    #     dajax.assign('#msg_area_project_error', 'innerHTML', msg)
    #     # dajax.alert(u"Заполните все поля помеченные звездочкой чтобы создать проект")
    return dajax.json()

#######################################################################
@dajaxice_register
def add_new_user(request, user_name, user_surname, user_login, user_email, user_gender, user_dep, user_office, user_prof):
    dajax = Dajax()
    #then we have to check if user 'login' and 'email' value are unique:
    if not User.objects.filter(login = user_login) and not User.objects.filter(email = user_email):
        offices = Offices.objects.all()
        user = User(name=user_name, surname=user_surname, login=user_login, dep=user_dep, accessLevel=0, status=0,
                office=user_office, avator="", email=user_email, fb="", twitter="", skype="", hb="", phone="",
                gender=user_gender, ua="", counter01=0, profession=user_prof)
        user.save()
        subject = u"[TT] У нас на офисе появился новый сотрудник %s %s " % (user.name, user.surname)
        message = u"Новый сотрудник в нашем офисе: %s %s \n\r Отдел: %s" % (user.name, user.surname, user.dep)
        for office in offices:
            if user.office == office.short_name:
                datatuple = ((subject, message, utils.TT_EMAIL_SYSTEM, [office.mass_email]),)
                utils.mail(datatuple)
        msg = u"Новый пользователь %s %s добавлен" % (user_name, user_surname)
    else:
        msg = u"Логин %s и/или эл.почта %s уже заняты. Логин должен быть уникальным, выберите другой" % (user_login, user_email)
    dajax.assign('#msg_area_add_user', 'innerHTML', msg)

    return dajax.json()

#######################################################################

@dajaxice_register
def edit_user_data(request, uid):
    """
    This function is used for user data editing via admin page
    Actually it just print out the data to the forms and show button for saving
    """
    dajax = Dajax()
    user = User.objects.get(id = uid)
    dajax.script("$('#user_name').attr('value', '"+user.name+"')")
    dajax.script("$('#user_surname').attr('value', '"+user.surname+"')")
    dajax.script("$('#user_login').attr('value', '"+user.login+"')")
    dajax.script("$('#user_email').attr('value', '"+user.email+"')")
    dajax.script("$('#uid').attr('value', '"+str(uid)+"')")
    dajax.script('$("#user_edit_button_div").show();')
    dajax.script('$("#user_add_button_div").hide();')
    return dajax.json()

#######################################################################

@dajaxice_register
def edit_existing_user(request, user_name, user_surname, user_login, user_email, user_gender, user_dep, user_office, user_prof, uid):

    dajax = Dajax()
    user = User.objects.get(id = int(uid))
    #we have to keep logins and emails unique but we allow to use it again for the same user
    if (User.objects.filter(login=user_login) and user not in User.objects.filter(login=user_login)) or\
       (User.objects.filter(email=user_email) and user not in User.objects.filter(email=user_email)):
        msg = u"Логин %s и/или эл.почта %s уже заняты. Логин должен быть уникальным, выберите другой" % (user_login, user_email)
    else:
        user.name = user_name
        user.login = user_login
        user.email = user_email
        user.surname = user_surname
        user.gender = user_gender
        user.office = user_office
        user.dep = user_dep
        user.profession = user_prof
        user.save()
        msg = u"Пользовательские данные обновлены. Обновите страницу, чтобы увидеть изменения"
        dajax.script("$('#user_name').attr('value', '')")
        dajax.script("$('#user_surname').attr('value', '')")
        dajax.script("$('#user_login').attr('value', '')")
        dajax.script("$('#user_email').attr('value', '')")
        dajax.script('$("#user_edit_button_div").hide();')
        dajax.script('$("#user_add_button_div").show();')
    dajax.assign('#msg_area_add_user', 'innerHTML', msg)
    return dajax.json()

#######################################################################
@dajaxice_register
def add_new_dep_or_prof(request, data_name, data_type):
    """
    This function is used for adding new deps and professions to the DB.
    It is used for adding new:
    - Departments (to which one is user belonging),
    - Professions (what are user's main responsibilities),
    and
    - Standard project roles (what are user's main responsibilities on the some projects)
    """
    dajax = Dajax()
    if data_name=='':
        dajax.alert(u"Нельзя добавлять пустые наименования")
    else:
        if data_type == 'dep':
            UserDepartament(name=data_name).save()
            msg=''
            for dep in UserDepartament.objects.all():
                msg += "<tr><td><br/>" + dep.name + "<br/></td><td style='padding: 10px;'><a href='#dpp' onclick=\"Dajaxice.timecard.show_dpp_deletetion_confirmation_form(Dajax.process, {'data_id':" +str(dep.id)+ ", 'data_type':'dep'});\"><img src='"+settings.STATIC_URL+"css/images/del.png'/></a></td></tr>"
            dajax.assign('#deps_table', 'innerHTML', msg)
            dajax.assign('#dep_msg', 'innerHTML', u"Добавлен новый отдел "+data_name)
        if data_type == 'prof':
            UserProfession(name=data_name).save()
            msg=''
            for prof in UserProfession.objects.all():
                msg += "<tr><td><br/>" + prof.name + "<br/></td><td style='padding: 10px;'><a href='#dpp' onclick=\"Dajaxice.timecard.show_dpp_deletetion_confirmation_form(Dajax.process, {'data_id':" +str(prof.id)+ ", 'data_type':'prof'});\"><img src='"+settings.STATIC_URL+"css/images/del.png'/></a></td></tr>"
            dajax.assign('#profs_table', 'innerHTML', msg)
            dajax.assign('#prof_msg', 'innerHTML', u"Добавлена новая должность "+data_name)
        if data_type == "role":
            UserRoles(name=data_name).save()
            msg=''
            for role in UserRoles.objects.all():
                msg += "<tr><td><br/>" + role.name + "<br/></td><td style='padding: 10px;'><a href='#dpp'onclick=\"Dajaxice.timecard.show_dpp_deletetion_confirmation_form(Dajax.process, {'data_id':" +str(role.id)+ ", 'data_type':'role'});\"><img src='"+settings.STATIC_URL+"css/images/del.png'/></a></td></tr>"
            dajax.assign('#roles_table', 'innerHTML', msg)
            dajax.assign('#role_msg', 'innerHTML', u"Добавлена новая роль "+data_name)

    return dajax.json()

######################################################################
@dajaxice_register
def show_dpp_deletetion_confirmation_form(request, data_id, data_type):
    """
    This function is used as simple protection against accidental dep, profession or role deletion
    It is used for drawing confirmation form
    """
    dajax = Dajax()
    if data_type == 'dep':
        name = UserDepartament.objects.get(id = data_id).name
        msg = u"Пожалуйста, кликните на ссылку ниже, чтобы подтвердить свои действия:<br/><br/><a href = '/admin/?del_dep="\
              +str(data_id) + u"' style='color: red'>DELETE DEPARTMENT " + name + u"</a>"
    if data_type == 'prof':
        name = UserProfession.objects.get(id = data_id).name
        msg = u"Пожалуйста, кликните на ссылку ниже, чтобы подтвердить свои действия:<br/><br/><a href = '/admin/?del_prof="\
              +str(data_id) + u"' style='color: red'>DELETE PROFESSION " + name + u"</a>"
    if data_type == 'role':
        name = UserRoles.objects.get(id = data_id).name
        msg = u"Пожалуйста, кликните на ссылку ниже, чтобы подтвердить свои действия:<br/><br/><a href = '/admin/?del_role="\
              +str(data_id) + u"' style='color: red'>DELETE ROLE " + name + u"</a>"
    dajax.assign('#dpp', 'innerHTML', msg)
    return dajax.json()

#####################################################################
@dajaxice_register
def show_user_deletetion_confirmation_form(request, uid):
    """
    This function is used as simple protection from accidental user deletion.
    This function is used for drawing user deletion confirmation form
    """
    dajax = Dajax()
    user = User.objects.get(id = uid)
    # before allow admin to delete user we have to check that user has no objects reserved by him
    if Reservation_Objects.objects.filter(is_avaliable=False, user=user):
        msg = u"Данный пользователь согласно журналу бронирования взял что-то в пользование и пока еще не вернул. " \
              u"Прежде чем этот пользователь будет удален из системы, он должен вернуть все, что взялы."
    else:
        msg = u"Пожалуйста, кликните на ссылку ниже, чтобы подтвердить свои действия:<br/><br/><a href = '/admin/?del_user="+\
              str(uid)+u"' style='color: red'>DELETE ACCOUNT ("+user.name+u" "+user.surname+u")</a>"
    dajax.assign('#user_deletion_dummy_protection', 'innerHTML', msg)

    return dajax.json()

#######################################################################
@dajaxice_register
def show_project_deletetion_confirmation_form(request, pid):
    dajax = Dajax()
    project = Projects.objects.get(id=pid)
    msg = u"Пожалуйста, кликните на ссылку ниже, чтобы подтвердить свои действия:<br/><br/><a href = '/projects/?close_project="+ \
          str(pid) + u"' style='color: red'>CLOSE PROJECT (" + project.project_name + u")</a>"
    dajax.assign('#pddp', 'innerHTML', msg)
    return dajax.json()

#######################################################################
@dajaxice_register
def save_user_settings(request, uid, user_hb, user_skype, user_twitter, user_fb, user_phone):
    dajax = Dajax()
    user = User.objects.get(id=uid)
    user.hb=user_hb
    user.skype=user_skype
    user.twitter=user_twitter
    user.fb=user_fb
    user.phone=user_phone
    user.save()
    msg = u"Ваши данные обновлены"
    dajax.assign('#msg_area', 'innerHTML', msg)

    return dajax.json()

#######################################################################
@dajaxice_register
def save_new_report(request, choosen_project, uid, report, feedback, hours ,week_hours):
    """
    This function is calling when user post new weekly report.
    """
    dajax = Dajax()
    user = User.objects.get (id = uid)
    msg = utils.check_user_report (choosen_project,uid,report,feedback, hours)
    dajax.assign('#msg_area','innerHTML','')
    #
    if msg:
        dajax.alert(msg)
    else:
        report_date=datetime.date.today().strftime("%d/%m/%Y")  #current date of report posting
        report_week=datetime.date.today().isocalendar()[1]      #number of current week
        report_year=datetime.date.today().strftime("%Y")        #current year number
        r = Reports(user_id = uid, report = report, employee_feedback = feedback, project_name = choosen_project, lead_feedback = "Empty", week = report_week, year = report_year, office = user.office, dep = user.dep, reporting_date = report_date, hours = int(hours), user_name = user.name, user_surname = user.surname)
        r.save()
        dajax.script("$('#report').attr('value','')")
        dajax.script("$('#feedback').attr('value','')")
        dajax.script("$('#hours').attr('value','')")
        dajax.assign('#msg_area','innerHTML', u"Вы добавили недельный отчет!<br/>Обновите страницу, чтобы увидеть изменения")
        # OK. We successfully added new report but now we have to check if user reports this week are overtimed
        utils.check_overtime(report_week,report_year, uid, week_hours)
    return dajax.json()

@dajaxice_register
def change_report(request, rid):
    """
    This function is used when user wants to change data from his/her week report
    It fills up appropriate fields of page with the report data and enable button for
    updating, BUT DO NOT DO ANY CHANGES TO DB!
    """
    dajax = Dajax()
    r = Reports.objects.get(id=rid)
    dajax.script("$('#report').attr('value','"+r.report+"')")
    dajax.script("$('#feedback').attr('value','"+r.employee_feedback+"')")
    dajax.script("$('#hours').attr('value','"+str(r.hours)+"')")
    dajax.script("$('#rid').attr('value', '"+str(rid)+"')")
    dajax.assign('#msg_area','innerHTML','')
    dajax.script('$("#update_report_div").show();')
    dajax.script('$("#save_new_report_div").hide();')
    dajax.script('$("#select_div").hide();')
    dajax.assign('#project_div','innerHTML','PROJECT: '+r.project_name+'')
    return dajax.json()

@dajaxice_register
def update_report(request, rid, report, feedback, hours, week_hours):
    """
    This function actually do the updating. It reads the fields from page and updating the record and
    informs the user about result
    """
    dajax=Dajax()
    r = Reports.objects.get(id = int(rid))
    msg = utils.check_user_report (r.project_name,r.user_id,report,feedback, hours, True)
    if msg:
        dajax.alert(msg)
    else:
        r.report = report
        r.employee_feedback = feedback
        r.hours = int(hours)
        r.save()
        dajax.assign('#msg_area','innerHTML',u"Вы успешно обновили ваш отчет!<br/>Обновите страницу, чтобы увидеть изменения")
        dajax.script('$("#update_report_div").hide();')
        dajax.script('$("#save_new_report_div").show();')
        dajax.script('$("#select_div").show();')
        dajax.script("$('#hours').attr('value','')")
        dajax.script("$('#report').attr('value','')")
        dajax.script("$('#feedback').attr('value','')")
        dajax.assign('#project_div','innerHTML','')
        # We updated the reports and now have to calculate spent hours to check overtimes
        utils.check_overtime(r.week,r.year, r.user_id, week_hours)
    return dajax.json()


@dajaxice_register
def show_report(request, rid,old_rid):
    """
    This function is calling when a lead click the report in the list.
    """
    dajax=Dajax()
    msg,lf = utils.show_report(rid)
    #on click we show the hidden forms: report/feedback area and lead feedback submition form...
    dajax.script('$("#div_update_lead_feedback").show();')
    dajax.script('$("#msg_area").show();')
    # ...then show the current lead feedback...
    dajax.script("$('#update_lead_feedback').attr('value', '"+lf+"')")
    # ...assign current report record id for further calls...
    dajax.script("$('#rid').attr('value', '"+str(rid)+"')")
    # ...show the actual report...
    dajax.assign('#msg_area','innerHTML',msg)
    # ...and finally highlight report record line
    dajax.script("$('#report_line_"+str(old_rid)+"').attr('style','color:#000000; font-style:normal;')")
    dajax.script("$('#report_line_"+str(rid)+"').attr('style','color:#6666FF; font-style:italic;')")
    return dajax.json()

@dajaxice_register
def update_lead_feedback(request, rid,feedback,uid):
    """
    This function is calling when lead update his/her feedback.
    It updates the lead_feedback and hides the report viewing and feedback editing forms
    """
    dajax = Dajax()
    msg, new_lf = utils.update_lead_feedback(int(rid),feedback,uid)
    # on click we update DB with submited lead feedback and hide forms
    dajax.alert(msg)
    dajax.script('$("#div_update_lead_feedback").hide();')
    dajax.script('$("#msg_area").hide();')
    # after lead feedback updating we would not redraw the whole page, instead we redraw only one cell
    dajax.assign("#leadfeedback_"+rid,'innerHTML',new_lf)
    dajax.script("$('#report_line_"+str(rid)+"').attr('bgcolor','#F7F7F7')")
    return dajax.json()

@dajaxice_register
def add_vote(request, question, yes, no, dontcare, office):
    """
    This function is calling when admin add new voting.
    All votings are separated by office and will be available only for users from appropriate offices.
    Also when admin add new voting the previous one is going to become 'archived'. It means the archived voting
    is hidden from users and avaliable from admin page for deleting. Also when the new voting is created the user's
    'voted' flag is set to 0 to allow to vote again.
    """
    dajax = Dajax()
    try:
        if len (question)>100 or len(yes)>20 or len (no)>20 or len(dontcare)>20 or not (question or no or yes or dontcare):
            dajax.assign("#msg_area_votes",'innerHTML',u'Поля вопроса и вариантов ответов не должны быть пусты, длины'
                                                       u'текстов не должны быть слишком велики (<100 для вопроса) или слишком мала <20!)')
        else:
            # first we set the 'archived' flag for the current last voting
            try:
                last_vote = Votes.objects.filter(office=office).latest('id')
                last_vote.archived = 1
                last_vote.save()
            except:
                pass
            # and next we create new voting
            dajax.assign("#msg_area_votes",'innerHTML',u'Новое голосование добавлено и будет отображаться в качестве текущего. Обновите страницу, чтобы увидеть изменения')
            vote = Votes(question = question,votes_yes_desc = yes, votes_no_desc = no, votes_dontcare_desc = dontcare, votes_dontcare = 0, votes_yes= 0, votes_no = 0, office = office, archived = 0,votes_yes_who ='',votes_no_who ='',votes_dontcare_who ='')
            vote.save()
            # and update the user voting status
            User.objects.filter(office = office).update(voted = 0)
    except Exception,e:
        dajax.assign("#msg_area_votes",'innerHTML','Error: '+str(e))
    return dajax.json()

@dajaxice_register
def vote(request,vote_id, opinion, uid):
    """
    Here is a voting function. It updates the 'user.voted' flag and increment counters in voting results.
    Also our voting are not truly anonymous:) Guys who has access to admin page (user.accessLevel = 2 (ADMIN) or
    3 (ROOT)) can view the history of votes. That is why our voting records are stored in DB with names of voted
    users in fields 'votes_dontcare_who', 'votes_yes_who' and 'votes_no_who'.
    """
    dajax=Dajax()
    try:
        user = User.objects.get(id = uid)
        if not user.voted:
            vote = Votes.objects.get(id = vote_id)
            if opinion == 'yes':
                vote.votes_yes +=1
                user.voted = 1
                if vote.votes_yes_who == '':# first record
                    vote.votes_yes_who +=str(uid)
                else:
                    vote.votes_yes_who +=' ' + str(uid)#if not first record add a space before uid
            if opinion =='no':
                vote.votes_no +=1
                user.voted = 2
                if vote.votes_no_who == '':
                    vote.votes_no_who +=str(uid)
                else:
                    vote.votes_no_who +=' ' + str(uid)
            if opinion =='dontcare':
                vote.votes_dontcare +=1
                user.voted = 3
                if vote.votes_dontcare_who == '':
                    vote.votes_dontcare_who +=str(uid)
                else:
                    vote.votes_dontcare_who +=' ' + str(uid)
            vote.save()
            user.save()
            # reinit the object again to get the latest data
            vote = Votes.objects.get(id = vote_id)
            dajax.assign("#yes_vote", 'innerHTML',str(vote.votes_yes))
            dajax.assign("#no_vote", 'innerHTML',str(vote.votes_no))
            dajax.assign("#dontcare_vote", 'innerHTML',str(vote.votes_dontcare))

        else:
            dajax.alert(u'Вы уже проголосовали. Обновите страницу, если изменения не отображаются')
    except Exception, e:
        dajax.assign("#votings_div",'innerHTML',str(e))
    return dajax.json()


@dajaxice_register
def show_voting_details(request, voting_id, show_or_hide):
    """
    That function draw a table with names of voted employees
    for the later posting it to tha admin page via ajax 'partial POST'
    """
    dajax= Dajax()
    if int(show_or_hide):#'show_or_hide' == 1 so we have to hide div with voting details
        dajax.assign("#secret_votings_results",'innerHTML','')
        dajax.script("$('#vsh').attr('value','0')")
    else:
        try:
            voting = Votes.objects.get (id = voting_id)

            if voting.votes_yes_who:
                persons_voted_yes = voting.votes_yes_who.split(' ')
                list_yes = []
                for temp in persons_voted_yes:
                    user = User.objects.get(id = int(temp))
                    list_yes.append(user.name+' '+user.surname)
                persons_voted_yes= "</br>".join(list_yes)
            else:
                persons_voted_yes = ''

            if voting.votes_no_who:
                persons_voted_no = voting.votes_no_who.split(' ')
                list_no=[]
                for temp in persons_voted_no:
                    user = User.objects.get(id = int(temp))
                    list_no.append(user.name+' '+user.surname)
                persons_voted_no= "</br>".join(list_no)
            else:
                persons_voted_no = ''

            if voting.votes_dontcare_who:
                persons_voted_dontcare = voting.votes_dontcare_who.split(' ')
                list_dontcare =[]
                for temp in persons_voted_dontcare:
                    user = User.objects.get(id = int(temp))
                    list_dontcare.append(user.name+' '+user.surname)
                persons_voted_dontcare= "</br>".join(list_dontcare)
            else:
                persons_voted_dontcare=''

            dajax.assign ("#secret_votings_results",'innerHTML',"<table width='100%' cellpadding='1' cellspacing='1'><em><h5>"+voting.question+"</h5></em><col width='50' /><col width='50' /><col width='50'/><tr><td bgcolor='#CCFFCC'><strong>"+voting. votes_yes_desc+":</strong><br/><br/>"+persons_voted_yes+"</td><td bgcolor='#FFCCCC'><strong>"+voting.votes_no_desc+":</strong><br/><br/>"+persons_voted_no+"</td><td bgcolor='#FFFFCC'><strong>"+voting.votes_dontcare_desc+":</strong><br/><br/>"+persons_voted_dontcare+"</td></tr></table>")
            dajax.script("$('#vsh').attr('value','1')")
        except Exception, e:
            dajax.assign ("#secret_votings_results",'innerHTML',str(e))
    return dajax.json()


################################################################################
# here is a block of select updating functions

@dajaxice_register
def updatecombo1 (request, select_project,d2,d3):
    """
    Is used for user assignment on the project
    This function chooses project in projects page. If at the moment also the user is chosen for a project
    it will activate the button for user assignment for a project
    """
    dajax=Dajax()
    project = Projects.objects.get(id = select_project)
    dajax.assign ('#assignment_area','innerHTML','')
    dajax.assign ('#unassignment_area','innerHTML','')
    dajax.assign('#project_area','innerHTML','Set: '+project.project_name)
    if d2 and d3:
        dajax.script("$('#assignment_button').attr('disabled', false)")
    return dajax.json()

@dajaxice_register
def updatecombo2 (request, select_dep):
    """
    Is used for user assignment on the project
    This function updates the options in select for departments in projects page and and reinit
    the data for user select on the page. Also it will automatically drop the chosen user on the page
    (if any at this moment)
    """
    dajax = Dajax()
    dajax.assign ('#assignment_area','innerHTML','')
    dajax.assign ('#unassignment_area','innerHTML','')
    dajax.assign ('#dep_area','innerHTML','Set: '+select_dep)
    users = User.objects.filter (dep = select_dep).order_by('surname')
    options ='<option selected="selected" disabled="disabled">...</option>'
    for user in users:
        options+="<option value='"+str(user.id)+"'>"+user.surname + ' '+user.name+"</option>"
    dajax.assign('#select_user','innerHTML',options)
    dajax.assign('#user_area','innerHTML','')
    dajax.script("$('#assignment_button').attr('disabled', true)")
    return dajax.json()

@dajaxice_register
def updatecombo3 (request, select_user,d1,d2,d3 ):
    """
    Is used for user assignment on the project
    This function chooses user in select in projects page. If at the moment also the project and role are chosen
    it will activate the button for user assignment for a project
    """
    dajax = Dajax()
    dajax.assign ('#assignment_area','innerHTML','')
    dajax.assign ('#unassignment_area','innerHTML','')
    user = User.objects.get(id = int(select_user))
    dajax.assign ('#user_area','innerHTML','Set: '+user.surname + ' ' + user.name)
    if d1 and d2 and d3:
        dajax.script("$('#assignment_button').attr('disabled', false)")
    return dajax.json()

@dajaxice_register
def updatecombo4 (request, select_project):
    """
    Is used for user removing from the project
    This function enumerates projects with previously assigned users and (re)init tha data for user selection
    Also if user was chosen for removing at this moment it will drop choice
    """
    dajax = Dajax()
    project = Projects.objects.get(id = select_project)
    dajax.assign ('#assignment_area','innerHTML','')
    dajax.assign ('#unassignment_area','innerHTML','')
    dajax.assign('#project_area_unassign','innerHTML','Set: '+project.project_name)
    assigned_users_ids = ProjectThread.objects.filter(who_unassigned='',project_id = int(select_project)).values_list('user_id', flat = True).distinct()
    users = User.objects.filter (id__in = assigned_users_ids).order_by('surname')
    options = '<option selected="selected" disabled="disabled">...</option>'
    for user in users:
        options+="<option value='"+str(user.id)+"'>"+user.surname + ' '+user.name+"</option>"
    dajax.assign('#select_user_unassign','innerHTML',options)
    dajax.assign('#user_area_unassign','innerHTML','')
    return dajax.json()

@dajaxice_register
def updatecombo5 (request, select_user ,d1):
    """
    Is used for user removing from the project
    This function is choosing users from assigned projects and activating button for unassignig them
    """
    dajax = Dajax()
    dajax.assign ('#assignment_area','innerHTML','')
    dajax.assign ('#unassignment_area','innerHTML','')
    user = User.objects.get (id = int(select_user))
    dajax.assign ('#user_area_unassign','innerHTML','Set: '+user.surname + ' ' + user.name)
    if d1:
        dajax.script("$('#unassignment_button').attr('disabled', false)")
    return dajax.json()

@dajaxice_register
def updatecombo6 (request, select_role, d1, d2, d3):
    """
    Is used for setting user role for the project
    """
    dajax = Dajax()
    role = UserRoles.objects.get(id = int(select_role))
    dajax.assign ('#role_area','innerHTML','Set: '+role.name)
    if d1 and d2 and d3:
        dajax.script("$('#assignment_button').attr('disabled', false)")
    return dajax.json()

@dajaxice_register
def assign_project (request, uid, pid ,me, role):
    """
    This function make new project assignment. It actually store the record about new assignment if
    this user is not already assigned for this project. Also it stores data about the person who
    made project assignment
    """
    #TODO: not to check if user already assigned but just do not allow assignment via page forms
    dajax = Dajax()
    project_manager = User.objects.get (id = me)
    assigned_user = User.objects.get (id = int(uid))
    # first we have to check if we already have assignment for the user in project
    threads = ProjectThread.objects.filter(user_id = int (uid), project_id = int (pid), who_unassigned = '')
    if threads:
        dajax.assign ('#assignment_area','innerHTML',u'Сотрудник уже назначен на проект')
    else:
        ProjectThread(user_id = int (uid), user_name_surname = (assigned_user.surname + ' ' + assigned_user.name),
                      project_id = int(pid), who_assigned = (project_manager.surname + ' ' + project_manager.name),
                      who_unassigned = '', user_role = role).save()
        dajax.assign ('#assignment_area','innerHTML',u'Вы назначили сотрудника на проект. Обновите страницу, чтобы увидеть изменения')
    return dajax.json()

@dajaxice_register
def unassign_project (request, uid, pid, me):
    """
    This function just remove user assignment from project. It not just delete record (because we want to have history)
    but just updating the flag 'who_unassigned' - it empty if assignment is active and it stores the name of project
    manager who removed the employee from project.
    Also when we have a weird situation when user is periodically is assigned/unassigned for the same project we do not
    store history about all that jumps in and out. Instead we always store only two states: 'is currently assigned'
    and 'is now removed from project'. When the user is unassigned we just looking for the old records and updating them
    with the new 'who_unassigned' data.
    """
    dajax = Dajax()
    try:
        project_manager = User.objects.get (id = me)
        old_thread = ProjectThread.objects.exclude(who_unassigned = '').filter(user_id = int (uid), project_id = int(pid)).values_list('id',flat = True).distinct()
        thread = ProjectThread.objects.filter(who_unassigned = '', user_id = int (uid), project_id = int(pid)).values_list('id', flat = True).distinct()
        thread = ProjectThread.objects.get(id = sum(thread))
        if old_thread:
            old_thread = ProjectThread.objects.get (id =sum(old_thread))
            thread.who_assigned = old_thread.who_assigned
            thread.who_unassigned = project_manager.surname + ' '+project_manager.name
            thread.save()
            old_thread.delete()
        else:
            thread.who_unassigned = project_manager.surname + ' '+project_manager.name
            thread.save()

        dajax.assign ('#unassignment_area','innerHTML',u"Вы сняли сотрудника с проекта! Обновите страницу, чтобы увидеть изменения")
    except Exception,e:
        dajax.assign ('#unassignment_area','innerHTML',"Error!" + str(e))
    return dajax.json()







@dajaxice_register
def show_detailed_statistics (request, pid, vsh ):
    """
    This function shows the hidden div with common statistics about project, calculates data for individual hours
    and post it via ajax in the template
    """
    # print request



    print pid

    dajax = Dajax()
    if int(vsh): #if we have some statistics already shown
        if int(vsh)!=pid: # and if we clicked to show another div
            dajax.script("$('#project_div_"+vsh+"').hide();")
            dajax.script("$('#project_div_"+str(pid)+"').show();")
            dajax.script("$('#vsh').attr('value','"+str(pid)+"');")
            text = utils.fill_up_statistics_table (pid)
            dajax.assign("#individual_hours_table_for_"+str(pid)+"","innerHTML",text)
        else:#we just clicked same div and now have to hide it
            dajax.script("$('#project_div_"+str(pid)+"').hide();")
            dajax.script("$('#vsh').attr('value','"+str(0)+"');")
    else: #if we do not have anything to show
        dajax.script('$("#project_div_'+str(pid)+'").show();')
        dajax.script("$('#vsh').attr('value','"+str(pid)+"');")
        text = utils.fill_up_statistics_table (pid)
        dajax.assign("#individual_hours_table_for_"+str(pid)+"","innerHTML",text)
    return dajax.json()







@dajaxice_register
def add_new_office(request, full_name, short_name, boss_email,mass_email,time_shift,weather_script):
    """
    This function is used for creation new office. Also we checking first for unique names for full and short names
    because we want full name just be unique for clearance and better look and the short name MUST BE UNIQUE because we
    using it for user's records filtering in a different situations.
    """
    dajax = Dajax()
    try:
        existing_offices_short = Offices.objects.filter(short_name = short_name)
        existing_offices_full = Offices.objects.filter(full_name = full_name)
        if existing_offices_short or existing_offices_full:
            dajax.assign('#msg_area_office', 'innerHTML', u'Вы должны использовать уникальные имена для офисов!')
        else:
            office = Offices(full_name = full_name, short_name = short_name, boss_email = boss_email, mass_email = mass_email, time_shift = time_shift, weather_script = weather_script)
            office.save()
            dajax.assign('#msg_area_office', 'innerHTML', u'Новый офис ' +full_name +u' добавлен!')
    except Exception, e:
        dajax.alert('Error!: '+str(e))
    return  dajax.json()