#########################################################################
# TimeCard ajax requests
# author Alex Bogdanovich
# 2012 
#########################################################################

# -*- coding: utf-8 -*-

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.template.loader import render_to_string
from timecard.models import User, UserTime, UserPost, UserPostComment, CalendarDaysOff, UserMissedHours, Boss_notice
from timecard import utils
import settings
import os
from django.shortcuts import render_to_response
from django.template import RequestContext
import random
import datetime

#######################################################################

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
	    print "Error: could not create directory to upload files!"
	    return "Error: could not create directory to upload files!"
	
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
def add_report_project(request, next_id):
    
    dajax = Dajax()

    inc_id = int(next_id) + 1
    
    dajax.alert(next_id)
    #dajax.script("$('#add_report_project_button').attr('title', '"+inc_id+"')")
    #dajax.alert("$('#add_report_project_button').attr('title')")
    

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
    str3 = "Team: %s<br/>" % (user.dep)
    str4 = "Phone: %s<br/>" % (user.phone)
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
def save_user_time(request):
    dajax = Dajax()
    
    year = datetime.date.today().year
    month = datetime.date.today().month
    day = datetime.date.today().day
    tdate =  "%d-%02d-%02d" % (year, month, day)
    
    try:
	uid = request.session['uid']
	
	status = utils.save_user_time(request, int(uid))
	last_diff = status[1]
	
	if status[0]:
	    user_info = '<form method="post"> <input type="button" name="user_time" id="user_time" onclick="Dajaxice.timecard.save_user_time(Dajax.process);" class="onoffbutton_in"/> </form>'
	    dajax.script('$("#counter_form").show();')
	    if utils.check_duty(tdate, int(uid)):
		dajax.alert('You are on duty today! Please keep the kitchen clean :)')
	else:
	    user_info = '<form method="post"> <input type="button" name="user_time" id="user_time" onclick="Dajaxice.timecard.save_user_time(Dajax.process);" class="onoffbutton_out"/> </form>'
	    dajax.script('$("#counter_form").hide();')
	    if utils.check_duty(tdate, int(uid)):
		dajax.alert('You are on duty today! Please check our kitchen before leaving the office! :) Thanks!')
	
	dajax.assign('#user_time_block', 'innerHTML', user_info)
	
	dajax.script('$("#user_time").hide();')
	
	
	
	if last_diff > 0:
	    animated_time_info = '<b style="color: red; font-size: 40px;">+%s</b>' % (last_diff)
	    dajax.assign('#animated_time', 'innerHTML', animated_time_info)
	    dajax.script('$("#animated_time").show();')
	    dajax.script('$("#animated_time").animate({ opacity: 0, top: "-=150"}, 2000, function() { $(this).hide(); $(this).css({"top" : "350", "opacity":"100", "display": "none"}); });')
	    
    
	dajax.script('$("#user_time").show();')
	nowtime = utils.get_unix_datetime()
	localtime = utils.convert_unix_date("time", nowtime)
	
	
	dajax.assign('#user_time_area', 'innerHTML', localtime)
    except:
	dajax.alert('Please refresh the page and try again.')

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
	msg = "avatar is updated"
	dajax.assign('#msg_area_pic', 'innerHTML', msg)
    
    except:
	dajax.alert('Please refresh the page and try again.')

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
def set_day_off(request, dt):
    dajax = Dajax()

    
    dayoff = dict(c_yearoff=dt[:4], c_monthoff=dt[5:7], c_dayoff=dt[8:10])
    #print dayoff
    if utils.save_calendar_dayoff(dayoff):
        msg = "Day off is set: %s" % dt
    else:
        msg = "Already set for this day! Revert and set as working day: %s" % dt

    dajax.assign('#msg_area', 'innerHTML', msg)

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
    subject = "[TT] corrected hours"
    message = "Your hours were corrected! \n\r Your request at [ %s ] with message: \n %s" % (record_data.date, record_data.umess)
    
    #get user db data
    user = User.objects.get(id=record_data.user)
    
    datatuple = (
	    (subject, message, utils.TT_EMAIL_SYSTEM, [user.email]),
    )
    
    utils.mail(datatuple)
    
    record_data.status = 1
    record_data.save()
    
    dajax.script("$('#"+button_id+"').hide()")
    dajax.assign('#msg_area_editor', 'innerHTML', 'User is informed! Time correction is done. <a href="/user_requests/">BACK</a>')
        
    return dajax.json()

#######################################################################
    
@dajaxice_register
def add_corrected_time(request, uid, date, time):
    dajax = Dajax()
    
    try:
	#time has simple hh:mm - need convert into YYY-MM-DD HH:MM:SS -> int format
	sdate = date.split("-")
	stime = time.split(":")
	
	yy = int(sdate[0])
	mm = int(sdate[1])
	dd = int(sdate[2])
	h = int(stime[0])
	m = int(stime[1])
	
	dt = datetime.datetime(yy,mm,dd,h,m)
	dt = dt - datetime.timedelta(hours=3) #GMS+3 offset for UTC time
	
	sdate = dt.strftime('%Y-%m-%d %H:%M')
	corrected_time = utils.get_unix_strdtime(sdate)
	
	utime = UserTime(user_id=uid, time=corrected_time)
	utime.save()
	#dajax.alert(utime.id)
	
	#get the list of updated hours
	
	#and add all of these hours into the new div list
	msg = '<div style="display: inline; background-color: #FF9999; padding: 5px; width: 60px; height: 10px; border: groove 1px gray;">%02d:%02d</div>&nbsp;' % (h,m)
	dajax.append('#missed_time_area', 'innerHTML', msg)
    except ValueError:
	dajax.alert('Minutes or hours are wrong! Hours [0..23], minutes [0..59]')
	
    return dajax.json()    

