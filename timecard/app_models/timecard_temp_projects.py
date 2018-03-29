# -*- coding: utf-8 -*-

#########################################################################
# Model for MongoDB collection `timecard_temp_projects`
# author DZmitriy Morozov
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
from ..doctordog import *
from ..app_classes.MyLog import MyLog
import humbledb

class TimecardTempProjects(Document):

    config_database = 'tt'
    config_collection = 'timecard_temp_projects'

    id_ = 'id'
    user_id_ = 'user_id'
    #       "_id" in collection typeof ObjectId()  IS PROJECT_ID

    def getAllTimecardTempProjects(self):
        listTimecardTempProjects = []
        cursor = None
        with MyDB:
            cursor = TimecardTempProjects.find()
            # cursor = TimecardCustomers.find().sort(order_by, humbledb.ASC)
            for obj in cursor:
                listTimecardTempProjects.append(obj)
        return listTimecardTempProjects

    def insertDocs(self, docs):
        result = None
        with MyDB:
            result = TimecardTempProjects.insert(docs)
        return result

    def add(self, **options):
        insertedDocId = None
        with MyDB:
            doc = {
                TimecardTempProjects.user_id_ : options['user_id'],
                'timestamp': datetime.datetime.now(),
            }
            insertedDocId = TimecardTempProjects.insert(doc)
        return insertedDocId


    def delete__(self, **options):
        l = MyLog().l()
        removingResult = None
        with MyDB:
            doc = {
                TimecardTempProjects.user_id_ : options['user_id'],
            }
            # l(doc, 'removing DOC')
            removingResult = TimecardTempProjects.remove(doc)
            # l(removingResult, 'removingResult')
        return removingResult


    def getTempProjectIdByUserId(self, userId):
        objectId = None
        with MyDB:
            cursor = TimecardTempProjects.find({TimecardTempProjects.user_id_: userId})
            for el in cursor:
                objectId = el['_id']
                objectId = str(objectId)
                break
        return objectId



    def generateNewTempProjectIdForUserId(self, userId):

        return False
        # response = None
        # tempProjectId = self.getTempProjectIdByUserId(userId)
        # if tempProjectId != None:
        #     self.delete__(user_id = userId)
        # self.add(user_id = userId)
        #
        # return response



    def initTempProjectsForUsers(self, users):
        l = MyLog().l()
        p = MyLog().p()
        result = None

        ids = []
        for user in users:
            i = int(user[TimecardUser.id_])
            ids.append(i)

        # l(ids, 'ids')

        allTempProjects = self.getAllTimecardTempProjects()
        usersOnEmptyProjects = []  # Those PM which has not an empty project

        for proj in allTempProjects:
            userId = int(proj[TimecardTempProjects.user_id_])
            usersOnEmptyProjects.append(userId)

        docs = []
        for user in users:
            uid = int(user[TimecardUser.id_])
            if uid not in usersOnEmptyProjects:
                l(uid, 'i hav no empty proj')
                doc = {}
                doc[TimecardTempProjects.user_id_] = uid
                docs.append(doc)

        if docs:
            r = self.insertDocs(docs)

        #  TODO: INIT INSERT [NO NEED TO USE -- BUT NECCESSARY]
        if False:
            docs = []
            ids = []
            for user in users:
                i = int(user[TimecardUser.id_])
                ids.append(i)
                doc = {}
                doc[TimecardTempProjects.user_id_] = i
                docs.append(doc)

            with MyDB:
                result = TimecardTempProjects.insert(docs)


        return result
