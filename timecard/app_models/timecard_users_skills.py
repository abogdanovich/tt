# -*- coding: utf-8 -*-

#########################################################################
# Model for MongoDB collection `timecard_users_skills`
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
from timecard_skills import TimecardSkills

from bson.objectid import ObjectId
import humbledb

import collections

import codecs


class TimecardUsersSkills(Document):

    config_database = 'tt'
    config_collection = 'timecard_users_skills'

    id_ = 'id'
    user_id_ = 'user_id'
    skill_id_ = 'skill_id'
    description_ = 'description'
    show_on_main_page_ = 'show_on_main_page'



    def activateShowOnMainPage(self, **options):
        updateResult = None
        response = False
        skillId = options['skillId']
        userId = options['userId']
        searchDoc = {
            TimecardUsersSkills.skill_id_: skillId,
            TimecardUsersSkills.user_id_: userId
        }

        updateDoc = {
            '$set': {
                TimecardUsersSkills.show_on_main_page_: 1
            }
        }

        with MyDB:
            updateResult = TimecardUsersSkills.update(searchDoc, updateDoc)

            if isinstance(updateResult, collections.Iterable):
                if 'updatedExisting' in updateResult:
                    if updateResult['updatedExisting'] == True:
                        response = True
        return response


    def deactivateShowOnMainPage(self, **options):
        response = False
        updateResult = False
        skillId = options['skillId']
        userId = options['userId']
        searchDoc = {
            TimecardUsersSkills.skill_id_: skillId,
            TimecardUsersSkills.user_id_: userId
        }

        updateDoc = {
            '$set': {
                TimecardUsersSkills.show_on_main_page_: 0
            }
        }

        with MyDB:
            updateResult = TimecardUsersSkills.update(searchDoc, updateDoc)

            if isinstance(updateResult, collections.Iterable):
                if 'updatedExisting' in updateResult:
                    if updateResult['updatedExisting'] == True:
                        response = True
        return response


    def attachSkillsToUsers(self, **options):

        l = MyLog().l()
        users = options['users']
        usersSkills = options['usersSkills']
        allSkills = options['allSkills']

        if isinstance(users, collections.Iterable):
            for user in users:
                if not 'user_skill_list' in user:
                    user['user_skill_list__'] = []

                if TimecardUser.id_ in user:

                    if isinstance(usersSkills, collections.Iterable):
                        for userSkill in usersSkills:
                            if isinstance(userSkill, collections.Iterable):

                                if TimecardUsersSkills.user_id_ in userSkill:
                                    if userSkill[TimecardUsersSkills.user_id_] == user[TimecardUser.id_]:

                                        if TimecardUsersSkills.skill_id_ in userSkill: # type 'unicode'

                                            if isinstance(allSkills, collections.Iterable):
                                                for skill in allSkills:
                                                    if isinstance(skill, collections.Iterable):
                                                        if 'id_' in skill: # class 'bson.objectid.ObjectId'
                                                            if str(skill['id_']) == str(userSkill[TimecardUsersSkills.skill_id_]):
                                                                userSkill['skill_name'] = ''
                                                                if TimecardSkills.name_ in skill:
                                                                    userSkill['skill_name'] = skill[TimecardSkills.name_]

                                                                user['user_skill_list__'].append(userSkill)


        return users



    def _remove_(self, **options):
        response = False
        removeResult = False
        l = MyLog().l()


        skillId = options['skillId']
        userId = options['userId']

        removeDoc = {
            TimecardUsersSkills.skill_id_: skillId,
            TimecardUsersSkills.user_id_: userId,

        }

        thisSkillId = self.existsSame(skillId = skillId, userId = userId)


        l(thisSkillId, 'thisSkillId')

        if thisSkillId != None:
            with MyDB:
                removeResult = TimecardUsersSkills.remove(removeDoc)

                l(removeResult, '$$$-->>removeResult')


        if isinstance(removeResult, collections.Iterable):
            if 'ok' in removeResult:
                if removeResult['ok'] == 1:
                    response = True

        return response





    def clearListFromAppliedSkills(self, **options):
        l = MyLog().l()

        notAppliedUsersSkills = []

        # return notAppliedUsersSkills

        usersSkills = options['usersSkills']
        allSkills = options['allSkills']

        if isinstance(allSkills, collections.Iterable):
            for skill in allSkills:

                if isinstance(skill, collections.Iterable):
                    if 'id_' in skill:
                        hasUserThisSkill = False;

                        if isinstance(usersSkills, collections.Iterable):
                            for userSkill in usersSkills:

                                if isinstance(userSkill, collections.Iterable):
                                    if TimecardUsersSkills.skill_id_ in userSkill:

                                        if userSkill[TimecardUsersSkills.skill_id_] == str(skill['id_']):
                                            hasUserThisSkill = True
                                            break


                        if hasUserThisSkill == False:
                            notAppliedUsersSkills.append(skill)

        return notAppliedUsersSkills


    def setNamesToSkills(self, **options):
        l = MyLog().l()
        _users_skills = []

        usersSkills = options['usersSkills']
        allSkills = options['allSkills']

        if iterable(usersSkills):
            for userSkill in usersSkills:
                if iterable(userSkill):
                    if TimecardUsersSkills.skill_id_ in userSkill:
                        for skill in allSkills:
                            if iterable(skill):
                                if 'id_' in skill:
                                    stra = str(skill['id_'])
                                    strb = str(userSkill[TimecardUsersSkills.skill_id_])
                                    if stra == strb:
                                        userSkill['skill_name__'] = skill[TimecardSkills.rus_name_]
                                        _users_skills.append(userSkill)
        return _users_skills


    def getByUserId(self, **options):
        usersSkills = []
        user_id = options['user_id']

        searchDoc = {
            TimecardUsersSkills.user_id_: user_id
        }

        docs = []
        cursor = None

        with MyDB:
            cursor = TimecardUsersSkills.find(searchDoc)

        if cursor != None:
            for x in cursor:
                docs.append(x)

        return docs

    def getForMainPageByUserId(self, **options):
        usersSkills = []
        user_id = options['user_id']

        searchDoc = {
            TimecardUsersSkills.user_id_: user_id,
            TimecardUsersSkills.show_on_main_page_: 1
        }

        docs = []
        cursor = None

        with MyDB:
            cursor = TimecardUsersSkills.find(searchDoc)

        if cursor != None:
            for x in cursor:
                docs.append(x)

        return docs

    def getAllUsersSkills(self):
        usersSkills = []
        with MyDB:
            cursor = TimecardUsersSkills.find({})
            if iterable(cursor):
                for x in cursor:
                    usersSkills.append(x)

        return usersSkills


    def add(self, **options):
        p = MyLog().p()
        result = None
        resultInsert = False
        l = MyLog().l()
        userId = options['userId']
        skillId = options['skillId']
        insertDoc = {
            TimecardUsersSkills.user_id_: userId,
            TimecardUsersSkills.skill_id_: skillId,
        }

        searchResult = None
        searchResult = self.existsSame(userId = userId, skillId = skillId)

        if searchResult == None:
            with MyDB:
                resultInsert = TimecardUsersSkills.insert(insertDoc)
                result = resultInsert
        else:
            result = '0'
        p(resultInsert, 'resultInsert')
        return result


    def _update_(self, **options):

        result = None
        l = MyLog().l()
        userId = options['userId']
        skillId = options['skillId']
        description = options['description']

        updateDoc = {
            TimecardUsersSkills.user_id_: userId,
            TimecardUsersSkills.skill_id_: skillId,
        }

        searchResult = None
        searchResult = self.existsSame(userId = userId, skillId = skillId)

        # l(searchResult, 'searchResult')


        # utfEncodedDescription = unicode(description.strip(codecs.BOM_UTF8), 'utf-8')
        # utfEncodedDescription = unicode(description, 'utf-8')
        utfEncodedDescription = str(description.encode('utf-8'))

        setDoc = {
                    TimecardUsersSkills.description_: utfEncodedDescription
                }
        # l(setDoc, 'setDoc')


        if searchResult != None:
            with MyDB:
                resultUpdate = TimecardUsersSkills.update(updateDoc,
                {
                    '$set': setDoc
                })
                result = resultUpdate
        else:
            result = '0'

        return result


    def existsSame(self, **options):
        l = MyLog().l()
        p = MyLog().p()
        userId = options['userId']
        skillId = options['skillId']
        response = None
        obj = None
        searchDoc = {
            TimecardUsersSkills.user_id_: userId,
            TimecardUsersSkills.skill_id_: skillId,
        }

        with MyDB:
            resultSearchCursor = TimecardUsersSkills.find(searchDoc)

            for _ in resultSearchCursor:
                obj = _
                break

        if obj != None:
            if '_id' in obj:
                response = obj['_id']

        return response

