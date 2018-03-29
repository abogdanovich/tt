# -*- coding: utf-8 -*-

#########################################################################
# Model for MongoDB collection `timecard_customers`
# author DZmitriy Morozov
# email: castor_troy@tut.by
# vk: vk.com/id13245451
# skype: xdoctordog
# 2014
#########################################################################

from humbledb import Document
from MyDB import MyDB
from ..doctordog import *

class TimecardCustomers(Document):

    config_database = 'tt'
    config_collection = 'timecard_customers'

    id_ = 'id'
    name_ = 'name'
    customer_id_ = 'customer_id'
    country_ = 'country'
    address_ = 'address'
    contact_person_ = 'contact_person'
    telephone_ = 'telephone'
    email_ = 'email'
    others_ = 'others'

    def getAllCustomers(self):
        listTimecardCustomers = []
        with MyDB:
            cursor = TimecardCustomers.find()
            # cursor = TimecardCustomers.find().sort(order_by, humbledb.ASC)
            if iterable(cursor):
                for obj in cursor:
                    listTimecardCustomers.append(obj)
        return listTimecardCustomers
