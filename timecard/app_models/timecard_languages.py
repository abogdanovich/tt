# -*- coding: utf-8 -*-

#########################################################################
# Model for MongoDB collection `timecard_languages`
# author DZmitriy Morozov
# email: castor_troy@tut.by
# vk: vk.com/id13245451
# skype: xdoctordog
# 2014
#########################################################################
# from reportlab.lib.utils import c

from timecard.app_models.timecard_user import *


import logging
from humbledb import Document
from MyDB import MyDB

# from timecard.app_models.timecard_user import TimecardUser
# from timecard.models import *

import datetime
from ..doctordog import *
from ..app_classes.MyLog import MyLog
from bson.objectid import ObjectId
import humbledb


class TimecardLanguages(Document):

    config_database = 'tt'
    config_collection = 'timecard_languages'

    _id = '_id'
    name_ = 'name'

    def getNameByLanguageId(self, **options):
        language_id = options['language_id']

        name = None
        doc = None
        with MyDB:
            _ = TimecardLanguages.find({TimecardLanguages._id: ObjectId(language_id)})

        for x in _:
            doc = x
            break

        if TimecardLanguages.name_ in doc:
            name = doc[TimecardLanguages.name_]

        return name

    def prepareForTemplate(self, **options):
        allLanguages = options['allLanguages']
        l = MyLog().l()
        p = MyLog().p()
        response = []
        for language in allLanguages:
            # l(TimecardLanguages.language_id_, 'TimecardLanguages.language_id_')
            # l(x[TimecardLanguages.language_id_], 'x[TimecardLanguages.language_id_')
            # l(x, 'x')
            # l(x['_id'], 'x[_id]')
            # l(x['name'], 'x[name]')
            response.append({
                'id': str(language['_id']),
                TimecardLanguages.name_: language[TimecardLanguages.name_],
            })
        return response


    def getAll(self):
        l = MyLog().l()
        p = MyLog().p()
        objects = []
        with MyDB:
            cursor = TimecardLanguages.find({})
            p(cursor, 'cursor')
            # l(cursor, 'cursor')
            for lang in cursor:
                # p(lang, 'lang')
                # l(lang, 'lang')
                objects.append(lang)
        return objects


    #
    # def getLanguageById(self, languageId):
    #     object = None
    #     with MyDB:
    #         cursor = TimecardLanguages.find({TimecardLanguages.language_id_: languageId})
    #         for el in cursor:
    #             # object = el['_id']
    #             object = el
    #             break
    #     return object


