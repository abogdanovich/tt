# -*- coding: utf-8 -*-

#########################################################################
# Yes This iZ that file which contains all neccessary functions for EVERYTHING
# Yes It is exists for real XD
# author DZmitriy Morozov
# email: castor_troy@tut.by
# vk: vk.com/id13245451
# skype: xdoctordog
# 2014
# original
#########################################################################



import collections
from __builtin__ import isinstance
from bson.objectid import ObjectId

from app_classes.MyLog import MyLog
# from timecard.app_classes.Switch import switch
# from timecard.app_models.timecard_users_skills import *

def toObjectId(val):

    response = False

    if not type(val) == ObjectId:
        if type(val) == str or isinstance(val, unicode):
            val = ObjectId(val)
            response = val
    else:
        response = val

    return response


def is_int(val):
    response = False

    if type(val) == int:
        response = True

    return response

def iterable(val):
    response = False
    if isinstance(val, collections.Iterable):
        response = True
    return response

def is_str(val):
    response = False
    if \
        type(val) == str \
        or \
        isinstance(val, unicode):
        response = True

    return response

def my_explode(val):
    # val = str(val.encode('utf-8'))
    val = val.lower()

    edits = [(',', ' '), (';', ' ')]
    for search, replace in edits:
        val = val.replace(search, replace)

    lst = val.split(' ')

    _ls = []
    for name in lst:
        if name != '':
            _ls.append(name)

    return _ls


def isValidObjectId(val):
    response = False

    if type(val) == ObjectId:
        response = True
    elif is_str(val):
        if len(val) == len('541a89374f452d177481b671'):
            response = True
    return response

def toInt(val):

    if type(val) == int or type(val) == unicode:
        val = int(val)
    return val


def getVal(object, key):
    val = None
    if type(key) == str:
        if isinstance(object, collections.Iterable):
            if key in object:
                val = object[key]
    return val

def getSimpleVal(object, key):
    val = None
    if type(key) == str:
        if key in object:
            val = object[key]
    return val



def myToString(objects):
    response = {}
    # print 'myToString'

    iterable = isinstance(objects, collections.Iterable)

    if iterable:
        # print 'IF: '
        for obj in objects:
            # print 'objects[', obj, ' ] : ', objects[ obj ]
            # print 'isinstance(objects[obj], collections.Iterable):  ',isinstance(objects[obj], collections.Iterable)
            obj = str(obj)
            # print 'objects[', obj, ']', objects[obj]
    else:
        objects = str(objects)
        # print 'ELSE: objects [ ', objects, ' ] '

    # print 'myToString END '
    return objects




def addObjectIDs(objects):

    if isinstance(objects, collections.Iterable):
        for obj in objects:
            addObjectID(obj)
    return objects



def addObjectID(obj):
    l = MyLog().l()
    # l(isinstance(obj, collections.Iterable), 'isinstance(obj, collections.Iterable)')
    # l(obj, ';obj')
    if isinstance(obj, collections.Iterable):
        b = '_id' in obj and not 'id__' in obj;
        # l(b, '_id in obj and not id__ in obj')
        if b:
            obj['id__'] = obj['_id']
    return obj

def is_in(el, mass):
    l = MyLog().l()
    response = False
    for _ in mass:
        if el == _:
            response = True
            break
    return response



#
# l = MyLog().l()
# listA = [
#     {'id': 1, 'name': 'Alena'},
#     {'id': 2, 'name': 'Anna'},
#     {'id': 3, 'name': 'Annastasia'}, ]
#
# listB = [
#     {'userid': 1, 'mobilePhone': '+375291112233'},
#     {'userid': 2, 'mobilePhone': '+375291000233'},
#     {'userid': 2, 'mobilePhone': '+375331000233'},
#     {'userid': 3, 'mobilePhone': '+375291470234'},
#     {'userid': 3, 'mobilePhone': '+375295070234'},
#     ]
# keyA = 'id'
# keyB = 'userid'
# joinType = 'much_to_much'
# containerName = '__TELEPHONES__'
# resultA = my_join(listA, listB, keyA, keyB, containerName, joinType )
#
# l(resultA, 'resultA OF my_join() <<<---')


def my_join(listA, listB, keyA, keyB, containerName, joinType = 'much_to_much', **o):

    debug = getSimpleVal(o, 'debug')

    l = MyLog().l()

    # l(joinType, 'joinType4328906')

    # l(isinstance(listA, collections.Iterable), 'isinstance(listA, collections.Iterable)')
    # l(isinstance(listB, collections.Iterable), 'isinstance(listB, collections.Iterable)')

    # l(type(keyA), 'type(keyA)')
    # l(type(keyB), 'type(keyB)')
    #
    #
    # l(type(joinType), 'type(joinType)')
    # l(type(containerName), 'type(containerName)')

    if type(keyA) == str \
    and type(keyB) == str \
    and isinstance(listA, collections.Iterable)\
    and isinstance(listB, collections.Iterable)\
    and type(joinType) == str\
    and type(containerName) == str:

        firstTime = True

        # l(joinType, 'f8nw4ui')
        if joinType == 'one_to_one' or joinType == 'much_to_much':
            # l(joinType, 'joinType89307ywt9ghern')

            for aEl in listA:
                # l(aEl, 'aEl')
                if isinstance(keyA, collections.Iterable):
                    firstTime = True # For checking if our aEl has NO such key initially
                    if keyA in aEl:
                        # l(keyA, 'keyA 3409875639')
                        if firstTime == True and not containerName in aEl:
                            firstTime = False
                            if joinType == 'one_to_one':
                                aEl[containerName] = None
                            else:
                                aEl[containerName] = []

                        for bEl in listB:
                            if isinstance(bEl, collections.Iterable):
                                if keyB in bEl:
                                    strValueB = str(bEl[keyB])
                                    strValueA = str(aEl[keyA])
                                    doc = {}
                                    doc['strValueA'] = strValueA
                                    doc['strValueB'] = strValueB
                                    # l(doc, '4893675370984doc')
                                    if strValueB == strValueA:

                                        if debug:
                                            l(strValueB + ' == ' + strValueA)
                                            l(joinType, 'joinType')

                                        if joinType == 'one_to_one':
                                            if aEl[containerName] == None:
                                                aEl[containerName] = bEl
                                        else:
                                            aEl[containerName].append(bEl)
                                    # else:
                                    #     l('WOWwwewhfjiniejwoehnfg___NO')
    return listA




# # FIXME: Make universal method
# def clearListFromAppliedSkills(self, **options):
#     l = MyLog().l()
#
#     notAppliedUsersSkills = []
#
#     # return notAppliedUsersSkills
#
#     usersSkills = options['usersSkills']
#     allSkills = options['allSkills']
#
#     if isinstance(allSkills, collections.Iterable):
#         for skill in allSkills:
#
#             if isinstance(skill, collections.Iterable):
#                 if 'id_' in skill:
#                     hasUserThisSkill = False;
#
#                     if isinstance(usersSkills, collections.Iterable):
#                         for userSkill in usersSkills:
#
#                             if isinstance(userSkill, collections.Iterable):
#                                 if TimecardUsersSkills.skill_id_ in userSkill:
#
#                                     if userSkill[TimecardUsersSkills.skill_id_] == str(skill['id_']):
#                                         hasUserThisSkill = True
#                                         break
#
#
#                     if hasUserThisSkill == False:
#                         notAppliedUsersSkills.append(skill)
#
#     return notAppliedUsersSkills
