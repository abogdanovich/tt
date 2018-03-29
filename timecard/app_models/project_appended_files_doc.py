# -*- coding: utf-8 -*-

#########################################################################
# Model for MongoDB collection `project_appended_files`
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


class ProjectAppendedFilesDoc(Document):
    config_collection = 'project_appended_files'
    config_database = 'tt'

    appenderId = 'appenderId'
    fileName = 'fileName'
    projectId = 'projectId'  # !ATTENTION! Set only for already created projects
    fileDescription = 'fileDescription'
    # Cause when this key is absent the project's employee are set to unexisting/hav been creating project


    def updateFileDescription(self, appenderId, fileId, fileDescription):
        result = None

        searchDoc = {
                        "_id": ObjectId(fileId),
                        ProjectAppendedFilesDoc.appenderId: appenderId,
                        # ProjectAppendedFilesDoc.projectId: { '$exists': False }
                    }

        updateDoc = { ProjectAppendedFilesDoc.fileDescription: fileDescription }

        with MyDB:
            result = ProjectAppendedFilesDoc.update( searchDoc, { '$set': updateDoc }, upsert = False, multi = False )
        return result

    def updateFileDescriptionRealProject(self, appenderId, projectId, fileId, fileDescription):
        l = MyLog().l()
        result = None

        updateDoc ={
                        "_id": ObjectId(fileId),
                        ProjectAppendedFilesDoc.appenderId: appenderId,
                        ProjectAppendedFilesDoc.projectId: ObjectId(projectId)
                    }

        setDoc = {
            ProjectAppendedFilesDoc.fileDescription: fileDescription
        }

        with MyDB:
            result = ProjectAppendedFilesDoc.update(updateDoc,
                {'$set': setDoc},
                upsert = False,
                multi = False
            )
        return result





    def bindFilesToProject(self, appenderId, projectId):
        result = None
        writeConcernDoc = None
        with MyDB:
            result = ProjectAppendedFilesDoc.update(
                {
                    ProjectAppendedFilesDoc.appenderId: appenderId,
                    ProjectAppendedFilesDoc.projectId: { '$exists': False }
                },
                {'$set': {ProjectAppendedFilesDoc.projectId: projectId}},
                upsert = False,
                multi = True
            )
        return result






    def appendFileOnEmptyProject(self, appenderId, fileName):
        result = None
        doc = {
            ProjectAppendedFilesDoc.appenderId : appenderId,
            ProjectAppendedFilesDoc.fileName: fileName,
            ProjectAppendedFilesDoc.fileDescription: ''
        }
        with MyDB:
            result = ProjectAppendedFilesDoc.insert(doc)
        return result


    def appendFileOnRealProject(self, appenderId, fileName, projectId):

        result = None
        doc = {
            ProjectAppendedFilesDoc.projectId: ObjectId(projectId),
            ProjectAppendedFilesDoc.appenderId: appenderId,
            ProjectAppendedFilesDoc.fileName: fileName,
            ProjectAppendedFilesDoc.fileDescription: ''
        }
        with MyDB:
            result = ProjectAppendedFilesDoc.insert(doc)
        return result



    def getFilesAppendedOnRealProject(self, project_id):
        l = MyLog().l()
        p = MyLog().p()
        _ = []

        #  project_id
        searchDoc = {
            ProjectAppendedFilesDoc.projectId: ObjectId(project_id)
        }

        l(searchDoc, 'searchDoc')

        with MyDB:
            cursor = ProjectAppendedFilesDoc.find( searchDoc )

            # l(cursor, 'cursor')

            for el in cursor:
                el['fileId'] = str(el['_id'])
                _.append(el)
                # l(el, 'el')
        return _





    def getFilesAppendedOnEmptyProject(self, appenderId):
        l = MyLog().l()
        p = MyLog().p()
        _ = []
        with MyDB:
            cursor = ProjectAppendedFilesDoc.find( { ProjectAppendedFilesDoc.appenderId: appenderId,
                                                     ProjectAppendedFilesDoc.projectId: { '$exists': False } })
            # _ =[x for x in cursor]

            for el in cursor:
                el['fileId'] = str(el['_id'])
                _.append(el)
                l(el, 'el')
        return _


    def getFilesIdsAppendedOnEmptyProject(self, appenderId):
        l = MyLog().l()
        p = MyLog().p()

        mass = self.getFilesAppendedOnEmptyProject(appenderId)
        _ = []
        for x in mass:
            _.append(str(x['_id']))
        return _






    def getFilesIdsAppendedOnRealProject(self, projectId):

        l = MyLog().l()
        p = MyLog().p()

        l('call func getFilesIdsAppendedOnRealProject() ')

        mass = self.getFilesAppendedOnRealProject(projectId)

        l(mass, 'mass')

        _ = []
        for x in mass:
            _.append(str(x['_id']))
        return _

