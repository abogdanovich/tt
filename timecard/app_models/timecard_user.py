# -*- coding: utf-8 -*-

#########################################################################
# Model for MongoDB collection `timecard_user`
# author Dzmitriy Morozov
# email: castor_troy@tut.by
# vk: vk.com/id13245451
# skype: xdoctordog
# 2014
#########################################################################

import logging
from humbledb import Document
from MyDB import MyDB
# from timecard.models import *

import datetime
from timecard.app_classes.MyLog import MyLog
# from timecard_languages import TimecardLanguages
# from timecard_language_skills import TimecardLanguageSkills
# from bson.objectid import ObjectId
import humbledb
import collections


from ..doctordog import *


class TimecardUser(Document):
    config_database = 'tt'
    config_collection = 'timecard_user'

    #  KEYS
    id_ = 'id'
    name_ = 'name'
    surname_ = 'surname'
    login_ = 'login'
    dep_ = 'dep'
    group_ = 'group'
    accessLevel_ = 'accessLevel'
    status_ = 'status'
    office_ = 'office'
    avator_ = 'avator'
    email_ = 'email'
    fb_ = 'fb'
    twitter_ = 'twitter'
    skype_ = 'skype'
    hb_ = 'hb'
    phone_ = 'phone'
    gender_ = 'gender'
    ua_ = 'us'
    counter01_ = 'counter01'
    voted_ = 'voted'
    profession_ = 'profession'

    can_edit_position_skill_ = 'can_edit_position_skill'
    can_edit_language_skill_ = 'can_edit_language_skill'
    can_edit_skill_ = 'can_edit_skill'

    # __values = []
    # # VALUES
    # __values[TimecardUser.id_] = None
    # __values[TimecardUser.name_] = None
    # __values[TimecardUser.surname_] = None
    # __values[TimecardUser.login_] = None
    # __values[TimecardUser.dep_] = None
    # __values[TimecardUser.group_] = None
    # __values[TimecardUser.accessLevel_] = None
    # __values[TimecardUser.status_] = None
    # __values[TimecardUser.office_] = None
    # __values[TimecardUser.avator_] = None
    # __values[TimecardUser.email_] = None
    # __values[TimecardUser.fb_] = None
    # __values[TimecardUser.twitter_] = None
    # __values[TimecardUser.skype_] = None
    # __values[TimecardUser.hb_] = None
    # __values[TimecardUser.phone_] = None
    # __values[TimecardUser.gender_] = None
    # __values[TimecardUser.counter01_] = None
    # __values[TimecardUser.voted_] = None
    # __values[TimecardUser.profession_] = None

    # def __init__(self, **options):
    #     l = MyLog().l()
    #     result = None



    def unblockSkillEditByUserId(self, employeeId):
        l = MyLog().l()
        p = MyLog().p()

        response = False
        result = None
        criteriaDoc = {TimecardUser.id_: int(employeeId)}
        updateDoc = { "$set": { TimecardUser.can_edit_skill_: 1 } }

        with MyDB:
           result = TimecardUser.update(criteriaDoc, updateDoc)

        if isinstance(result, collections.Iterable):
            if 'updatedExisting' in result:
                if result['updatedExisting'] == True:
                    response = result['updatedExisting']

        return response



    def blockSkillEditByUserId(self, employeeId):
        l = MyLog().l()
        p = MyLog().p()

        response = False
        result = None
        criteriaDoc = { TimecardUser.id_: int(employeeId) }
        updateDoc = None
        updateDoc = { "$set": { TimecardUser.can_edit_skill_: 0 } }

        with MyDB:
            result = TimecardUser.update(criteriaDoc, updateDoc)

            l(result, 'result UPDATING')


        if isinstance(result, collections.Iterable):
            if 'updatedExisting' in result:
                l(result['updatedExisting'], 'result[\'updatedExisting\'] UPDATING')
                if result['updatedExisting'] == True:
                    response = result['updatedExisting']

        return response



    def unblockLanguageEditByUserId(self, employeeId):
        l = MyLog().l()
        p = MyLog().p()

        response = False
        criteriaDoc = {TimecardUser.id_: int(employeeId)}
        updateDoc = { "$set": { TimecardUser.can_edit_language_skill_: 1 } }

        l(criteriaDoc, 'criteriaDoc')
        l(updateDoc, 'updateDoc')
        with MyDB:
            response = TimecardUser.update(criteriaDoc, updateDoc)

        return response


    def blockLanguageEditByUserId(self, employeeId):
        l = MyLog().l()
        p = MyLog().p()

        response = False
        criteriaDoc = {TimecardUser.id_: int(employeeId)}
        updateDoc = { "$set": { TimecardUser.can_edit_language_skill_: 0 } }

        l(criteriaDoc, 'criteriaDoc')
        l(updateDoc, 'updateDoc')
        with MyDB:
            response = TimecardUser.update(criteriaDoc, updateDoc)

        return response




    def setOfficeName(self, **options):
        response = None

        users = options['users']
        allOffices = options['allOffices']

        for user in users:
            for office in allOffices:
                if 'full_name' in office \
                    and 'short_name' in office \
                    and 'office' in user  \
                    and office['short_name'] == user['office']:

                    user['office_name__'] = office['full_name']

        return users



    def my_save(self):
        l = MyLog().l()
        p = MyLog().p()
        l('OLOLO TROLOLO Method my_save() do nothing')
        l('ATTENTION: Method my_save() do nothing')
        p('OLOLO TROLOLO Method my_save() do nothing')
        p('ATTENTION: Method my_save() do nothing')
        result = None

        # with MyDB:
        #     # objA = []  # list
        #     # objB = ()  # tuple
        #     objC = {}  # dict
        #
        #     setDoc = {}
        #     if self.__values[TimecardUser.name_] != None:
        #         setDoc[TimecardUser.name_] = self.__values[TimecardUser.name_]
        #
        #     result = TimecardUser.update(
        #         {
        #             TimecardUser.id_: self[TimecardUser.id_],
        #         },
        #         {'$set': setDoc
        #         },
        #         upsert = False,
        #         multi = False
        #     )
        return result



    def leaveWorkPlace(self, userId):
        result = None
        with MyDB:
            result = TimecardUser.update(
                {
                    TimecardUser.id_: userId,
                },
                {'$set':
                     {
                         TimecardUser.status_: 0
                     }
                },
                upsert = False,
                multi = False
            )
        return result


    def cameToWorkPlace(self, userId):
        result = None
        with MyDB:
            result = TimecardUser.update(
                {
                    TimecardUser.id_: userId,
                },
                {'$set':
                     {
                         TimecardUser.status_: 1
                     }
                },
                upsert = False,
                multi = False
            )
        return result


    def getNotAppliedOnProjectEmployee(self, _users, appliedEmployeeIds):
        # notAppliedOnProjectUsers = {} # dict | notAppliedOnProjectUsers[i] = user
        notAppliedOnProjectUsers = [] # list

        i = 0

        for user in _users:
            if user['id'] not in appliedEmployeeIds:
                user['order'] = i
                notAppliedOnProjectUsers.append(user)
                i+=1

        return notAppliedOnProjectUsers

    def getAllUsers(self, **options):
        l = MyLog().l()
        p = MyLog().p()
        users = []
        order_by = getSimpleVal(options, 'order_by')
        i = 0
        with MyDB:
            if order_by != None:
                cursor = TimecardUser.find().sort(order_by, humbledb.ASC)
            else:
                cursor = TimecardUser.find()

            if iterable(cursor):
                for x in cursor:
                    x['order'] = i
                    i += 1
                    users.append(x)
        return users

    def groupBy(self, **options):
        l = MyLog().l()
        group_by = options['group_by']
        users = options['users']

        groups = {}
        for user in users:
            if group_by in user:
                if not user[group_by] in groups:
                    groups[user[group_by]] = []
                groups[user[group_by]].append(user)
        return groups


    def setCurrentLocationOrder(self, **options):
        l = MyLog().l()
        p = MyLog().p()
        me = options['me']
        groupedUsers = options['groupedUsers']
        groups = []

        if 'office' in me and me['office'] in groupedUsers:
            # l(groupedUsers[me['office']], '39024uht930h0949groupedUsers[me[office]]') # projectList__
            groups.append(groupedUsers[me['office']])
            del groupedUsers[me['office']]

        for groupName, group in groupedUsers.iteritems():
            groups.append(group)

        return groups

    def me(self, userId):
        me = []
        with MyDB:
            cursor = TimecardUser.find( { TimecardUser.id_: userId })
            for x in cursor:
                me = x
                break

        return me


    def getUsersNotInList(self, ids):
        appliedEmployees = []
        with MyDB:
            cursor = TimecardUser.find( { TimecardUser.id_: {'$nin' :ids} })
            appliedEmployees =[x for x in cursor]
        return appliedEmployees

    def getUsersByIds(self, ids):
        appliedEmployees = []
        with MyDB:
            cursor = TimecardUser.find( { TimecardUser.id_: {'$in' :ids} })
            appliedEmployees =[x for x in cursor]
        return appliedEmployees



