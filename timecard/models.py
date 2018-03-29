# -*- coding: utf-8 -*-

#########################################################################
# TimeCard models module
# author Alex Bogdanovich
# 2012
#########################################################################

import logging
from django.db import models
import humbledb
from humbledb import Document
import datetime
import json
from doctordog import *

from app_models.MyDB import MyDB
from app_models.timecard_customers import TimecardCustomers
from app_classes.MyLog import MyLog
from bson.objectid import ObjectId

from timecard.app_models.timecard_offices import TimecardOffices
from timecard.app_models.timecard_user import TimecardUser
# from timecard.app_models.project_appended_employee_role import ProjectAppendedEmployeeRoleDoc
from timecard.app_models.project_appended_employee_role import ProjectAppendedEmployeeRoleDoc
from timecard.app_models.timecard_projects import TimecardProjects
from timecard.app_classes.MyDate import *

#GENDER CHOICE

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)
# User social networks

USER_NETWORK_CHOICES = (
    ('SK','Skype'),
    ('TW','Twitter'),
    ('FB','FaceBook'),
    ('VK','Vkontakte'),
    ('OD','Odnoklassniki'),
    ('GP','Google plus'),
)

class Image(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.FileField(upload_to="images/")

    def __unicode__(self):
        return self.image.name
# import re

###########################################################################################################


# TODO: REMOVE CAREFULLY usage of this class cause There is no need more
class ProjectAppendedEmployeeDoc(Document):
    config_collection = 'project_appended_employee'
    config_database = 'tt'

    userId = 'userId'
    project_appended_employee = 'project_appended_employee'
    projectId = 'projectId'  # !ATTENTION! Set only for already created projects
    # Cause when this key is absent the project's employee are set to unexisting/hav been creating project

    def bindEmployeeToProject(self, appenderId, projectId):

        result = None

        with MyDB:
            result = ProjectAppendedEmployeeDoc.update(
                {
                    ProjectAppendedEmployeeDoc.userId: appenderId,
                    ProjectAppendedEmployeeDoc.projectId: { '$exists': False }
                #   ProjectAppendedEmployeeRoleDoc.projectId: { '$exists': False }
                },
                {
                    '$set': { ProjectAppendedEmployeeDoc.projectId: projectId }
                }
            )

        return result



    def removeIdFromStr(self, id, string):
        response = []
        ids = string.split(',')

        for _ in ids:
            if str(_) != str(id):
                response.append(_)

        __ = ','.join(response)

        return __

    def removeEmployeeFromEmptyProject(self, appenderId, employeeId):
        result = None
        with MyDB:
            doc = ProjectAppendedEmployeeDoc.find({ProjectAppendedEmployeeDoc.userId: appenderId,
                                                   ProjectAppendedEmployeeDoc.projectId: { '$exists': False }})
            __ = None
            for _ in doc:
                __ = {  ProjectAppendedEmployeeDoc.userId: _[ProjectAppendedEmployeeDoc.userId],
                        ProjectAppendedEmployeeDoc.project_appended_employee: _[ProjectAppendedEmployeeDoc.project_appended_employee],
                    }
                break
            resultString = self.removeIdFromStr( employeeId, __[ProjectAppendedEmployeeDoc.project_appended_employee] )
            self.apllyEmployeeOnEmptyProject(appenderId, resultString)

        return False


    def addRoles(self, appliedEmployees, employeesRolesOnProject):

        _ = []
        for empl in appliedEmployees:
            # objA = []  # list
            # objB = ()  # tuple
            objC = {}  # dict


            objC[TimecardUser.id_] = empl[TimecardUser.id_]
            objC[TimecardUser.name_] = empl[TimecardUser.name_]
            objC[TimecardUser.surname_] = empl[TimecardUser.surname_]

            for role in employeesRolesOnProject:
                if int(empl[TimecardUser.id_]) == int(role[ProjectAppendedEmployeeRoleDoc.employeeId]):
                    objC[ProjectAppendedEmployeeRoleDoc.roleOnProject] = role[ProjectAppendedEmployeeRoleDoc.roleOnProject]
                    objC[ProjectAppendedEmployeeRoleDoc.startDayOnProject] = role[ProjectAppendedEmployeeRoleDoc.startDayOnProject]
                    objC[ProjectAppendedEmployeeRoleDoc.finishDayOnProject] = role[ProjectAppendedEmployeeRoleDoc.finishDayOnProject]

            _.append(objC)
        return _


    # list of employee connects to manager ID
    def apllyEmployeeOnEmptyProject(self, appenderId, project_appended_employee):

        doc = {"project_appended_employee" : project_appended_employee,
               "userId": appenderId}
        result = None
        with MyDB:
            ProjectAppendedEmployeeDoc.remove({ProjectAppendedEmployeeDoc.userId: appenderId, ProjectAppendedEmployeeDoc.projectId: { '$exists': False }})
            result = ProjectAppendedEmployeeDoc.insert(doc)
        return result

    def getProjectAppendedEmployee(self, userId):
        doc = None
        with MyDB:
            doc = ProjectAppendedEmployeeDoc.find(
                {
                    ProjectAppendedEmployeeDoc.userId: userId,
                    ProjectAppendedEmployeeDoc.projectId: { '$exists': False }
                }
            )
        return doc

    def getAppliedEmployeesToRealProjectByUserId(self, project_id):
        l = MyLog().l()
        p = MyLog().p()
        listAppliedUsers = []
        ids, rolesUsers = ProjectAppendedEmployeeRoleDoc().getEmployeeIdsOnRealProject( project_id )

        appliedEmployees = TimecardUser().getUsersByIds(ids)

        if iterable(ids):
            for userId in ids:
                l(userId, 'userId987')
                for user in appliedEmployees:
                    if userId == user['id']:
                        listAppliedUsers.append(user)
                        break
        # l(listAppliedUsers, 'listAppliedUsers3897')
        return listAppliedUsers, ids, rolesUsers


    def getAppliedEmployeesToTempProjectByUserId(self, userId):
        l = MyLog().l()
        p = MyLog().p()

        appliedUsers = None
        ids = None

        appliedEmployees = []

        # cursor
        findedListOfEmployesOnEmptyProject = ProjectAppendedEmployeeRoleDoc().getEmployeeIdsOnEmptyProject(userId)

        notesUsers = []
        listUsers = []
        idsArray = []
        if(findedListOfEmployesOnEmptyProject != None):
            for el in findedListOfEmployesOnEmptyProject:
                idsArray.append(int(el[ProjectAppendedEmployeeRoleDoc.employeeId]))
                notesUsers.append(el)

        # l(notesUsers, 'notesUsers')

        appliedEmployees = TimecardUser().getUsersByIds(idsArray)

        for userId in idsArray:
            for user in appliedEmployees:
                if userId == user['id']:
                    listUsers.append(user)
                    break
        return listUsers, idsArray, notesUsers

    def __unicode__(self):
        return unicode("ProjectAppendedEmployeeDoc")

# class HumbleDoc(Document):
#     config_database = 'tt'
#     config_collection = 'example'
#
#     description = 'd'
#     value = 'v'
#     def __unicode__(self):
#         return unicode("str")

class User(models.Model):

    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=40)
    login = models.CharField(max_length=30)

    accessLevel = models.CharField(max_length=1, default=0)
    #################################################
    #accessLevel
    #[0] = normal user - submit hours | post/edit personal report
    #[1] = boss  - view hours | view all time reports for assigned office
    #[2] = admin level - access to admin section | view\submit personal hours, add\delete new users, manage SPAM board, send emails messages
    #[3] - super root - access to any section | all privileges
    #[4] - project manager - submit hours | assign employees to projects |view project reports
    #################################################

    status = models.IntegerField(default=0)
    office = models.CharField(max_length=2)
    dep = models.CharField(max_length=15)
    avator = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, default='@minsk.ximxim.com')
    fb = models.CharField(max_length=100)
    twitter = models.CharField(max_length=100)
    skype = models.CharField(max_length=100)
    hb = models.CharField(max_length=10)
    phone = models.CharField(max_length=255)
    gender = models.CharField(max_length=2, default=1, choices=GENDER_CHOICES) #not used
    ua = models.CharField(max_length=30)
    profession = models.CharField(max_length=30)
    counter01 = models.IntegerField() # form spam counter
    group = models.CharField(max_length=50) #not used for now
    voted = models.IntegerField(default=0)

    def __unicode__(self):
        return unicode("%s" % self.login)

