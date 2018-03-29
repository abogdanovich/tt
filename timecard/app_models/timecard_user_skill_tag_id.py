# -*- coding: utf-8 -*-

#########################################################################
# Model for MongoDB collection `timecard_user_skill_tag_id`
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


class TimecardUserSkillTagId(Document):

    config_collection = 'timecard_user_skill_tag_id'
    config_database = 'tt'


    userSkillTagId_ = '_id'

    user_id_ = 'user_id'
    skill_id_ = 'skill_id'
    skill_tag_id_ = 'skill_tag_id'

    def getAll(self):
        all = []
        with MyDB:
            cursor = TimecardUserSkillTagId.find({})
        if iterable(cursor):
            for doc in cursor:
                all.append(doc)
        return all


    def addSkillTagIdsToUser(self, userId, skillId, skillTagIds):



        addedUserSkillTagId = []
        l = MyLog().l()

        if is_int(userId) and isValidObjectId(skillId):
            removeResult = self.removeUsersSkillTagsIds(userId = userId, skillId = skillId)


            if iterable(skillTagIds):
                for skillTagId_objectId in skillTagIds:

                    b = not self.existsSame(skillTagId = skillTagId_objectId, userId = userId, skillId = skillId )

                    l([b, skillTagId_objectId], 'NOT THE SAME: NEED INSERT ?')

                    if b:
                        # ObjectId
                        userSkillTagId = self.addUserSkillTagId(skillTagId = skillTagId_objectId, userId = userId, skillId = skillId)

                        if isValidObjectId(userSkillTagId):
                            addedUserSkillTagId.append(userSkillTagId)

        return addedUserSkillTagId

    def addUserSkillTagId(self, **o):
        l = MyLog().l()
        skillTagId = getSimpleVal(o, 'skillTagId')
        userId = getSimpleVal(o, 'userId')
        skillId = getSimpleVal(o, 'skillId')
        insertDoc = None

        userSkillTagId = None

        if is_int(userId) and isValidObjectId(skillTagId) and isValidObjectId(skillId):

            insertDoc = {
                TimecardUserSkillTagId.skill_id_: ObjectId(skillId),
                TimecardUserSkillTagId.skill_tag_id_: ObjectId(skillTagId),
                TimecardUserSkillTagId.user_id_: userId,
            }

            with MyDB:
                userSkillTagId = TimecardUserSkillTagId.insert(insertDoc)


        l(userSkillTagId, 'NEW USER SKILL TAG')

        return userSkillTagId  # ObjectId

    def removeUsersSkillTagsIds(self, **o):
        l = MyLog().l()
        removeResult = None

        userId = o['userId']
        skillId = o['skillId']

        criteriaDoc = {
            TimecardUserSkillTagId.user_id_: userId,
            TimecardUserSkillTagId.skill_id_: skillId
        }

        with MyDB:
            removeResult = TimecardUserSkillTagId.remove(criteriaDoc)

        l(removeResult, 'removeResult')

        return removeResult


    def existsSame(self, **o):
        l = MyLog().l()

        userId = getSimpleVal(o, 'userId')
        skillTagId = getSimpleVal(o, 'skillTagId')
        skillId = getSimpleVal(o, 'skillId')

        response = False
        doc = None

        # l(is_int(userId), 'is_int(userId)')
        # l(isValidObjectId(skillTagId), 'isValidObjectId(skillTagId)')


        # l(skillId, 'skillId')
        #
        # l(isValidObjectId(skillId), 'isValidObjectId(skillId)')



        if is_int(userId) and isValidObjectId(skillTagId) and isValidObjectId(skillId):
            searchDoc = {
                TimecardUserSkillTagId.user_id_: userId,
                TimecardUserSkillTagId.skill_id_: ObjectId(skillId),
                TimecardUserSkillTagId.skill_tag_id_: ObjectId(skillTagId),
            }

            with MyDB:
                cursor = TimecardUserSkillTagId.find(searchDoc)

            # l(cursor, 'cursor987tsdfasdf')
            # l(iterable(cursor), 'iterable(cursor)')

            if iterable(cursor):
                for d in cursor:
                    # l(d, 'd')
                    doc = d
                    break

            # l(doc, 'DOCCcc')

            if doc != None:
                response = True

            # l(doc, 'isExists doc')

        return response