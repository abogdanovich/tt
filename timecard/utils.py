# -*- coding: utf-8 -*-
#########################################################################
# TimeCard utils module
# author Alex Bogdanovich
# 2012
#
# This module contains differnet supportive functions. Most of them are calling from
# ajax.py module. Some of them (as decorators, for example) are calling from views.py
#
#########################################################################

from timecard.models import User, UserTime, UserPost, UserPostComment, CalendarDaysOff, UserModule, UserMissedHours, Boss_notice, User_duty, Projects, UserProjectAssignments, Reports, ProjectThread, Offices
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.conf import settings
from django.core.mail import BadHeaderError, send_mass_mail
import calendar
import datetime
import time
import ldap
import pytz
import Image, ImageFilter, ImageDraw
import operator
import itertools
import socket
import random
import logging
from timecard.app_classes.MyLog import *
#########################################################################

#Global tt settings

TIMEZONE = "Europe/Minsk"
SPAM_PAGE_MSG = 5
PERSONAL_TABLE_CELLS = 10

TT_EMAIL_SYSTEM = "TT notification"

ROOT_EMAIL = "myurkin@minsk.ximxim.com"

#########################################################################

# decorator for all timecard.views pages - login required - check that user is logged

def check_access_level(list_of_allowed_levels):
    def real_decorator(func):
        def wrapper(request, *args, **kwargs):
            try:
                user = User.objects.get(id = int(request.session['uid']))
                if user.accessLevel not in list_of_allowed_levels:
                    logging.debug("access: user tried to load denied page: " + user.login)
                    return redirect('/main/')
                else:
                    return func(request, *args, **kwargs)
            except Exception, e:
                logging.debug("access_error: "+str(e))
        return wrapper
    return real_decorator

def login_required(func):
    def wrapper(request, *args, **kw):

        try:
            if request.session['uid'] != '':
                acceuser = User.objects.get(id=int(request.session['uid']))

                if request.session['ip'] != '':
                    user_ip_new = request.META['REMOTE_ADDR']
                    user_ip_old = request.session['ip']

                    if user_ip_new != user_ip_old:

                        preStr = 'login_required\login: different user access: '
                        logging.debug(preStr + "login [ " + acceuser.login + ']' )
                        logging.debug(preStr + "old ip [ " + user_ip_old + ']' )
                        logging.debug(preStr + "new ip [ " + user_ip_new + ']' )

                        error_message = u"Ваш текущий IP адрес отличается от предыдущего, перелогиньтесь :)"
                        logging.debug("login_required\login: different user access: re-auth")
                        request.session.flush()
                        return render_to_response(
                            'timecard/login.html',
                            {
                                'error_message':error_message
                            },
                            context_instance=RequestContext(request)
                        )
                else:
                    request.session['ip'] = request.META['REMOTE_ADDR']
                    preStr = 'login_required\login: different user access: '
                    logging.debug( preStr + "ip is empty - saving... : " + acceuser.login)
                    logging.debug( preStr + "save user ip: " + request.session['ip'])
            results = func(request, *args, **kw)
            return results
        except KeyError:
            error_message = u"Введите логин и пароль"
            return render_to_response(
                    'timecard/login.html',
                    {
                        'error_message':error_message
                    },
                    context_instance=RequestContext(request)
            )
    return wrapper

# this is checker: report must be put in Friday, Saturday or Sunday
# and also user must be assigned for any project
def reporting_conditions_check(func):
    def condcheck(request, *args, **kwargs):
        if datetime.date.today().isoweekday() in [5,6,7]:
            ttuser = User.objects.get(id=int(request.session['uid']))
            projects_assigned = ProjectThread.objects.filter(user_id = ttuser.id, who_unassigned = '')
            if projects_assigned:
                return func(request, *args, **kwargs)
            else:
                return redirect('/main/')
        else:
            return redirect('/main/')
    return condcheck

# not used ?
def timer(f):
    def tmp(*args, **kwargs):
        t = time.time()
        res = f(*args, **kwargs)
        print "Working function time : %f" % (time.time()-t)
        return res
    return tmp

#########################################################################
# check user missed hours counter


def get_user_missedh_counts(uid):
    user = User.objects.get(id=uid)
    users_from_whom_show_requests = User.objects.filter(office = user.office).values_list('id', flat=True).distinct()
    missed_hours = UserMissedHours.objects.filter(status = 0, user__in=users_from_whom_show_requests).count()

    return missed_hours

#########################################################################

# check user spam counter

def get_user_spam_counts(uid):
    user = User.objects.get(id=uid)
    spam_records = UserPost.objects.all().count()

    return spam_records - user.counter01


def set_user_spam_counts(uid):
    user = User.objects.get(id=uid)
    spam_records = UserPost.objects.all().count()
    user.counter01 = spam_records
    user.save()

    return spam_records

#########################################################################

# get User Agent string

def updateUA(uid, ua):
    user_agent = User.objects.get(id=uid)
    user_agent.ua = ua
    user_agent.save()

    return True

#########################################################################

# get User Agent string

def getUA(request):

    UA = request.META['HTTP_USER_AGENT']
    UA.lower()
    user_browser = ""

    if "Firefox" in UA:
        user_browser = "Mozilla Firefox"
    elif "Chrome" in UA:
        user_browser = "Google Chrome"
    elif "Safari" in UA:
        user_browser = "Apple Safari"
    elif "Opera" in UA:
        user_browser = "Opera"
    elif "Netscape" in UA:
        user_browser = "Netscape"
    elif "MSIE" in UA:
        user_browser = "Internet Explorer"
    else:
        user_browser = "Unknown"

    return user_browser

