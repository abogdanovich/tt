# -*- coding: utf-8 -*-

#########################################################################
# Model for MongoDB collection `timecard_offices`
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

class TimecardOffices(Document):

    config_database = 'tt'
    config_collection = 'timecard_offices'

    _id = '_id'
    id_ = 'id'
    short_name_ = 'short_name'
    full_name_ = 'full_name'
    boss_email_ = 'boss_email'
    mass_email_ = 'mass_email'
    time_shift_ = 'time_shift'
    weather_script_ = 'weather_script'


    def getAll(self):
        allOffices = []

        with MyDB:
            cursor = TimecardOffices.find({})

            for _ in cursor:
                allOffices.append(_)

        return allOffices






