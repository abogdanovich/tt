# -*- coding: utf-8 -*-

#########################################################################
# Model for MongoDB collection `timecard_users_languages`
# author DZmitriy Morozov
# email: castor_troy@tut.by
# vk: vk.com/id13245451
# skype: xdoctordog
# 2014
#########################################################################

import logging
from humbledb import Document
from MyDB import MyDB

from timecard.app_models.timecard_user import *



# from timecard.models import *
import humbledb

import datetime
from ..doctordog import *
from ..app_classes.MyLog import MyLog

from timecard_languages import TimecardLanguages
from bson.objectid import ObjectId



class TimecardLanguageSkills(Document):

    config_database = 'tt'
    config_collection = 'timecard_language_skills'

    # <select class="mb_input" id="choosen_language_written_53ff06bc019442a2e3e9c2e7">
    # <option value="0">None</option>
    # <option value="1">Basic</option>
    # <option value="2">Advanced</option>
    # <option value="3">Fluent</option>
    # </select>
    id_ = 'id' # id_ : Именно это value со страницы /settings/ где устанавливается уровень владения языком
    order_ = 'order'
    name_ = 'name'
    rus_name_ = 'rus_name'

    def getAllLanguageSkills(self, **o):
        skills = []
        order_by = getVal(o, str(TimecardLanguageSkills.order_))
        with MyDB:
            if order_by != None:
                cursor = TimecardLanguageSkills.find({}).sort(order_by, humbledb.ASC)
            else:
                cursor = TimecardLanguageSkills.find({})
        if iterable(cursor):
            for skill in cursor:
                skills.append(skill)
        return skills