#########################################################################

# prepare | sort and regroup masse of dicts

def group_list(dic_list):

    dic_list.sort(key=operator.itemgetter('date'))

    # group the dates in lists
    list1 = []
    for key, items in itertools.groupby(dic_list, operator.itemgetter('date')):
	list1.append(list(items))

    sum_timelist = []
    sum_timelist = calc_user_day_hours(list1)

    return list1


def group_list_stat(dic_list):

    dic_list.sort(key=operator.itemgetter('hour'))

    # group the dates in lists
    list1 = []
    for key, items in itertools.groupby(dic_list, operator.itemgetter('hour')):
	list1.append(list(items))


    return list1

def group_list_stat_ua(dic_list):

    dic_list.sort(key=operator.itemgetter('ua'))

    # group the dates in lists
    list1 = []
    for key, items in itertools.groupby(dic_list, operator.itemgetter('ua')):
	list1.append(list(items))


    return list1

def group_list_spam(dic_list):

    #dic_list.sort(key=operator.itemgetter('id'))

    # group the dates in lists
    list1 = []
    for key, items in itertools.groupby(dic_list, operator.itemgetter('id')):
	list1.append(list(items))


    return list1

def group_list_teams(dic_list):

    dic_list.sort(key=operator.itemgetter('dep'))

    # group the dates in lists
    list1 = []
    for key, items in itertools.groupby(dic_list, operator.itemgetter('dep')):
	list1.append(list(items))


    return list1

def group_list_duty(dic_list):

    dic_list.sort(key=operator.itemgetter('name', 'surname'))

    # group the dates in lists
    list1 = []
    for key, items in itertools.groupby(dic_list, operator.itemgetter('userid')):
	list1.append(list(items))


    return list1


def group_list_xim_assignment(dic_list):

    dic_list.sort(key=operator.itemgetter('name', 'surname'))

    # group the dates in lists
    list1 = []
    for key, items in itertools.groupby(dic_list, operator.itemgetter('userid')):
	list1.append(list(items))


    return list1

#########################################################################

# PIL office statistic: visiting

def draw_office_visiting(user_list, gday):

    year = datetime.date.today().year
    month = datetime.date.today().month

    start_date = make_month_date(year, month, int(gday), "start")
    end_date = make_month_date(year, month, int(gday), "end")

    instat = []
    outstat = []

    for i in range(0,25):
	instat.append({'hour': "%2d" % i, 'counts': 0})

    for i in range(0,25):
	outstat.append({'hour': "%2d" % i, 'counts': 0})

    for u in user_list:
	usertime = UserTime.objects.filter(user_id=u.id, time__range=(start_date, end_date)).order_by('time') # from the 1st dat of the current month
	i = 0
	for k in usertime:
	    #get all user hours - need to get the first time rec
	    userin = convert_unix_date('stattime', k.time)
	    i += 1
	    if i % 2 == 0: #user is out
		#in_stat append
		outstat.append({'hour': userin, 'counts': 1})
	    else:
		#in_stat append
		instat.append({'hour': userin, 'counts': 1})

    in_peoples = []
    instat = group_list_stat(instat)

    out_peoples = []
    outstat = group_list_stat(outstat)

    num = 0
    for day in outstat:
        for visits in day:
	    if visits['counts'] != 0:
		num+=1
	out_peoples.append(num)
	num = 0

    num = 0
    for day in instat:
        for visits in day:
	    if visits['counts'] != 0:
		num+=1
	in_peoples.append(num)
	num = 0


    filename = "%stt_data/visit_stat.jpg" % (settings.MEDIA_ROOT)

    pic_size = 530,230
    size = 510,210

    im = Image.new('RGB', pic_size)
    draw = ImageDraw.Draw(im)
    draw.rectangle((0,0,pic_size[0]-1,pic_size[1]-1), fill="#FFFFFF")

    draw.line((5, 220, 5, 5), fill="#707070", width=1)
    draw.line((5, 220, 520, 220), fill="#707070", width=1)

    for i in range(0,25):
	draw.text((i*20,220), "%2d" % i, fill="#000000")

    hours = 0
    oldx = 10
    oldy = size[1]-10
    count = 0

    for prixod in in_peoples:
	count = prixod

	x = hours*20
	y = size[1]-prixod-10
	if x!=0:
	    draw.line((x, y, x, 200), fill="#006600", width=20)
	if count != 0:
	    draw.text((x-5,y-10), "%d" % count, fill="#000000")

	oldx = x
	oldy = y
	hours += 1

    hours = 0
    oldx = 10
    oldy = size[1]-50
    count = 0
    for prixod in out_peoples:
	count = prixod

	x = hours*20
	y = size[1]-prixod-110

	if x!=0:
	    draw.line((x, y, x, 100), fill="#CC0000", width=20)
	if count != 0:
	    draw.text((x-5,y-10), "%d" % count, fill="#000000")
	oldx = x
	oldy = y
	hours += 1

    draw.line((10, 10, 20, 10), fill="#006600", width=1)
    draw.text((25,5), "in", fill="#006600")

    draw.line((10, 20, 20, 20), fill="#CC0000", width=1)
    draw.text((25,15), "out", fill="#CC0000")


    im.save(filename, quality=100)

#########################################################################


#########################################################################

# PIL office statistic: browsers

