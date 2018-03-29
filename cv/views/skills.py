# -*- coding: utf-8 -*-
__author__ = 'ABKorotky'
__email__ = ['akorotky@minsk.ximxim.com', 'aleksandr.korotky@ximad.com']


from django.conf import settings
from django.contrib import messages
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from timecard import utils
from erp.utils import get_cv, check_login, check_permission

from cv.models import Skill, CVSkill
from cv.forms import SkillMFormset


@check_login
def skills_vf(request):
    """
    display te skills list formset.
    operations are add new skills, modify data & delete skills.
    check data & save.
    """
    cv = get_cv(request)
    if not check_permission(cv, perm_index=30): # view skills/requirements data
        messages.error(request, "Access denied")
        return redirect("erp_home")
    else:
        manage = False
        if check_permission(cv, perm_index=31): # manage skills/requirements data
            manage = True
    skills = None
    skill_mforms = None
    stage = request.REQUEST.get('stage', None)
    if stage == 'confirm' and request.method == "POST":
        if manage:
            skills_del = request.session.get('skills_del', None)
            for skill in skills_del:
                skill.delete()
            del request.session['skills_del']
            messages.success(request, 'Selected skills has been deleted successfully.')
        else:
            messages.error(request, "Access denied")
            return redirect("erp_home")
    if stage == 'validate' and request.method == "POST":
        if manage:
            skill_mforms = SkillMFormset(request.POST)
            if skill_mforms.is_valid():
                if skill_mforms.deleted_forms:
                    request.session['skills_del'] = [form.instance for form in skill_mforms.deleted_forms]
                    return render_to_response(
                        "cv/del_skills.html",
                        {
                            'cv': get_cv(request),
                            'nav': "cv",
                            'skills_del': request.session['skills_del'],},
                        RequestContext(request))
                skill_mforms.save()
                messages.success(request, 'Skills updated successfully.')
            else: # errors in saving
                messages.error(request, 'Skills didn`t save. There were some errors.')
        else:
            messages.error(request, "Access denied")
            return redirect("erp_home")
    # stage == input
    if manage:
        skill_mforms = SkillMFormset()
    else:
        skills = Skill.objects.all()
    return render_to_response(
        "cv/skills.html",
        {
            'cv': cv,
            'nav': "cv",
            'skills': skills,
            'skill_mforms': skill_mforms,
        },
        RequestContext(request))


@check_login
def filter_skill_vf(request, s_id=''):
    """
    display list of CV which filter by skill tag.
    """
    tag = request.REQUEST.get('tag', None)
    try:
        skill = Skill.objects.get(id=int(s_id))
    except Skill.DoesNotExist, Skill.MultipleObjectsReturned:
        skill = None
    if skill and tag:
        cvs = []
        for cv_sk in CVSkill.objects.filter(skill=skill):
            if cv_sk.desc:
                lst = map(unicode.strip, cv_sk.desc.lower().split(','))
                if tag in lst:
                    cvs.append(cv_sk.cv)
        return render_to_response(
            "cv/filter_skill.html",
            {
                'cv': get_cv(request),
                'nav': "cv",
                'skill': skill,
                'tag': tag,
                'cvs': cvs,
            },
            RequestContext(request))
    else:
        messages.error(request, 'Bad request')
        return redirect("erp_home")