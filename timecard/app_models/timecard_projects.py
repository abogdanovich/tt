# -*- coding: utf-8 -*-

#########################################################################
# Model for MongoDB collection `timecard_userprojectassignments`
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

from timecard_languages import TimecardLanguages
from timecard_language_skills import TimecardLanguageSkills


from bson.objectid import ObjectId
import humbledb
import collections


class TimecardProjects(Document):

    config_database = 'tt'
    config_collection = 'timecard_projects'

    # id = '_id'

    temp_project_id_ = 'temp_project_id'

    id_ = 'id'
    project_name_ = 'project_name'
    project_desc_ = 'project_desc'
    project_desc_for_customer_ = 'project_desc_for_customer'
    customer_id_ = 'customer_id'

    customer_feedback_ = 'customer_feedback'

    service_ = 'service'
    industry_ = 'industry'
    solution_highlight_ = 'solution_highlight'
    development_tools_and_technologies_ = 'development_tools_and_technologies'
    development_time_ = 'development_time'
    start_date_ = 'start_date'
    finish_date_ = 'finish_date'
    project_is_in_pause_ = 'project_is_in_pause'
    creator_id_ = 'creator_id'
    project_opened_ = 'project_opened'

    closed_ = 'closed'

    # FIXME: Next two lines maybe deprecated... really don't know :D
    project_opened_ = 'project_opened'
    project_service_ = 'project_service'





    def getProjectById(self, **_):
        project_id = _['project_id']
        l = MyLog().l()
        projectInfo = []
        cursor = None

        searchDoc =\
        {
            '_id': ObjectId(project_id)
        }

        with MyDB:
            cursor = TimecardProjects.find(searchDoc)

            if isinstance(cursor, collections.Iterable):
                for el in cursor:
                    projectInfo = el
                    break


        projectInfo = addObjectID(projectInfo)
        return projectInfo


    def updateProject(self, **options):
        l = MyLog().l()
        projectId = options['projectId']
        l(projectId, 'projectIdINSIDE')
        resultUpdate = False
        response = False

        if isValidObjectId(projectId):
            doc = {}

            doc[TimecardProjects.project_name_] = options[TimecardProjects.project_name_]
            doc[TimecardProjects.project_desc_] = options[TimecardProjects.project_desc_]
            doc[TimecardProjects.project_desc_for_customer_] = options[TimecardProjects.project_desc_for_customer_]
            doc[TimecardProjects.customer_id_] = options[TimecardProjects.customer_id_]

            # l(doc[TimecardProjects.customer_id_], 'doc[TimecardProjects.customer_id_] <<---')

            doc[TimecardProjects.customer_feedback_] = options[TimecardProjects.customer_feedback_]
            doc[TimecardProjects.service_] = options[TimecardProjects.service_]
            doc[TimecardProjects.industry_] = options[TimecardProjects.industry_]
            doc[TimecardProjects.solution_highlight_] = options[TimecardProjects.solution_highlight_]
            doc[TimecardProjects.development_tools_and_technologies_] = options[TimecardProjects.development_tools_and_technologies_]
            doc[TimecardProjects.development_time_] = options[TimecardProjects.development_time_]

            doc[TimecardProjects.start_date_] = options[TimecardProjects.start_date_]
            doc[TimecardProjects.finish_date_] = options[TimecardProjects.finish_date_]




            if options[TimecardProjects.project_is_in_pause_] == 'true':
                doc[TimecardProjects.project_is_in_pause_] = True
            else:
                doc[TimecardProjects.project_is_in_pause_] = False

            doc[TimecardProjects.creator_id_] = options[TimecardProjects.creator_id_]
            doc[TimecardProjects.project_opened_] = options[TimecardProjects.project_opened_]


            l(doc, 'DGO')


            criteriaDoc = {
                '_id': ObjectId(projectId),
            }

            l(criteriaDoc, 'criteriaDoc')

            with MyDB:
                resultUpdate = TimecardProjects.update(criteriaDoc, { '$set': doc }, upsert = False, multi = True)


            if getSimpleVal(resultUpdate, 'updatedExisting') != None:
                if resultUpdate['updatedExisting'] == True:
                    response = True


        l(response, 'response')
        return response






    def insertNewProject(self, **options):

        l = MyLog().l()
        p = MyLog().p()
        resultInsert = False
        doc = {}

        doc[TimecardProjects.temp_project_id_] = options[TimecardProjects.temp_project_id_]
        doc[TimecardProjects.project_name_] = options[TimecardProjects.project_name_]
        doc[TimecardProjects.project_desc_] = options[TimecardProjects.project_desc_]
        doc[TimecardProjects.project_desc_for_customer_] = options[TimecardProjects.project_desc_for_customer_]
        doc[TimecardProjects.customer_id_] = options[TimecardProjects.customer_id_]

        l(doc[TimecardProjects.customer_id_], 'doc[TimecardProjects.customer_id_] <<---')

        doc[TimecardProjects.customer_feedback_] = options[TimecardProjects.customer_feedback_]
        doc[TimecardProjects.service_] = options[TimecardProjects.service_]
        doc[TimecardProjects.industry_] = options[TimecardProjects.industry_]
        doc[TimecardProjects.solution_highlight_] = options[TimecardProjects.solution_highlight_]
        doc[TimecardProjects.development_tools_and_technologies_] = options[TimecardProjects.development_tools_and_technologies_]
        doc[TimecardProjects.development_time_] = options[TimecardProjects.development_time_]

        doc[TimecardProjects.start_date_] = options[TimecardProjects.start_date_]
        doc[TimecardProjects.finish_date_] = options[TimecardProjects.finish_date_]

        if options[TimecardProjects.project_is_in_pause_] == 'true':
            doc[TimecardProjects.project_is_in_pause_] = True
        else:
            doc[TimecardProjects.project_is_in_pause_] = False

        doc[TimecardProjects.creator_id_] = options[TimecardProjects.creator_id_]
        doc[TimecardProjects.project_opened_] = options[TimecardProjects.project_opened_]

        with MyDB:
            resultInsert = TimecardProjects.insert(doc)

        return resultInsert


    def getAllProjects(self, **opts):
        l = MyLog().l()
        order_by = getVal(opts, 'order_by')
        allProjects = []
        with MyDB:
            if order_by == None:
                cursor = TimecardProjects.find()
            else:
                cursor = TimecardProjects.find().sort(order_by, humbledb.ASC)
            if iterable(cursor):
                for object in cursor:
                    allProjects.append(object)
        return allProjects


    def getProjectNameById(self, **o):
        l = MyLog().l()
        projectId = getVal(o, 'projectId')
        name = None
        closeResult = False
        if isValidObjectId(projectId):
            criteriaDoc = {
                '_id': ObjectId(projectId)
            }

            with MyDB:
                cursor = TimecardProjects.find(criteriaDoc)
                if iterable(cursor):
                    for obj in cursor:
                        if iterable(obj):
                            if TimecardProjects.project_name_ in obj:
                                name = obj[TimecardProjects.project_name_]
        return name


    def close(self, **o):
        l = MyLog().l()
        projectId = getVal(o, 'projectId')
        closeResult = False
        response = False
        if isValidObjectId(projectId):
            criteriaDoc = {
                '_id': ObjectId(projectId)
            }

            updateDoc = {
                '$set': {
                    TimecardProjects.closed_: True
                }
            }

            with MyDB:
                r = TimecardProjects.update(criteriaDoc, updateDoc)
                l(r, 'result closing Project')
                if iterable(r):
                    if 'updatedExisting' in r:
                        if r['updatedExisting'] == True:
                            response = True
        return response