def draw_office_browsers():

    #get all users

    user_list = User.objects.all()
    ualist = []

    #add them to the common list and sort by UA strings....
    for u in user_list:
	if u.ua != "":
	    ualist.append({'ua': u.ua, 'counts': 1})

    total_users = len(user_list)

    ualist = group_list_stat_ua(ualist)
    out_ua = []

    num = 0
    for ua_list in ualist:
        for ua in ua_list:
	    if ua['counts'] != 0:
		num+=1
	out_ua.append({'ua': ua['ua'], 'counts': num})
	num = 0



    filename = "%stt_data/ua_stat.jpg" % (settings.MEDIA_ROOT)

    pic_size = 530,230
    size = 510,210

    im = Image.new('RGB', pic_size)
    draw = ImageDraw.Draw(im)
    draw.rectangle((0,0,pic_size[0]-1,pic_size[1]-1), fill="#000000")
    draw.rectangle((1,1,pic_size[0]-2,pic_size[1]-2), fill="#FFFFFF")

    #draw.line((5, 220, 5, 5), fill="#707070", width=1)
    #draw.line((5, 220, 520, 220), fill="#707070", width=1)
    i = 0

    for ua in out_ua:
	i += 10
	persent_int = ua['counts'] * 100 / total_users
	persent = str(ua['counts'] * 100 / total_users) + "%"
	rand_color = "%s%s%s%s%s%s" % (random.randint(1,9), random.randint(1,9), random.randint(1,9), random.randint(1,9), random.randint(1,9), random.randint(1,9))
	draw.text((10,10+i*2), "%s - %s" % (ua['ua'], persent), fill="#%s" % (rand_color))
	draw.line((10, 25+i*2, 10+persent_int*5, 25+i*2), fill="#%s" % (rand_color), width=2)




    im.save(filename, quality=100)

#########################################################################

# PIL resize func

def img_resize(imageFile):

    size = 120,120
    im = Image.open(imageFile)
    if im.size[0] > 120 or im.size[1] > 120:
	im.thumbnail(size, Image.ANTIALIAS)

    im.save(imageFile, quality=100)

    return True

#########################################################################

# PIL save func

def img_save(infile, outfile):

    im = Image.open(infile)
    im.save(outfile, quality=100)

    return True

#########################################################################

# PIL save func

def img_rotate(infile):

    im = Image.open(infile)
    im2 = im.rotate(-90)
    im2.save(infile, quality=100)

    return True

#########################################################################

# PIL filter

def img_filters(infile, filter_name):

    im = Image.open(infile)

    if filter_name == "BLUR":
	im2 = im.filter(ImageFilter.BLUR)
    elif filter_name == "CONTOUR":
	im2 = im.filter(ImageFilter.CONTOUR)
    elif filter_name == "DETAIL":
	im2 = im.filter(ImageFilter.DETAIL)
    elif filter_name == "EDGE_ENHANCE":
	im2 = im.filter(ImageFilter.EDGE_ENHANCE)
    elif filter_name == "EMBOSS":
	im2 = im.filter(ImageFilter.EMBOSS)
    elif filter_name == "FIND_EDGES":
	im2 = im.filter(ImageFilter.FIND_EDGES)
    elif filter_name == "SMOOTH":
	im2 = im.filter(ImageFilter.SMOOTH)
    elif filter_name == "SHARPEN":
	im2 = im.filter(ImageFilter.SHARPEN)

    im2.save(infile, quality=100)

    return True

#########################################################################

# PIL add fon

def img_addfon(infile, img_addfon):

    im = Image.open(infile)
    im2 = Image.open(img_addfon)

    if im.size[0] < im2.size[0]:
	dx = im2.size[0] - im.size[0]
	im2.paste(im,(dx, 0))
    else:
	im2.paste(im,(0, 0))
    im2.save(infile, quality=100)

    return True
#########################################################################

# get month num days | default params are current year & month

def get_month_days(year=datetime.date.today().year, month=datetime.date.today().month):

    num_days = calendar.monthrange(year, month) #weekday|num days of month

    return num_days[1]

#########################################################################

# get working month num days | default params are current year & month

def get_working_month_days(office, year=datetime.date.today().year, month=datetime.date.today().month):

    total_month_days = get_month_days(year, month)
    #logging.debug("debug: total_month_days: >>>>>>>>>> " + total_month_days)
    #current month
    start_date = make_month_date(year, month, 1, "start")
    #logging.debug("debug: start_date: >>>>>>>>>> " + start_date)
    #end of cur month
    end_date = make_month_date(year, month, total_month_days-1, "end")
    #logging.debug("debug: end_date: >>>>>>>>>> " + end_date)

    num_days_off = CalendarDaysOff.objects.filter(date__range=(start_date, end_date),office=office).count()
    #print "num_days_off %s " % num_days_off

    #logging.debug("debug: num_days_off: >>>>>>>>>> " + num_days_off)
    return total_month_days - num_days_off

#########################################################################

# calculate user required work time

def get_required_time(user_id):

    user_office = User.objects.get(id = user_id).office
    month_w_days = get_working_month_days(user_office)
    user_time = calc_total_month_hours(user_id, datetime.date.today().month, datetime.date.today().year)

    # 1 hours = 3600 seconds -each day = 8 working hours => convert to make diff operation between total working days\hours-seconds
    # and user total wroked hours\seconds

    total_month = month_w_days * 8 * 3600
    timediff = total_month-user_time

    return timediff


#########################################################################

# send mail function

def mail(datatuple):

    try:
        hostname = socket.gethostname()
        if hostname == 'wwwloc.dmz':
            send_mass_mail(datatuple)
        else:
            pass
    except BadHeaderError:
        return 0

    return 1

#########################################################################

# generate user data using selected day

