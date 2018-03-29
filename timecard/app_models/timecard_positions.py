# -*- coding: utf-8 -*-

#########################################################################
# Model for MongoDB collection `timecard_positions`
# author DZmitriy Morozov
# email: castor_troy@tut.by
# vk: vk.com/id13245451
# skype: xdoctordog
# 2014
#########################################################################

import logging
from humbledb import Document
from MyDB import MyDB
# from timecard.models import *
import humbledb
import datetime
from ..doctordog import *
from ..app_classes.MyLog import MyLog
from bson.objectid import ObjectId

class TimecardPositions(Document):

    config_database = 'tt'
    config_collection = 'timecard_positions'

    _id = '_id'

    name_ = 'name'
    rus_name_ = 'rus_name'



    def getNameByPositionId(self, **o):
        l = MyLog().l()
        doc = None
        name = None
        positionId = getSimpleVal(o, 'positionId')

        l(isValidObjectId(positionId), 'isValidObjectId(positionId)')

        if isValidObjectId(positionId):
            searchDoc = {
                TimecardPositions._id: ObjectId(positionId)
            }

            l(searchDoc, 'searchDoc')

            with MyDB:
                cursor = TimecardPositions.find(searchDoc)

                if iterable(cursor):
                    for x in cursor:
                        l(x, 'x')
                        if iterable(x):
                            if TimecardPositions.rus_name_ in x:
                                name = x[TimecardPositions.rus_name_]

        return name



    def getPositionNameById(self, **o):

        doc = None
        name = None

        positionId = getSimpleVal(o, 'positionId')

        findDoc = {
            TimecardPositions._id: ObjectId(positionId)
        }

        with MyDB:
            cursor = TimecardPositions.find(findDoc)

        if iterable(cursor):
            for x in cursor:
                doc = x
                break

        if iterable(doc):
            if TimecardPositions.rus_name_ in doc:
                name = doc[TimecardPositions.rus_name_]

        return name




    def init(self):
        l = MyLog().l()

        all = []

        names = [
            ('Project Manager', 'Менеджер проектов'),
            ('Developer', 'Разработчик'),
            ('Designer', 'Дизайнер'),
            ('Tester', 'Тестировщик'),
            ('System administrator', 'Системный администратор'),
            ('Boss', 'Босс'),
            ('HR-manager', 'Менеджер по персоналу'),
        ]

        for name, rusname in names:
            doc = {
                TimecardPositions.name_: name,
                TimecardPositions.rus_name_: rusname,
            }

            with MyDB:
                id = TimecardPositions.insert(doc)
                all.append(id)
        return all



    def clean(self):
        p = MyLog().p()
        removeResult = None
        with MyDB:
            removeResult = TimecardPositions.remove({})
        return removeResult


    def getAll(self):
        l = MyLog().l()
        p = MyLog().p()
        all = []
        with MyDB:
            cursor = TimecardPositions.find({})

        if iterable(cursor):
            for doc in cursor:
                doc = addObjectID(doc)
                all.append(doc)

        return all

    def showAll(self):
        p = MyLog().p()
        all = self.getAll()
        for x in all:
            p(x)
        return all



