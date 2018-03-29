# -*- coding: utf-8 -*-

#########################################################################
# Model for MongoDB collection `timecard_users_languages`
# author DZmitriy Morozov
# email: castor_troy@tut.by
# vk: vk.com/id13245451
# skype: xdoctordog
# 2014
#########################################################################

import logging
import collections
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


class TimecardUsersLanguages(Document):

    config_database = 'tt'
    config_collection = 'timecard_users_languages'

    # id = '_id'

    user_id_ = 'user_id'
    language_id_ = 'language_id'
    language_written_skills_value_ = 'language_written_skills_value'
    language_spoken_skills_value_ = 'language_spoken_skills_value'

    def attachLanguageSkillsToUsers(self, **options):
        l = MyLog().l()
        languageSkills = options['languageSkills']
        users = options['users']
        allUsersLanguages = options['allUsersLanguages']
        for user in users:
            for lang in allUsersLanguages:
                if 'id' in user and 'user_id' in lang and user['id'] == lang['user_id']:
                    if not 'user_language_list' in user:
                        user['user_language_list'] = []

                    if TimecardUsersLanguages.language_written_skills_value_ in lang:
                        if isinstance(languageSkills, collections.Iterable):
                            for skill in languageSkills:
                                if TimecardLanguageSkills.id_ in skill:

                                    strA = str(skill[TimecardLanguageSkills.id_])
                                    strB = str(lang[TimecardUsersLanguages.language_written_skills_value_])

                                    if strA == strB:
                                        if TimecardLanguageSkills.rus_name_ in skill:
                                            lang['skill_name_written'] = skill[TimecardLanguageSkills.rus_name_]

                                    strA = str(skill[TimecardLanguageSkills.id_])
                                    strB = str(lang[TimecardUsersLanguages.language_spoken_skills_value_])
                                    if strA == strB:
                                        # FIXME: add changing skill name by selected language
                                        if TimecardLanguageSkills.rus_name_ in skill:
                                            lang['skill_name_spoken'] = skill[TimecardLanguageSkills.rus_name_]

                    user['user_language_list'].append(lang)
        # l(users, 'users39406')
        return users




    def groupBy(self, **options):
        response = None
        l = MyLog().l()
        allUsersLanguages = options['allUsersLanguages']
        group_by = options['group_by']
        groupedLanguages = {}

        for userLanguage in allUsersLanguages:
            if group_by in userLanguage:
                if not group_by in groupedLanguages:
                    groupedLanguages[group_by] = []
                groupedLanguages[group_by].append(userLanguage)


        for k, group in groupedLanguages.iteritems():
            if response == None:
                response = []
            response.append(group)

        return response




    def remove_user_language(self, **options):
        result = None

        user_id = options['user_id']
        language_id = options['language_id']

        with MyDB:
            result = TimecardUsersLanguages.remove(
            {
                TimecardUsersLanguages.user_id_: user_id,
                TimecardUsersLanguages.language_id_: ObjectId(language_id),
            })
        return result


    def getAllUserLanguages(self, **options):
        l = MyLog().l()
        obj = None

        allNamesLanguages = TimecardLanguages().getAll();

        l(allNamesLanguages, 'allNamesLanguages');

        mlist = []
        with MyDB:
            doc = {
                TimecardUsersLanguages.user_id_ : options['user_id'],
            }
            _ = TimecardUsersLanguages.find(doc)

            for x in _:
                doc = {
                    TimecardUsersLanguages.user_id_: x[TimecardUsersLanguages.user_id_],
                    TimecardUsersLanguages.language_id_: str(x[TimecardUsersLanguages.language_id_]),
                    TimecardUsersLanguages.language_written_skills_value_: x[TimecardUsersLanguages.language_written_skills_value_],
                    TimecardUsersLanguages.language_spoken_skills_value_: x[TimecardUsersLanguages.language_spoken_skills_value_],
                }

                for el in allNamesLanguages:
                    # l(el[TimecardLanguages._id], 'el[TimecardLanguages._id]')
                    # l(x[TimecardUsersLanguages.language_id_], 'x[TimecardUsersLanguages.language_id_]')
                    # l(el[TimecardLanguages.name_], 'el[TimecardLanguages.name_]')
                    if el[TimecardLanguages._id] == x[TimecardUsersLanguages.language_id_]:
                        doc[TimecardLanguages.name_] = el[TimecardLanguages.name_]

                mlist.append(doc);
        # l(mlist, 'mlist')
        return mlist

    def getAllUsersLanguages(self):
        l = MyLog().l()
        allNamesLanguages = TimecardLanguages().getAll()
        # l(allNamesLanguages, 'allNamesLanguages9078564876')
        mlist = []
        with MyDB:
            doc = {}
            cursor = TimecardUsersLanguages.find(doc)

        for doc in cursor:
            for language in allNamesLanguages:
                if language[TimecardLanguages._id] == doc[TimecardUsersLanguages.language_id_]:
                    doc[TimecardLanguages.name_] = language[TimecardLanguages.name_]
                    l(doc[TimecardLanguages.name_], 'doc[TimecardLanguages.name_]')
            mlist.append(doc)
        return mlist

    def _find_(self, **options):
        obj = None
        with MyDB:
            doc = {
                TimecardUsersLanguages.user_id_ : options['user_id'],
                TimecardUsersLanguages.language_id_ : ObjectId(options['language_id']),
            }
            _ = TimecardUsersLanguages.find(doc)

            for x in _:
                obj = x;
                break;
        return obj




    def add(self, **options):
        response = None
        l = MyLog().l()


        insertedDocId = None

        sameLang = self._find_( user_id = options['user_id'],
                     language_id = options['language_id']
                     )

        if sameLang == None:
            with MyDB:
                doc = {
                    TimecardUsersLanguages.user_id_ : options['user_id'],
                    TimecardUsersLanguages.language_id_ : ObjectId(options['language_id']),

                    # FIXME: add using NumberInt() to next two lines
                    TimecardUsersLanguages.language_written_skills_value_ : options['language_written_skills_value'],
                    TimecardUsersLanguages.language_spoken_skills_value_ : options['language_spoken_skills_value'],

                    'timestamp': datetime.datetime.now(),
                }
                insertedDocId = TimecardUsersLanguages.insert(doc)
                response = insertedDocId
        else:
            response = sameLang

        return response

    def _update_(self, **options):
        l = MyLog().l()

        insertResult = self.add(
            user_id = options['user_id'],
            language_id = options['language_id'],
            language_written_skills_value = None,
            language_spoken_skills_value = None,
         )

        result = None
        with MyDB:
            findDoc = {
                            TimecardUsersLanguages.user_id_: options['user_id'],
                            TimecardUsersLanguages.language_id_: ObjectId(options['language_id']),
                        }

            setDoc = {'$set':
                         {
                            TimecardUsersLanguages.language_written_skills_value_ : options['language_written_skills_value'],
                            TimecardUsersLanguages.language_spoken_skills_value_ : options['language_spoken_skills_value'],
                         }
                    }


            result = TimecardUsersLanguages.update( findDoc, setDoc, upsert = False,multi = False)
        return result