def make_month_date(year, month, day, startend):

    dt = datetime.datetime.today()
    start_date = dt.replace(year=year, month=month, day=day, hour=00, minute=00)
    start_date = start_date - datetime.timedelta(hours=3) #GMT -3 because of UTC format
    end_date = start_date + datetime.timedelta(days=1)

    if startend == "start":
	sdt = start_date.strftime('%Y-%m-%d %H:%M')
    else:
	sdt = end_date.strftime('%Y-%m-%d %H:%M')

    return int(time.mktime(time.strptime(sdt, "%Y-%m-%d %H:%M")))

#########################################################################
# TODO: do we allow remote users only to be stored in minsk LDAP?
def is_remote_user(user, l):

    is_remote = False

    baseDN = "ou=groups,dc=minsk,dc=ximxim,dc=com"
    searchScope = ldap.SCOPE_SUBTREE
    retrieveAttributes = None
    searchFilter = "cn=Remote-Users"

    try:
	ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
	result_set = []
	result_set = l.result(ldap_result_id, 1)
	remote_users = result_set[1][0][1]['memberUid']

	for u in remote_users:
	    if user == u:
		is_remote = True
		break
    except ldap.LDAPError, e:
	#print e
	return False

    return is_remote

# check user account in LDAP DB

def check_ip(user_ipd, username, l):


    status = True
    ## TODO: do not strictly use certain mask. Instead we have to add some flexibility and first find IP of our server
    ## and then take the mask from it.
    if user_ipd[0] != '192' and user_ipd[1] != '168':
        if user_ipd != ['127', '0', '0', '1']:
        #allowed only from PC from local network and localhost
            logging.debug("check_ip\ldap: REMOTE ACCESS from user: " + username)

            #remote access - checking remote access
            if is_remote_user(username, l):
                logging.debug("check_ip\ldap: remote access is allow for user: " + username)

            else:
                logging.debug("check_ip\REMOTE ACCESS!: user tried to login as a remote user: " + username)
                logging.debug("check_ip\ldap: remote access is DENIED for user: " + username)
                status = False

    return status


def ldap_check(request, username=None,password=None):
    status = False
    length = len(password);
    passwordStr = False
    if isinstance(password, basestring):
        passwordStr = True
    if passwordStr and length > 0:
        # we try to find user info in LDAP directories allowed in settings.AD_LDAP
        for currentldap in settings.AD_LDAP:
            if not status:
                try:
                    binddn = "uid=%s,%s" % (username, currentldap['LDAP_SEARCH_DN'])
                    l = ldap.initialize(currentldap['LDAP_URL'])
                    l.protocol_version = ldap.VERSION3
                    l.set_option(ldap.OPT_REFERRALS, 0)
                    status = check_ip(request.META['REMOTE_ADDR'].split('.'), username, l)
                    l.simple_bind_s(binddn, password)
                    l.unbind_s()
                except ldap.LDAPError:
                    status = False
    return status
#########################################################################

# check user account in TimeTrack system

def tt_accountcheck(request, username):
    try:
        user = User.objects.get(login=username)
    except User.DoesNotExist:
        logging.debug("tt_accountcheck\login: tt base has no user : " + username)
        return 0
    request.session['uid'] = user.id
    user_ip = request.META['REMOTE_ADDR']
    request.session['ip'] = user_ip
    logging.debug("tt_accountcheck\login: new user session: " + user_ip)

    return 1

#########################################################################

# save calendar days off

def save_calendar_dayoff(dayoff, office):

    flag = 0
    #convert to int
    int_day_off = make_month_date(int(dayoff['c_yearoff']), int(dayoff['c_monthoff']), int(dayoff['c_dayoff']), "start")
    #save into db
    try:
        day_rec = CalendarDaysOff.objects.get(date=int_day_off, office=office)
        day_rec.delete()
    except CalendarDaysOff.DoesNotExist:
        day_rec = CalendarDaysOff(date=int_day_off, office=office)
        day_rec.save()
        flag = 1

    return flag


#########################################################################
# save duty day

def save_duty_user(date, user):

    flag = 0

    try:
	day_rec = User_duty.objects.get(date=date, user=user)
	day_rec.delete()
    except User_duty.DoesNotExist:
	day_rec = User_duty(date=date, user=user)
	day_rec.save()
	flag = 1

    return flag

#########################################################################
def get_project_color(project_id):

    color = Projects.objects.get(id=project_id)

    return color.project_color

#########################################################################
# save save_user_assignment day

def save_user_assignment(date, user, project_id):

    flag = 0

    try:
	day_assign_rec = UserProjectAssignments.objects.get(date=date, user=user)
	day_assign_rec.delete()
    except UserProjectAssignments.DoesNotExist:
	day_assign_rec = UserProjectAssignments(date=date, user=user, project=project_id)
	day_assign_rec.save()
	flag = 1

    return flag

#########################################################################

# save user submitted time into DB

def save_user_time(uid):

    user = User.objects.get(id=uid)
    timeshift = int(Offices.objects.get(short_name = user.office).time_shift)
    # here we have to do a correction and store in DB not actually server time but users's local time
    # because all the users may be situated in different timezones.
    #
    # Also we have to subtract GMS +3 hours because server is in that timezone and we want to be based
    # on the local server time

    NOW = int(round(time.time()))+timeshift - 3 * 3600
    utime = UserTime(user_id=user.id, time=NOW)
    utime.save()