class UserTime(models.Model):
    user_id = models.IntegerField()
    time = models.IntegerField()

    def __unicode__(self):
        return unicode("%s" % self.time)

class UserDepartament(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return unicode("%s" % self.name)

class UserProfession(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return unicode("%s" % self.name)

class UserRoles(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return unicode("%s" % self.name)


class UserModule(models.Model):
    user_id = models.IntegerField()
    mod = models.CharField(max_length=20) #module1 | module2 | modulen
    position = models.CharField(max_length=20) #left|right|top
    show = models.IntegerField(default=0)

    def __unicode__(self):
        return unicode("%s" % self.user_id)

class UserPost(models.Model):
    author = models.TextField()
    body = models.CharField(max_length=20000)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode("%s" % self.title)

class UserPostComment(models.Model):
    post_id = models.IntegerField()
    body = models.TextField()
    author = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode("%s: %s" % (self.post, self.body[:60]))

class CalendarDaysOff(models.Model):
    date = models.IntegerField()
    office = models.CharField(max_length=2)
    def __unicode__(self):
        return unicode("%d" % (self.date))

class UserMissedHours(models.Model):
    user = models.CharField(max_length=100)
    umess = models.CharField(max_length=1000)
    date = models.CharField(max_length=10)
    status = models.IntegerField()
    lock_person = models.CharField(max_length=70)
    def __unicode__(self):
        return self.id#############

class Boss_notice(models.Model):
    user = models.IntegerField()
    date = models.CharField(max_length=12)
    notice = models.CharField(max_length=500)

    def __unicode__(self):
        return self.id##############

class User_duty(models.Model):
    user = models.IntegerField()
    date = models.CharField(max_length=25)

    def __unicode__(self):
        return self.id##############

class Projects(models.Model):
    project_name = models.CharField(max_length=25) #project label
    project_desc = models.CharField(max_length=500) #project short description
    project_opened = models.IntegerField() #flag is this project is currently active or not (1 - is active,s 0 - closed)
    project_service = models.CharField(max_length=100, default = '')

    def __unicode__(self):
        return self.id################3

class UserProjectAssignments(models.Model):
    user = models.IntegerField()
    date = models.CharField(max_length=25)
    project = models.IntegerField() #user name surname

    def __unicode__(self):
        return self.id ###############3

class Reports(models.Model):
    #we do not link 'Reports' to the 'User' because if any user will be deleted from db,
    #django automaticaly will delete all the reports associated with user.
    #instead we copy the columns from 'User' table

    #fields below are used now for better time managment and for further sorting
    #####
    week = models.CharField(max_length=2)
    year = models.CharField(max_length=4)
    reporting_date = models.CharField(max_length=10)
    #####
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=30)
    user_surname = models.CharField(max_length=40)
    #fields below can be used later for sorting reports accordingly to the office and department.
    #for now they are worthless.
    #####
    office = models.CharField(max_length=2)
    dep = models.CharField(max_length=15)
    #####
    project_name = models.CharField(max_length=25)
    report = models.CharField(max_length = 10000)
    employee_feedback = models.CharField(max_length = 5000)
    lead_feedback = models.CharField(max_length = 5000)
    # realy spent hours
    hours = models.IntegerField()
    # that is overtime flag. If week reports of user has summary hours above limit it is set as quantity of all spent hours per week (not only overtimed, but all) for all reports
    overtimed = models.IntegerField(default = 0)
    def __unicode__ (self):
        return unicode("%s %s %s %s %s %s" % (self.report, self.employee_feedback, self.employee_name, self.employee_surname, self.project_name, self.lead_feedback))

class Votes(models.Model):
    # here are the counters for votes
    votes_yes = models.IntegerField()
    votes_no = models.IntegerField()
    votes_dontcare = models.IntegerField()
    # here are the descriptions of answers
    votes_yes_desc = models.CharField(max_length = 20)
    votes_no_desc = models.CharField(max_length = 20)
    votes_dontcare_desc = models.CharField(max_length = 20)
    # actual text of question for voting
    question = models.CharField(max_length = 100)
    # every voting must be assigned for offices separately
    office = models.CharField(max_length=2)
    # is voting is actual ir archived
    archived = models.IntegerField(default = 0)
    # we would like to remember who and how voted :)
    votes_yes_who = models.CharField(max_length = 5000)
    votes_no_who = models.CharField(max_length = 5000)
    votes_dontcare_who = models.CharField(max_length = 5000)
    def __unicode__(self):
        return unicode("%s %s %s %s" % (self.question, self.votes_yes_desc, self.votes_no_desc, self.votes_dontcare_desc))

class ProjectThread(models.Model):
    """
    That class is used for projects statistics and user activity measurment

    We do not store all the project assignments ever created. Instead we will store only new assignments.
    If employee is removed from project then we also store that record. But if employee is again assignmented
    hew records is not created.
    """
    #first we have to assign user id
    user_id = models.IntegerField()
    #we have to store user name and surname in case of user deleting from DB
    user_name_surname = models.CharField(max_length=71)
    #we have to set up the role for the user on that project
    user_role = models.IntegerField()
    # that is actual spent hours on that project. It is filled out when thread is closed, otherwise it is 0
    project_id = models.IntegerField()
    # next one is filled with surname and name of user who made this assignment
    who_assigned =models.CharField(max_length=71)
    # next one is filled after assignment we removed. It is also serves as flag that assignment is currently active
    who_unassigned =models.CharField(max_length=71)
    def __unicode__(self):
        return self.id

class Offices(models.Model):
    """
    That class is used for storing info about offices, their names and details
    """
    short_name = models.CharField(max_length = 2)
    full_name = models.CharField(max_length = 30)
    boss_email = models.CharField(max_length = 50)
    mass_email = models.CharField(max_length = 50)
    # the next one is used for correcting results of function utils.show_user_month_hours
    # the only reason for it is difference in time zone between different offices
    time_shift = models.CharField(max_length=10)
    # the next one is used for showing correct weather informer
    # we use informers from pogoda.by
    weather_script = models.CharField(max_length = 1000)
    #
    def __unicode__(self):
        return self.id


class Reservation_Categories(models.Model):
    """
    That class is used for storing different categories.
    All the categories are linked to the offices
    """
    name = models.CharField(max_length=30)
    office = models.CharField(max_length=2)


class Reservation_Objects(models.Model):
    """
    That class is used for storing objects for reservation
    and representing its current state
    """
    name = models.CharField(max_length=30)
    category = models.ForeignKey(Reservation_Categories, db_index=False)
    is_avaliable = models.BooleanField(default=True)
    user = models.ForeignKey(User, db_index=False)


class Reservation_History(models.Model):
    """
    That class is for storing history of activity of reserved objects
    """
    obj = models.ForeignKey(Reservation_Objects, db_index=False)
    event = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=100)
    status = models.BooleanField()