#######################################################################
    
@dajaxice_register
def change_user_dep(request, uid, button_id, button_id2, dep):
    dajax = Dajax()

    user = User.objects.get(id=uid)
    user.dep = dep
    user.save()
    
    dajax.script("$('#"+button_id+"').hide()")
    dajax.assign('#'+button_id2, 'innerHTML', dep)
    dajax.script("$('#"+button_id2+"').show()")
        
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
    time.delete()
    
    dajax.assign('#'+button_id, 'innerHTML', '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
    dajax.script("$('#"+button_id+"').hide()")
        
    return dajax.json()    

#######################################################################

@dajaxice_register
def make_root(request, uid, button_id):
    dajax = Dajax()

    user = User.objects.get(id=uid)
    #send request
    user.accessLevel = 3 # make root
    user.save()
    dajax.alert(user.login + ' accesslevel is 3')
    
    dajax.script("$('#"+button_id+"').hide()")
        
    return dajax.json()

#######################################################################
    
@dajaxice_register
def make_admin(request, uid, button_id):
    dajax = Dajax()

    user = User.objects.get(id=uid)
    #send request
    user.accessLevel = 2 # make admin
    user.save()
    dajax.alert(user.login + ' accesslevel is 2')
    
    dajax.script("$('#"+button_id+"').hide()")
        
    return dajax.json()

#######################################################################
    
@dajaxice_register
def make_boss(request, uid, button_id):
    dajax = Dajax()

    user = User.objects.get(id=uid)
    #send request
    user.accessLevel = 1 # make boss
    user.save()
    dajax.alert(user.login + ' accesslevel is 1')
    
    dajax.script("$('#"+button_id+"').hide()")
        
    return dajax.json()

#######################################################################
    
@dajaxice_register
def make_user(request, uid, button_id):
    dajax = Dajax()

    user = User.objects.get(id=uid)
    #send request
    user.accessLevel = 0 # make user
    user.save()
    dajax.alert(user.login + ' accesslevel is 0')
    
    dajax.script("$('#"+button_id+"').hide()")
        
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
    dajax.assign('#msg_area', 'innerHTML', 'Your notice is saved. Please refresh the page.')
    
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
    #send request
    
    dajax.script('$("#dialog_correct_my_hours").hide();')
    dajax.assign('#msg_area', 'innerHTML', 'Your request is sent! The copy of request is sent to you. Wait please :)')
    
    #add record to db
    
    user_rec = UserMissedHours(user=user.id, umess=msg, date=dt, status=0, lock_person=0)
    user_rec.save()
    
    subject = "[TT] correct time for %s %s " % (user.name, user.surname)
    message = "Date: %s \n\r Message: \n\r %s \r\n" % (dt, msg)
    
    if user.office == "M":
	datatuple = (
	    (subject, message, utils.TT_EMAIL_SYSTEM, [user.email]),
	)
	
    else:
	datatuple = (
	    (subject, message, utils.TT_EMAIL_SYSTEM, [user.email]),
	)
    
    utils.mail(datatuple)
    
    subject = "[TT] correct time for %s %s " % (user.name, user.surname)
    message = "Date: %s \n\r Message: \n\r %s \r\n Edit user hours: https://tt.minsk.ximxim.com/user_requests/?missed_id=%s" % (dt, msg, user_rec.id)
    
    if user.office == "M":
	datatuple = (
	    (subject, message, utils.TT_EMAIL_SYSTEM, [utils.BOOS_EMAIL_MINSK]),
	    (subject, message, utils.TT_EMAIL_SYSTEM, [utils.ROOT_EMAIL]),
	)
	
    else:
	datatuple = (
	    (subject, message, utils.TT_EMAIL_SYSTEM, [utils.BOOS_EMAIL_GOMEL]),
	    (subject, message, utils.TT_EMAIL_SYSTEM, [utils.ROOT_EMAIL]),
	)
    
    utils.mail(datatuple)    
    
    
    return dajax.json()    

#######################################################################

@dajaxice_register
def add_new_user(request, user_name, user_surname, user_login, user_email, user_gender, user_dep, user_office):
    dajax = Dajax()
    
    user = User(name=user_name, surname=user_surname, login=user_login, dep=user_dep, accessLevel=0, status=0, office=user_office, avator="", email=user_email, fb="", twitter="", skype="", hb="", phone="", gender=user_gender, ua="", counter01=0)
    user.save()
    
    subject = "[TT] new user %s %s " % (user.name, user.surname)
    message = "New employee at your office: %s %s \n\r Team: %s" % (user.name, user.surname, user.dep)
    
    if user.office == "M":
	datatuple = (
	    (subject, message, utils.TT_EMAIL_SYSTEM, [utils.MINSK_MAIL_LIST]),
	)
	
    else:
	datatuple = (
	    (subject, message, utils.TT_EMAIL_SYSTEM, [utils.GOMEL_MAIL_LIST]),
	)
    
    utils.mail(datatuple)    
    
    
    msg = "New user %s %s is added" % (user_name, user_surname)
    dajax.assign('#msg_area', 'innerHTML', msg)

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
    msg = "settings are updated"
    dajax.assign('#msg_area', 'innerHTML', msg)

    return dajax.json()

#######################################################################    
    