#########################################################################
def get_user_state(uid):

    user = User.objects.get(id=uid)
    timeshift = int(Offices.objects.get(short_name = user.office).time_shift)
    NOW = int(round(time.time()))+timeshift - 3*3600

    year=int(time.strftime ('%Y', time.gmtime(NOW)))
    month=int(time.strftime ('%m', time.gmtime(NOW)))
    day=int(time.strftime ('%d', time.gmtime(NOW)))

    rangetime = make_month_date(year, month, day, "start")

    num = UserTime.objects.filter(user_id=uid, time__gte=rangetime).count() #get user time records starting from the current day

    #add try except block - to determine any possible errors!
    if num % 2 == 0: #check user status by submitted time records
        ustatus = 0
    else:
        ustatus = 1

    return ustatus

#########################################################################

# save user submitted time into DB

def save_spam_comment(request, post_id, comment_body):

    userpost = UserPost.objects.get(id=post_id)
    comment_body = comment_body
    ucomment = UserPostComment(author=int(request.session['uid']), post_id=userpost.id, body=comment_body)
    ucomment.save()

    #update post date
    #format: YYYY-MM-DD HH:MM:SS 2012-03-26 15:39:47
    #dt = datetime.datetime.utcnow()
    dt = get_unix_datetime()
    #sdate = dt.strftime('%Y-%m-%d %H:%M:%S')
    sdate = convert_unix_date('update_post_datetime', dt)
    userpost.created = sdate
    userpost.save()

    return ucomment.created

#########################################################################

# save user submitted time into DB

def save_spam_post(request, post_body, post_author):

    post = UserPost(author=post_author, body=post_body)
    post.save()

    return True

#########################################################################

# get the list of user active modules

def set_modules(user, module_name):

    #try to get user module - if none - then create a record

    try:
	mod = UserModule.objects.get(user_id=user, mod=module_name, position="right") #position is hardcoded
	if mod.show == 0:
	    mod.show = 1
	    mod.save()
	else:
	    mod.show = 0
	    mod.save()
    except UserModule.DoesNotExist:
	mod = UserModule(user_id=user, mod=module_name, position="right", show=1)
	mod.save()

    if mod.show == 1:
	return True
    else:
	return False

#########################################################################

# get the list of user active modules

def get_modules(user, module_name):

    #try to get user module - if none - then create a record

    state = False

    try:
	mod = UserModule.objects.get(user_id=user, mod=module_name, position="right") #position is hardcoded
	if mod.show == 0:
	    state = False
	else:
	    state = True

    except UserModule.DoesNotExist:
	state = False

    return state

#########################################################################
#get boss notices for concrete user date
def get_boss_notice(_user, _date):
    #print "boss notice get func"
    #notice = " "
    try:
	boss_notice = Boss_notice.objects.get(user=_user, date=_date)
	if boss_notice.notice != "":
	    notice = boss_notice.notice

    except:
	notice = " "
    #print "notice: %s" % (notice)
    return notice

#set boss notices for concrete user date
def set_boss_notice(_user, _date, _notice):

    boss_notice = Boss_notice(user=_user, date=_date, notice=_notice)
    boss_notice.save()

    return boss_notice.notice

#########################################################################

# check that day is "dayOFF"

def check_day_off(year, month, day, office):

    check_date = make_month_date(int(year), int(month), int(day), "start")
    day_is_off = CalendarDaysOff.objects.filter(date__startswith=check_date, office=office).count()

    if day_is_off:
        return True

    return False

#########################################################################
# check that day is marked as "project assignment"

def check_resource_assignment(dt, user_id):

    try:
        user_project = UserProjectAssignments.objects.get(user=int(user_id), date=dt)
	if user_project != []:
	    return user_project.project
	else:
	    return 0
    except UserProjectAssignments.DoesNotExist:
        return 0

#########################################################################
#get hours list for the selected day
def get_selected_day_hours(uid, year, month, day):

    start_date = make_month_date(year, month, day, "start")
    end_date = make_month_date(year, month, day, "end")

    #make selection from DB to get all hours for concrete day
    day_hours = UserTime.objects.filter(user_id=uid, time__range=(start_date, end_date)).order_by('time')
    #print day_hours

    #print day_hours

    hours_list = []

    for dh in day_hours:
        dh_time = convert_unix_date('time', dh.time)
        #print dh_time
        hours_list.append({'user_id': uid, 'time_id': dh.id, 'time': dh_time})

    #print hours_list

    return hours_list
#########################################################################
# get user hours only for this month and convert for template preview [small django hack to show data: t1 t2 t3.... etc in the table]
#@timer #show the real function working time
def show_user_month_hours(uid, _month, _year):

    year = _year
    month = _month

    month_days = get_month_days(year, month)

    tuser = User.objects.get(id=uid)

    utime = []

    d = datetime.date.today()
    day_today = d.strftime("%Y-%m-%d")

    for i in range(1, month_days+1):

	today = False
	tdate =  "%d-%02d-%02d" % (year, month, i)
	weekday = datetime.date(year, month, i)
	weekday = weekday.strftime("%A")

	day_off = check_day_off(year, month, i, tuser.office)

	if day_today == tdate:
	    today = True

	#check and get boss notices for that user
	#print "%s %s " % (tuser.id, tdate)
	boss_notice = get_boss_notice(tuser.id, tdate)

	utime.append({'date': tdate, 'time':"0", 'timeid':"0", 'sum':False, 'notice': boss_notice, 'weekday': weekday, 'dayoff': day_off, 'today':today}) #push all days into month array

    #pprint.pprint(utime)

    start_date = make_month_date(year, month, 1, "start") #start month
    end_date = make_month_date(year, month, month_days, "end") #end month

    usertime = UserTime.objects.filter(user_id=tuser.id, time__range=(start_date, end_date)).order_by('time') # from the 1st dat of the current month

    for dt in usertime:
        tdate = convert_unix_date('date', dt.time)
        #check_day = check_day_off(year, month, tdate[-2:])
        ttime = convert_unix_date('time', dt.time)
        utime.append({'date': tdate, 'time':ttime, 'timeid':dt.id, 'sum':False})

    #utime.sort()

    return group_list(utime)

