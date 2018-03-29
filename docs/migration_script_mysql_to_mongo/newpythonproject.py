# -*- coding: utf-8 -*-
import MySQLdb
import pprint

from humbledb import Document
from humbledb import Mongo


collectionNames = [
    'auth_group',
    'auth_group_permissions',
    'auth_message',
    'auth_permission',
    'auth_user',
    'auth_user_groups',
    'auth_user_user_permissions',
    'customers_customer',
    'cv_certificate',
    'cv_contact',
    'cv_cv',
    'cv_cvskill',
    'cv_fl',
    'cv_position',
    'cv_prevproject',
    'cv_prevscreenshot',
    'cv_skill',
    'django_admin_log',
    'django_content_type',
    'django_select2_keymap',
    'django_session',
    'django_site',
    'projects_preset',
    'projects_presetrequirement',
    'projects_project',
    'projects_projectrequirement',
    'projects_screenshot',
    'projects_workgroup',
    'south_migrationhistory',
    'taggit_tag',
    'taggit_taggeditem',
    'taggit_templatetags_amodel',
    'test',
    'timecard_boss_notice',
    'timecard_calendardaysoff',
    'timecard_offices',
    'timecard_projects',
    'timecard_projectthread',
    'timecard_reports',
    'timecard_reservation_categories',
    'timecard_reservation_history',
    'timecard_reservation_objects',
    'timecard_user',
    'timecard_user_duty',
    'timecard_userdepartament',
    'timecard_usermissedhours',
    'timecard_usermodule',
    'timecard_userpost',
    'timecard_userpostcomment',
    'timecard_userprofession',
    'timecard_userprojectassignments',
    'timecard_userroles',
    'timecard_usertime',
    'timecard_votes',
]
# collectionName = "timecard_user"


class MyDB(Mongo):
    # config_host = 'dm-morozov'  # On Windows 7

    config_host = 'localhost'  # On Ubuntu 14
    config_port = 27017

class HumbleDoc(Document):
    config_database = 'tt'
    config_collection = None
    def __unicode__(self):
        return unicode("str")


db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="panda2014", # your password
                      db="timetracker",# name of the data base
                      charset='utf8'
                     )

db.set_character_set('utf8')
cursor = db.cursor()
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')


for collectionName in collectionNames:
    print collectionName

    HumbleDoc.config_collection = collectionName
    cursor.execute("SELECT * FROM " + collectionName)
    numrows = int(cursor.rowcount)
    field_names = [i[0] for i in cursor.description]
    # print field_names
    docs = {}
    results = {}
    j = 0

    for x in range(0,numrows):
        row = cursor.fetchone()
        doc = {}
        i = 0
        for fieldValue in row:

            print 'field_names[i]'  # field name
            print field_names[i]  # field name
            print ']'

            print 'fieldValue['  # field value
            print fieldValue  # field value
            print ']'

            # doc[field_names[i]] = fieldValue
            # doc[field_names[i]] = str(fieldValue).decode('cp1252')
            doc[field_names[i]] = fieldValue
            i+=1
        print doc
        with MyDB:
            result = HumbleDoc.insert(doc)
            docs[j] = doc
            results[j] = result
            j+=1

    print "results ["
    print results
    print "]"
