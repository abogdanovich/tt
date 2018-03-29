# -*- coding: utf-8 -*-

#########################################################################
# Model for MongoDB collection `timecard_skill_tags`
# author DZmitriy Morozov
# email: castor_troy@tut.by
# vk: vk.com/id13245451
# skype: xdoctordog
# 2014
#########################################################################

import logging
from django.db import models
import humbledb
from humbledb import Document
import datetime
import json
from ..doctordog import *

from timecard.app_models.MyDB import MyDB
from timecard.app_models.timecard_customers import TimecardCustomers
from timecard.app_classes.MyLog import MyLog
from bson.objectid import ObjectId

from timecard.app_models.timecard_offices import TimecardOffices
from timecard.app_models.timecard_user import TimecardUser
# from timecard.app_models.project_appended_employee_role import ProjectAppendedEmployeeRoleDoc
from timecard.app_models.project_appended_employee_role import ProjectAppendedEmployeeRoleDoc
from timecard.app_models.timecard_projects import TimecardProjects
from timecard.app_classes.MyDate import *


class TimecardSkillTags(Document):

    config_collection = 'timecard_skill_tags'
    config_database = 'tt'

    skillTagId_ = '_id'

    name_ = 'name'
    removed_ = 'removed'


    def getAll(self):
        all = []
        with MyDB:
            cursor = TimecardSkillTags.find({})
        if iterable(cursor):
            for doc in cursor:
                all.append(doc)
        return all


    # Nas - The Message
    def addNewTags(self, **opts):
        skillTagIds = []
        l = MyLog().l()
        description = getSimpleVal(opts, 'description')
        words = my_explode(description)

        # wordsForInsert = list(set(words))

        # l(wordsForInsert, 'wordsForInsert')

        # for word in wordsForInsert:
        for word in words:
            if not self.existsSame(name = word):
                skillTagId = self.addTag(name = word)
                skillTagIds.append(skillTagId)
            else:
                skillTagId = self.getSkillTagIdByName(name = word)

                l([skillTagId, word], 'skillTagId, word')

                if isValidObjectId(skillTagId):
                    skillTagIds.append(skillTagId)
                else:
                    l('SOMETHING HAPPENING')

        # l(skillTagIds, 'skillTagIds')

        return skillTagIds  # list of ObjectId


    def getSkillTagIdByName(self, **o):
        l = MyLog().l()
        l = MyLog().empty()
        name = getSimpleVal(o, 'name')
        skillTagId = None
        doc = None
        cursor = None


        l(name, 'getSkillTagIdByName() name')

        if name != None:
            searchDoc = {
                TimecardSkillTags.name_: name
            }

            with MyDB:
                cursor = TimecardSkillTags.find(searchDoc)

            if iterable(cursor):
                for skill in cursor:
                    doc = skill
                    l(doc, 'finded skilltagID doc')
                    break


            skillTagId = self.get_id(doc)




            l(skillTagId, 'skillTagId')

        return skillTagId




    def addTag(self, **o):
        l = MyLog().l()
        resultInsert = False

        name = getSimpleVal(o, 'name')

        if is_str(name):
            insertDoc = {
                TimecardSkillTags.name_: name
            }

            with MyDB:
                skillTagId = TimecardSkillTags.insert(insertDoc)

        return skillTagId

    def get_id(self, doc):
        response = None
        if isinstance(doc, collections.Iterable):
            if '_id' in doc:
                response = doc['_id']
        return response

    def existsSame(self, **o):
        l = MyLog().l()
        l = MyLog().empty()

        name = o['name']
        response = False
        doc = None

        searchDoc = {
            TimecardSkillTags.name_: name
        }

        # l(searchDoc, 'existsSame() searchDoc32879t234g89')

        with MyDB:
            cursor = TimecardSkillTags.find(searchDoc)

        # if isinstance(cursor, collections.Iterable):
        for d in cursor:
            doc = d
            break

        if doc != None:
            response = True

        # l(doc, 'isExists doc6545641615')

        return response