#########################################################################
#check duty stuff
def check_duty(date, user):

    is_duty = User_duty.objects.filter(date=date, user=user).count()

    if is_duty:
        return True

    return False

#########################################################################

def show_duty_month_users(_year, _month, office):

    year = _year
    month = _month

    month_days = get_month_days(year, month)

    users = User.objects.filter(office=office).order_by("surname").order_by("name")

    uduty = []

    for u in users:

	uduty.append({'date': 0, 'name': u.name, 'surname': u.surname,  'is_duty': 0, 'userid': u.id}) #push all days into month array

	for i in range(1, month_days+1):

	    day_off = check_day_off(year, month, i, u.office)
	    if not day_off:
		tdate =  "%d-%02d-%02d" % (year, month, i)
		sdate =  "%02d" % (i)
		is_duty = False
		is_duty = check_duty(tdate, u.id)

		uduty.append({'date': tdate, 'name': u.name, 'surname': u.surname, 'is_duty': is_duty, 'userid': u.id, 'sdate': sdate }) #push all days into month array

		#pprint.pprint(uduty)

    return group_list_duty(uduty)

#########################################################################

def show_xim_resources_assignment(_year, _month, group):

    year = _year
    month = _month
    today = datetime.date.today().day
    month_days = get_month_days(year, month)


    if group == "wireless":
	users = User.objects.filter(group="wireless").exclude(dep="BOSS").exclude(dep="XIM PM").order_by("surname").order_by("name").order_by("dep")
    elif group == "ps":
	users = User.objects.filter(group="ps").exclude(dep="BOSS").exclude(dep="XIM PM").order_by("surname").order_by("name").order_by("dep")
    else:
	users = User.objects.all().order_by("surname").exclude(dep="BOSS").exclude(dep="XIM PM").order_by("name").order_by("dep")

    xim_projects = []

    for u in users:

	#user_month_seconds = calc_total_month_hours(int(u.id), month)
        #user_month_time = convert_seconds(user_month_seconds)

	xim_projects.append({'date': 0, 'name': u.name, 'surname': u.surname, 'dep': u.dep,  'project_id': 0, 'userid': u.id, 'tdcolor': 'white' }) #push all days into month array


	for i in range(1, month_days+1):

	    day_off = check_day_off(year, month, i, u.office)
	    if not day_off:

		tdate =  "%d-%02d-%02d" % (year, month, i)
		sdate =  "%02d" % (i)

		if int(sdate) == int(today):
		    is_today = True
		else:
		    is_today = False

		project_id = check_resource_assignment(tdate, u.id)

		if project_id != 0:
		    color = get_project_color(project_id)
		else:
		    color = "white"
		xim_projects.append({'date': tdate, 'name': u.name, 'surname': u.surname, 'dep': u.dep, 'project_id': project_id, 'userid': u.id, 'sdate': sdate, 'tdcolor': color, 'is_today': is_today }) #push all days into month array

    return group_list_xim_assignment(xim_projects)

#########################################################################

def get_last_day_of_month(year, month):

    if month == 12:
	year += 1
	month = 1
    else:
        month += 1
    return datetime.date(year, month, 1) - datetime.timedelta(1)

#########################################################################

# get and calculate all user day hours for each day and show in personal tab
#@timer #show the real function working time
def calc_user_day_hours(listd):

    sum_list = []
    sum_list = listd
    #pprint.pprint(sum_list)

    for items in sum_list:
	i = 0
	temp_secs = 0
	sum_secs = 0
	num = 0

	for day in items:
	    #convert time into INT
	    day_temp = day['date']
	    num += 1

	    if day['time'] != "0":
		curtime_secs = get_unix_strdtime(day['date']+" "+day['time']) #calculate all hours for each day in INT format
		i += 1
		if i % 2 == 0:
		    sum_secs += curtime_secs - temp_secs
		else:
		    temp_secs = curtime_secs

	#add empty cells to the table

	for k in range (i,PERSONAL_TABLE_CELLS):
	    items.append({'date': day_temp, 'time': "emp", 'timeid':"0", 'sum':False})

	#convert sum_secs into readable format
	if num > 1:
		
	    #Stanislav Dobrovolsky requirements: 02.02.2015 : each working day is: 8.30 (not more)
	    #8.30h = 8 hours + 30 min = eg: 8 hours = 8*60*60 = 28800 seconds + 30 * 60 = 28800 + 1800 seconds = 30600 working seconds each day is available
	    #need to check if user working seconds not more than 30600!
	
	    #new updates: on Mar 1 2017 - it should be no more than 8. hours and 10 minutes.... so (8*60+10)*60=29400
	
	    if sum_secs > 29400:
	    	sum_secs = 29400
		#set limited seconds for working day for each user
		
	    sum_user_day_time = convert_seconds(sum_secs) #return int format into readable eg: secs into min:sec format
	    items.append({'date': day_temp, 'time': sum_user_day_time, 'timeid':"0", 'sum':True})
	else:
	    items.append({'date': day_temp, 'time': "emp", 'timeid':"0", 'sum':True})

    #pprint.pprint(sum_list)

    return sum_list

#########################################################################

