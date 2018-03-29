# -*- coding: utf-8 -*-

#########################################################################
# Model for MongoDB collection `timecard_skills`
# author Dzmitriy Morozov
# email: castor_troy@tut.by
# vk: vk.com/id13245451
# skype: xdoctordog
# 2014
#########################################################################

import logging
from humbledb import Document
from MyDB import MyDB
from timecard.app_models.timecard_user import TimecardUser
# from timecard.models import *

import datetime
from ..app_classes.MyLog import MyLog
from ..doctordog import *

from timecard_languages import TimecardLanguages
from timecard_language_skills import TimecardLanguageSkills

from bson.objectid import ObjectId
import humbledb


class TimecardSkills(Document):

    config_database = 'tt'
    config_collection = 'timecard_skills'

    id_ = 'id'
    order_ = 'order'
    name_ = 'name'
    rus_name_ = 'rus_name'

    def getSkillNameById(self, **options):
        l = MyLog().l()
        skillId = options['skillId']

        l(skillId, 'getSkillNameById():: skillId')

        skillName = None

        searchDoc = {
            '_id': ObjectId(skillId)
        }

        doc = None
        with MyDB:
            cursor = TimecardSkills.find(searchDoc)

            for x in cursor:
                l(x, 'x')
                doc = x
                break

        if doc != None:
            l(doc[TimecardSkills.name_], 'doc[TimecardSkills.name_]')
            if TimecardSkills.name_ in doc:
                skillName = doc[TimecardSkills.name_]

        return skillName


    def getAll(self):
        allSkills = []
        with MyDB:
            cursor = TimecardSkills.find({})
        if iterable(cursor):
            for x in cursor:
                allSkills.append(x)
        return allSkills

    def prepareForTemplate(self, **options):
        skills = []
        allSkills = options['allSkills']
        # FIXME: BE patient when change fields of document in this collection: U may also change doc dictionary probably also
        if iterable(allSkills):
            for skill in allSkills:
                if iterable(skill):
                    if TimecardSkills.id_ in skill \
                        and TimecardSkills.order_ in skill \
                        and TimecardSkills.name_ in skill \
                        and TimecardSkills.rus_name_ in skill:
                        if not 'id_' in skill:
                            skill['id_'] = skill['_id']
                        skills.append(skill)
        return skills
