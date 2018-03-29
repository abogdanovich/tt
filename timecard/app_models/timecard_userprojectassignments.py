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
from timecard_projects import TimecardProjects


from bson.objectid import ObjectId
import humbledb
import collections


class TimecardUserprojectassignments(Document):

    config_database = 'tt'
    config_collection = 'timecard_userprojectassignments'

    # id = '_id'
    id_ = 'id'
    user_ = 'user'
    date_ = 'date'
    project_ = 'project'

    def attachProjects(self, **options):
        l = MyLog().l()
        users = options['users']
        allProjectsByUsersIds = options['allProjectsByUsersIds']

        if isinstance(users, collections.Iterable):
            for user in users:
                if not 'projectList__' in user:
                    user['projectList__'] = []

                if isinstance(user, collections.Iterable):
                    if TimecardUser.id_ in user:
                        if isinstance(allProjectsByUsersIds, collections.Iterable):
                            for userId in allProjectsByUsersIds:

                                projectList = allProjectsByUsersIds[userId]

                                if user[TimecardUser.id_] == userId:
                                    user['projectList__'].append(projectList)
                                    # l(projectList, 'user with ID[' + str(userId) + '] got such projects')

        return users



    def getUsersProjectsIdsByUserId(self, **options):

        return 'I SHOULD WORK, BUT DON\'T :( '
        l = MyLog().l()

        userId = options['userId']

        if type(userId) == int:
            usersProjectsIds = []

            findDoc = {
                TimecardUserprojectassignments.user_: str(userId)
            }

            with MyDB:
                cursor = TimecardUserprojectassignments.find(findDoc)

                # if isinstance(cursor, collections.Iterable):
                for _ in cursor:
                    if TimecardUserprojectassignments.project_ in _:
                        usersProjectsIds.append(_[TimecardUserprojectassignments.project_])

        return usersProjectsIds



    def getAllUsersProjectsIds(self):

        l = MyLog().l()
        usersProjectsIds = {}

        with MyDB:
            cursor = TimecardUserprojectassignments.find()

            if isinstance(cursor, collections.Iterable):
                for _ in cursor:
                    if TimecardUserprojectassignments.user_ in _:
                        userId = int(_[TimecardUserprojectassignments.user_])
                        if not TimecardUserprojectassignments.user_ in usersProjectsIds:
                            usersProjectsIds[userId] = []
                        usersProjectsIds[userId].append(_)

        return usersProjectsIds


    def getAllUsersProjects(self):

        l = MyLog().l()
        usersProjects = {}

        allProjects = TimecardProjects().getAllProjects()

        with MyDB:
            cursor = TimecardUserprojectassignments.find()

            if isinstance(cursor, collections.Iterable):
                for findedAssignment in cursor:

                    if isinstance(findedAssignment, collections.Iterable):
                        if TimecardUserprojectassignments.project_ in findedAssignment:


                            projectId = findedAssignment[TimecardUserprojectassignments.project_]

                            if isinstance(allProjects, collections.Iterable):
                                for project in allProjects:
                                    if TimecardProjects.id_ in project:

                                        if project[TimecardProjects.id_] == projectId:
                                            findedAssignment['description__'] = project
                                            break

                            if TimecardUserprojectassignments.user_ in findedAssignment:
                                userId = int(findedAssignment[TimecardUserprojectassignments.user_])


                                if not userId in usersProjects:
                                    usersProjects[userId] = []
                                usersProjects[userId].append(findedAssignment)
        return usersProjects