def calc_today_user_hours(uid, date):
    day = date
    year = datetime.date.today().year
    month = datetime.date.today().month

    start_date = make_month_date(year, month, day, "start")
    end_date = make_month_date(year, month, day, "end")

    day_hours = UserTime.objects.filter(user_id=uid, time__range=(start_date, end_date)).order_by('time')

    i = 0
    temp_secs = 0
    sum_secs = 0

    #calculate all hours for each day
    for dt in day_hours:
	i += 1
	if i % 2 == 0:
	    sum_secs += dt.time - temp_secs
	else:
	    temp_secs = dt.time

    total_user_secs = sum_secs

    return total_user_secs



# get and calculate all user month hours for each day
#@timer #show the real function working time
def calc_total_month_hours(uid, _month, _year):

    dt = datetime.date.today()
    days = dt.day # do we need it?
    year = dt.year
    month = dt.month

    if month != _month or year != _year:
        days = calendar.monthrange(_year,_month)[1]
        month = _month
        year = _year

    total_user_secs = 0

    for i in range(1,days+1):
	#index shift +1 because start position in for cycle from 0
	#create date range to find the list of hours for appropriate day

        start_date = make_month_date(year, month, i, "start")
	end_date = make_month_date(year, month, i, "end")

	#make selection from DB to get all hours for concrete day
        day_hours = UserTime.objects.filter(user_id=uid, time__range=(start_date, end_date)).order_by('time')
	#pprint.pprint(day_hours)

        i = 0
        temp_secs = 0
        sum_secs = 0

	#calculate all hours for each day
        for dt in day_hours:
            i += 1
            if i % 2 == 0:
                sum_secs += dt.time - temp_secs
            else:
                temp_secs = dt.time
	    #print "time: %s" % dt.time

        total_user_secs += sum_secs
	#print total_user_secs

    return total_user_secs

#########################################################################

# check hb for selected day

def get_hb_list(date):
    return User.objects.filter(hb=date)

#########################################################################

# seconds into hh:mm converter

def convert_seconds(secs):

    total   = secs
    hours   = total / 3600
    total   = total - (hours * 3600)
    mins    = total / 60

    return "%02d:%02d" % (hours, mins)

#########################################################################

# convert str datetime into UNIX (int) format

def get_unix_strdtime(dtime):

    return int(time.mktime(time.strptime(dtime, "%Y-%m-%d %H:%M")))

#########################################################################

# convert UTCNOW datetime into UNIX format

def get_unix_datetime():

    dt = datetime.datetime.utcnow()
    sdate = dt.strftime('%Y-%m-%d %H:%M')
    server_time = int(time.mktime(time.strptime(sdate, "%Y-%m-%d %H:%M")))
##    if uid == None:
##        corrected_time = server_time
##    else:
##    # we have now correct time in seconds for server. now we have to correct it and show accordingly to the user time (timezone). We have to add/substract some timeshift stored in settings.py as TIME_SHIFT_FOR_OFFICES
##        user= User.objects.get(id = uid)
##        corrected_time = server_time + int(TIME_SHIFT_FOR_OFFICES[user.office])
    return server_time

#########################################################################

# convert UNIX timestamp format into datetime

def convert_unix_date(sel, timestamp):
    if sel == 'date':
        dt_obj = datetime.datetime.fromtimestamp(timestamp)
        #return pytz.timezone(TIMEZONE).fromutc(dt_obj).strftime("%a %m-%d")
        return pytz.timezone(TIMEZONE).fromutc(dt_obj).strftime("%Y-%m-%d")
    elif sel == 'time':
        dt_obj = datetime.datetime.fromtimestamp(timestamp)
        return pytz.timezone(TIMEZONE).fromutc(dt_obj).strftime("%H:%M")
    elif sel == 'stattime':
        dt_obj = datetime.datetime.fromtimestamp(timestamp)
        return pytz.timezone(TIMEZONE).fromutc(dt_obj).strftime("%H")
    else:
        dt_obj = datetime.datetime.fromtimestamp(timestamp)
        return pytz.timezone(TIMEZONE).fromutc(dt_obj).strftime("%Y-%m-%d %H:%M")

#########################################################################
# add new weekly report
def check_user_report (choosen_project,uid,report,feedback, hours, need_update=False):
    """
    This function is calling when you try to post new report or to update the existing one.
    It serves only for validating data: not too much or too less texting, 1 report per 1 project per 1 week and so on
    """
    msg = ''
    try:

        # only one report for current week and project
        if not need_update:
            report_week=datetime.date.today().isocalendar()[1]      #number of current week
            report_year=datetime.date.today().strftime("%Y")        #current year number
            my_this_week_reports=Reports.objects.filter(week=report_week, year = report_year, user_id = uid, project_name =choosen_project )
            if my_this_week_reports:
                msg = u"На этой неделе вы уже оставили отчет по данному проекту. Выберите другой проект."
        # max size of our report is limited by model.py
        if len(report)>10000 or len(feedback)>10000:
            msg = u"ОГО! Да ваш отчет в длину более 10000 символов! Вы думаете, это кто-то станет читать? :) Сократите отчет"
        #prevent sending tiny and useless report
        if len (report)<20 or len (feedback)<20:
            msg = u"Ваш отчет совершенно крошечный и неинформативный (<20 символов). Добавьте больше сведений о проделанной работе"
        # user must choose project first
        if choosen_project == "Choose project...":
            msg = u'Вы не выбрали проект'
        # user must place spent hours
        try:
            hours = int(hours)
            if hours<1:#employee set 0 or negative number
                msg = u"Самый умный? :) Выставь количество отработанных часы БОЛЬШЕ ноля"
        except:
            msg = u"Выставьте количество часов цифрами, не используйте текст и не оставляйте поле пустым"
        ###########
    except Exception,e:
        # any error?
        msg = "Error! "+str(e)
    return  msg

