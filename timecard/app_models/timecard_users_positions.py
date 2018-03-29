# -*- coding: utf-8 -*-

#########################################################################
# Model for MongoDB collection `timecard_users_positions`
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


class TimecardUsersPositions(Document):

    config_collection = 'timecard_users_positions'
    config_database = 'tt'

    id = '_id'

    position_id_ = 'position_id'
    user_id_ = 'user_id'
    show_on_main_page_ = 'show_on_main_page'


    def deactivateShowOnMainPage(self, **o):
        response = False
        l = MyLog().l()
        positionId = getSimpleVal(o, 'positionId')
        l(positionId, 'positionId')
        userId = getSimpleVal(o, 'userId')

        positionId = toObjectId(positionId)


        l(positionId, 'positionId')
        l(is_int(userId), 'is_int(userId)')
        l(type(positionId) == ObjectId, 'type(positionId) == ObjectId')

        if is_int(userId) and type(positionId) == ObjectId:
            updateResult = None

            searchDoc = {
                TimecardUsersPositions.position_id_: positionId,
                TimecardUsersPositions.user_id_: userId
            }

            l(searchDoc, 'searchDoc')

            updateDoc = {
                '$set': {
                    TimecardUsersPositions.show_on_main_page_: False
                }
            }

            l(updateDoc, 'updateDoc')

            with MyDB:
                updateResult = TimecardUsersPositions.update(searchDoc, updateDoc)

                l(updateResult, 'updateResult')

                if isinstance(updateResult, collections.Iterable):
                    if 'updatedExisting' in updateResult:
                        if updateResult['updatedExisting'] == True:
                            response = True



        return response




    def activateShowOnMainPage(self, **o):
        response = False
        l = MyLog().l()
        positionId = getSimpleVal(o, 'positionId')
        l(positionId, 'positionId')
        userId = getSimpleVal(o, 'userId')

        positionId = toObjectId(positionId)


        l(positionId, 'positionId')
        l(is_int(userId), 'is_int(userId)')
        l(type(positionId) == ObjectId, 'type(positionId) == ObjectId')

        if is_int(userId) and type(positionId) == ObjectId:
            updateResult = None

            searchDoc = {
                TimecardUsersPositions.position_id_: positionId,
                TimecardUsersPositions.user_id_: userId
            }

            # l(searchDoc, 'searchDoc')

            updateDoc = {
                '$set': {
                    TimecardUsersPositions.show_on_main_page_: True
                }
            }

            # l(updateDoc, 'updateDoc')

            with MyDB:
                updateResult = TimecardUsersPositions.update(searchDoc, updateDoc)

                l(updateResult, 'updateResult')

                if isinstance(updateResult, collections.Iterable):
                    if 'updatedExisting' in updateResult:
                        if updateResult['updatedExisting'] == True:
                            response = True



        return response







    def remove_position_from_user(self, **o):
        l = MyLog().l()
        response = False
        ok = False
        removeResult = None
        userId = getSimpleVal(o, 'userId')
        positionId = getSimpleVal(o, 'positionId')

        l(positionId, 'positionId')
        l(userId, 'userId')

        if isValidObjectId(positionId):
            removeDoc = {
                TimecardUsersPositions.user_id_: userId,
                TimecardUsersPositions.position_id_: ObjectId(positionId),
            }

            l(removeDoc, 'removeDoc')

            with MyDB:
                removeResult = TimecardUsersPositions.remove(removeDoc)

            l(removeResult, 'removeResult')

            ok = getSimpleVal(removeResult, 'ok')
            if ok == 1:
                response = True
        l(ok, 'ok')
        return response







    def addPositionToUser(self, **o):
        l = MyLog().l()
        userId = getSimpleVal(o, 'userId')
        positionId = getSimpleVal(o, 'positionId')

        addResult = False

        # l(userId, 'userId')
        # l(is_int(userId), 'is_int(userId)')
        #
        l(positionId, 'positionId')
        l(isValidObjectId(positionId), 'isValidObjectId(positionId)')

        if is_int(userId) and isValidObjectId(positionId):
            doc = {
                TimecardUsersPositions.user_id_: userId,
                TimecardUsersPositions.position_id_: ObjectId(positionId),
            }
            l(doc, 'doc')
            if not self.existsSame(userId = userId, positionId = positionId):
                with MyDB:
                    addResult = TimecardUsersPositions.insert(doc)

        l(addResult, 'addResult')

        return addResult




    def existsSame(self, **o):
        l = MyLog().l()
        l = MyLog().empty()

        userId = getSimpleVal(o, 'userId')
        positionId = getSimpleVal(o, 'name')

        response = False
        doc = None

        l(userId, 'userId')
        l(positionId, 'positionId')

        if userId != None and positionId != None:
            searchDoc = {
                TimecardUsersPositions.user_id_: userId,
                TimecardUsersPositions.position_id_: positionId
            }

            # l(searchDoc, 'existsSame() searchDoc32879t234g89')

            with MyDB:
                cursor = TimecardUsersPositions.find(searchDoc)

            # if isinstance(cursor, collections.Iterable):
            for d in cursor:
                doc = d
                break

            if doc != None:
                response = True

            # l(doc, 'isExists doc6545641615')

        return response






    def getByUserId(self, **o):
        usersPositions = []
        user_id = getSimpleVal(o, 'user_id')

        searchDoc = {
            TimecardUsersPositions.user_id_: user_id
        }

        cursor = None

        with MyDB:
            cursor = TimecardUsersPositions.find(searchDoc)

        if iterable(cursor):
            for x in cursor:
                x = addObjectID(x)
                usersPositions.append(x)

        return usersPositions






    def clearListFromAppliedPositions(self, **o):

        l = MyLog().l()

        notApplied = []

        usersPositions = getSimpleVal( o, 'usersPositions')
        allPositions = getSimpleVal(o, 'allPositions')

        if iterable(allPositions):
            for position in allPositions:

                # l(position, 'position')

                if iterable(position):
                    if '_id' in position: # '_id'
                        hasUser = False;

                        # l(hasUser, 'hasUser')

                        if iterable(usersPositions):
                            for userPosition in usersPositions:

                                l(userPosition, 'userPosition')

                                if iterable(userPosition):
                                    if TimecardUsersPositions.position_id_ in userPosition:

                                        # l(userPosition[TimecardUsersPositions.position_id_], 'userPosition[TimecardUsersPositions.position_id_]')
                                        # l(position['_id'], 'position[_id]')

                                        strPositionId = str(position['_id'])
                                        strUserPosition = str(userPosition[TimecardUsersPositions.position_id_])

                                        # l(strPositionId, 'strPositionId')
                                        # l(strUserPosition, 'strUserPosition')

                                        b = strUserPosition == strPositionId

                                        # l(b, 'beeeee')

                                        if b:
                                            hasUser = True
                                            break

                        if hasUser == False:
                            notApplied.append(position)

        return notApplied





#




