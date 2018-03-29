# -*- coding: utf-8 -*-
__author__ = 'ABKorotky'
__email__ = ['akorotky@minsk.ximxim.com', 'aleksandr.korotky@ximad.com']





import ldap
from datetime import date
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from cv.models import Position, CV, Skill, CVSkill
from projects.models import Project, WorkGroup
from utils import get_cv, check_login

import logging


# TODO: re-comment when i know for what purpose
@check_login
def main_vf(request):
    projects = {
        'total': Project.objects.all().count(),
        'prepare': Project.prepare.count(),
        'develop': Project.develop.count(),
        'work': Project.develop.work().count(),
        'pause': Project.develop.pause().count(),
        'finish': Project.finish.count(),
    }
    cvs = {
        'total': CV.actives.count(),
        'fulls': CV.actives.fulls().count(),
        'positions': CV.actives.empty_positions().count(),
        'fls': CV.actives.empty_fls().count(),
        'skills': CV.actives.empty_skills().count(),
        'projects': CV.actives.empty_projects().count(),
        }
    emps_req = WorkGroup.objects.select_related('project', 'cv').filter(cv__fired=False)
    emps = {
        'idle': 0,
        'prepare': 0,
        'develop': 0,
        'work': 0,
        'pause': 0,
        'finish': 0,
    }
    for emp in emps_req:
        st = emp.project.get_state()
        emps[st] += 1
        if st == 'develop':
            if emp.project.is_pause():
                st = 'pause'
            else:
                st = 'work'
        emps[st] += 1
    emps['idle'] = cvs['total'] - emps['work']
    skills_req = CVSkill.desc_skills.select_related('skill').filter(skill__on_main=True)
    skills = {}
    for skill in skills_req:
        s_id = skill.skill.id
        if s_id not in skills:
            skills[s_id] = {'name': skill.skill.name, 'tags': {}}
        for tag in skill.get_tags():
            if tag not in skills[s_id]['tags']:
                skills[s_id]['tags'][tag] = 1
            else:
                skills[s_id]['tags'][tag] += 1
    return render_to_response(
        "erp/main.html",
        {
            'cv': get_cv(request),
            'nav': "main",
            'projects': projects,
            'cvs': cvs,
            'emps': emps,
            'skills': skills,},
        RequestContext(request),
        )




def login_vf(request):
    """
    view func for check ldap/tt login
    """
    stage = request.REQUEST.get('stage', None)

    if request.method == "POST" and stage == 'validate':
        u = request.POST.get('username', None)
        p = request.POST.get('password', None)
        if u and p:
            is_ldap = False
            for currentldap in settings.AD_LDAP:
                try:
                    l = ldap.initialize(currentldap['LDAP_URL'])
                    l.simple_bind_s("uid=%s,%s" % (u, currentldap['LDAP_SEARCH_DN']), p)
                    is_ldap = True
                    break
                    #l.unbind_s()
                except ldap.LDAPError:
                    is_ldap = False
            if is_ldap:
                # it is ok!!! now get cv_user
                try:
                    cv = CV.objects.get(login=u)
                except CV.DoesNotExist:
                    cv = CV.objects.create(name="%s_name" % u, surname="%s_surname" % u, login=u)
                    messages.info(request, "The first time you went to the ERP System.<br>Please, edit the yours personal data.")
                    request.session['cv_id'] = cv.id
                    return redirect("erp_cv", cv_id=cv.id)
                if cv.user:
                    request.session['cv_id'] = cv.id
                    request.session['uid'] = cv.user.id
                    request.session['ip'] = request.META['REMOTE_ADDR']
                return redirect("erp_home")
            messages.error(request, "Access denied.")
            return redirect("erp_logout")
        else:
            messages.error(request, "Username or password is missing.")
    # stage == input
    return render_to_response(
        "erp/login.html",
        {
            'cv': get_cv(request),
            'nav': "login",},
        RequestContext(request),
        )


def logout_vf(request):
    """
    view func for check ldap/tt login
    """
    request.session.flush()
    return render_to_response(
        "erp/logout.html",
        {
            'cv': None,
            'nav': "logout",},
        RequestContext(request),
        )