def check_overtime(report_week,report_year, uid, week_hours):
    """
    This function is used for checking for overtime for week reports. If sum of hours per week user put in reports
    is above of sum of working hours this function updating reports records and set the overtime value to 'overtimed'
    field. If no overtime is found 'overtimed' field is updating to 0 to show that everything is OK
    """
    user_week_reports = Reports.objects.filter(week = report_week, year = report_year, user_id = uid)
    if user_week_reports:
        list_of_hours = user_week_reports.values_list('hours',flat=True).distinct()
        if sum(list_of_hours)>week_hours:
            user_week_reports.update(overtimed = sum(list_of_hours))
        else:
            user_week_reports.update(overtimed = 0)

def show_report(rid):
    """
    This function is calling from ajax.py when lead tries to view employee reports.
    It actually returns the report data for later posting it via ajax 'partial POST'
    """
    try:
        report=Reports.objects.get(id = rid)
        #add some HTML formating to the outcome message
        msg="<strong>"+report.user_name+" "+report.user_surname+". "+report.project_name+". "+report.year+"/"+report.week+u"</strong><br/><br/>ОТЧЕТ: "+report.report+"<br/><br/>"+u"ОТЗЫВ ЛИДА: "+report.employee_feedback
        lf = report.lead_feedback
        return msg,lf
    except Exception,e:
        # any error?
        msg = "Error! "+str(e)
        lf='Error!'
        return  msg,lf

def update_lead_feedback(rid,feedback,uid):
    """
    This function is calling from ajax.py when lead updating his feedback
    It actually updating the 'lead_feedback' field in report record in DB
    """
    try:
        report= Reports.objects.get(id = rid)
        user = User.objects.get(id = uid)
        #adding simple signature to prevent anonymous lead feedback
        new_lead_feedback=user.name[0]+". "+user.surname+": " +feedback
        report.lead_feedback =new_lead_feedback
        report.save()
        msg=u"Вы оставили отзыв!"
        return msg, new_lead_feedback
    except Exception,e:
        msg = "Error! "+str(e); new_lead_feedback= 'ERROR'
        return msg, new_lead_feedback

def fill_up_statistics_table (pid):
    """
    This function calculate data for individual statistics for project
    and construct proper formatting for posting in the page via ajax 'partial POST'
    """
    project = Projects.objects.get(id = pid)
    # first we take the list of all users ever involved in our project
    reports = Reports.objects.filter(project_name = project.project_name)
    uid_list = reports.order_by('user_surname').values_list('user_id', flat = True).distinct()
    if uid_list:
        text = ""
        for uid in uid_list:
            #first we take all the hours from this user
            user_reports = reports.filter(user_id = uid).order_by('-id')
            first_user_report = user_reports[:1].get()
            all_hours = sum (user_reports.values_list('hours', flat = True).distinct())
            # here we add the first line for the table, where we shows user's info and all his/her hours
            text+="<tr style='background:#DAF0DC;'><td>"+first_user_report.user_surname+" "+first_user_report.user_name+u"</td><td><br/><br/></td><td>Часы: "+str(all_hours)+"</td></tr>"
            for report in user_reports:
                week = report.week
                year = report.year
                hours = report.hours
                text += "<tr><td></td><td>"+week+"/"+year+"</td><td>"+str(hours)+"</td></tr>"

    else:
        text= u"<tr>ОТЧЕТОВ ПОКА НЕТ</tr>"

    return text

def alert_mail(uid, alert_type):
    """
    This function is used for boss and root notification about raising user accessLevel
    (or other suspicious activities)
    """
    user = User.objects.get(id = uid)
    office = Offices.objects.get(short_name = user.office)

    if alert_type == "accessLevel":
        if user.accessLevel == 1: level = u"Руководителя офиса (возможность просматривать временные отчеты сотрудников" \
                                          u" и корректировать отработанное ими время)";
        if user.accessLevel == 2: level = u"Администратора TimeCard (возможность менять права любых сотрудников, " \
                                          u"создавать и удалять их, а также добавлять новые офисы и проекты)";
        if user.accessLevel == 3: level = u"Root (ПОЛНЫЕ ПРАВА по доступу к любой странице TimeCard!)";
        subject = u"В TimeCard зафиксировано повышение прав пользователя!"
        message = u"Возможно, так и должно быть, но на всякий случай вас информируют, что сотрудник %s %s" \
                  u" теперь имеет права %s!" % (user.name, user.surname, level)

    datatuple = (
    (subject, message, TT_EMAIL_SYSTEM, [ROOT_EMAIL]),
    (subject, message, TT_EMAIL_SYSTEM, [office.boss_email]),
        )
    mail(datatuple)

def change_css_on_some_event(user):
    #format of date is "day/month" - that is because we store birthday day in that format
    # and later we can apply custom css for the according
    p = MyLog().p()
    # p(user['office'], 'user[\'office\']')


    timeshift = int(Offices.objects.get(short_name = user['office']).time_shift)
    # p(timeshift, 'timeshift')

    NOW = int(round(time.time()))+timeshift - 3 * 3600
    now = time.gmtime(NOW)
    month = time.strftime ('%m', now)
    day = time.strftime ('%d', now)
    today = month + "/" + day
    css = ''
    # the logic is next: if we have birthday for current user we will draw for him/her birthday theme. If
    # not we will check if today is any other general event and draw CSS according to that event
    # p(user['hb'], 'user[hb]')
    if user['hb'] == today:
        if user['gender'] == 'M':
            css = 'style_male_hb.css'
        else:
            css = 'style_female_hb.css'
        return css
    else:
        try:
            return settings.EVENTS[today]
        except KeyError:
            return False
