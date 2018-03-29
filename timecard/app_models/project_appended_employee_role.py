# -*- coding: utf-8 -*-

#########################################################################
# Model for MongoDB collection `project_appended_employee_role`
# author DZmitriy Morozov
# email: castor_troy@tut.by
# vk: vk.com/id13245451
# skype: xdoctordog
# 2014
#########################################################################

from humbledb import Document
from MyDB import MyDB
from timecard.app_classes.MyDate import *

import datetime
from ..doctordog import *
import humbledb
# project_appended_employee_role.py
import collections
from bson.objectid import ObjectId
from in_out_stat import cursor


class ProjectAppendedEmployeeRoleDoc(Document):

    config_collection = 'project_appended_employee_role'
    config_database = 'tt'

    appenderId = 'appenderId'
    employeeId = 'employeeId'
    roleOnProject = 'roleOnProject'

    startDayOnProject = 'startDayOnProject'
    finishDayOnProject = 'finishDayOnProject'

    projectId = 'projectId'  # !ATTENTION! Set only for already created projects
    # Cause when this key is absent the project's employee are set to unexisting/hav been creating project


    removed_from_project_ = 'removed_from_project'



    def appendUserOnRealProject(
            self,
            appenderId,
            projectId,
            employeeId,
            roleOnProject,
            startDayOnProject,
            finishDayOnProject
    ):
        l = MyLog().l()
        result = None

        if type(employeeId) == int:
            projectId = projectId
            employeeId = employeeId

            insertDoc = {
                ProjectAppendedEmployeeRoleDoc.appenderId: appenderId,
                ProjectAppendedEmployeeRoleDoc.projectId: ObjectId(projectId),
                ProjectAppendedEmployeeRoleDoc.employeeId: employeeId,
                ProjectAppendedEmployeeRoleDoc.roleOnProject: roleOnProject,

                ProjectAppendedEmployeeRoleDoc.startDayOnProject: startDayOnProject,
                ProjectAppendedEmployeeRoleDoc.finishDayOnProject: finishDayOnProject,
            }


            l(insertDoc, 'insertDoc88')

            with MyDB:
                removeDoc = {
                    ProjectAppendedEmployeeRoleDoc.appenderId: appenderId,
                    ProjectAppendedEmployeeRoleDoc.projectId: ObjectId(projectId),
                    ProjectAppendedEmployeeRoleDoc.employeeId: employeeId,
                }

                l(removeDoc, 'removeDoc')

                removeResult = ProjectAppendedEmployeeRoleDoc.remove(removeDoc)

                l(removeResult, 'removeResult')

                result = ProjectAppendedEmployeeRoleDoc.insert(insertDoc)

                if type(result) != ObjectId:
                    result = ''
                else:
                    result = str(result)

        return result



    def getProjectsRoleIdsByEmployeeId(self, **options):

        l = MyLog().l()
        projectsRoles = []
        employeeId = options['employeeId']

        findDoc = {
            ProjectAppendedEmployeeRoleDoc.employeeId: employeeId
        }

        with MyDB:
            cursor = ProjectAppendedEmployeeRoleDoc.find(findDoc)
            if isinstance(cursor, collections.Iterable):
                for roleOnProject in cursor:
                    projectsRoles.append(roleOnProject)

        return projectsRoles


    def getRolesByEmployeeId(self, **options):
        l = MyLog().l()
        projectsRoles = []
        employeeId = getVal(options, 'employeeId')
        if is_int(employeeId):
            findDoc = {
                ProjectAppendedEmployeeRoleDoc.employeeId: employeeId
            }
            with MyDB:
                cursor = ProjectAppendedEmployeeRoleDoc.find(findDoc)
                if iterable(cursor):
                    for roleOnProject in cursor:
                        roleOnProject = addObjectID(roleOnProject)
                        projectsRoles.append(roleOnProject)
        return projectsRoles


    def getEmployeeIdsOnEmptyProject_(self, appenderId):
        l = MyLog().l()
        p = MyLog().p()
        findedListOfEmployes = None
        _ = []

        searchDoc =\
        {
            ProjectAppendedEmployeeRoleDoc.appenderId: appenderId,
            ProjectAppendedEmployeeRoleDoc.projectId: { '$exists': False }
        }

        # l(searchDoc, 'searchDoc')


        with MyDB:
            findedListOfEmployes = ProjectAppendedEmployeeRoleDoc.find(searchDoc)
        for x in findedListOfEmployes:
            _.append(str(x['_id']))
        return _


    def getEmployeeOnEmptyProject(self, appenderId):
        l = MyLog().l()
        p = MyLog().p()
        findedListOfEmployes = None
        _ = []

        searchDoc =\
        {
            ProjectAppendedEmployeeRoleDoc.appenderId: appenderId,
            ProjectAppendedEmployeeRoleDoc.projectId: { '$exists': False }
        }

        l(searchDoc, 'searchDoc')


        with MyDB:
            findedListOfEmployes = ProjectAppendedEmployeeRoleDoc.find(searchDoc)
        for x in findedListOfEmployes:
            _.append(x)
        return _


    def hasEmployeeValidStartDayOnEmptyProject(self, appenderId):
        response = False
        isBroken = False
        employee = self.getEmployeeOnEmptyProject(appenderId)
        if iterable(employee):
            for usrRole in employee:
                startDate = getSimpleVal(usrRole, 'startDayOnProject')
                if startDate == None:
                    isBroken = True
                    break
                else:
                    isValid = MyDate().isValidDate(startDate)
                    if isValid == False:
                        isBroken = True
                        break

        if isBroken == False:
            response = True

        return response




    def hasEmployeeValidStartDayOnRealProject(self, projectId):
        response = False
        isBroken = False
        employee = self.getEmployeeOnRealProject(projectId)
        if iterable(employee):
            for usrRole in employee:
                startDate = getSimpleVal(usrRole, 'startDayOnProject')
                if startDate == None:
                    isBroken = True
                    break
                else:
                    isValid = MyDate().isValidDate(startDate)
                    if isValid == False:
                        isBroken = True
                        break

        if isBroken == False:
            response = True

        return response






    def getEmployeeOnRealProject(self, project_id):
        l = MyLog().l()
        p = MyLog().p()
        findedListOfEmployes = None
        _ = []
        searchDoc =\
        {
            ProjectAppendedEmployeeRoleDoc.projectId: ObjectId(project_id)
        }

        # l(searchDoc, 'getEmployeeIdsOnRealProject():: searchDoc')

        with MyDB:
            cursor = ProjectAppendedEmployeeRoleDoc.find(searchDoc)

        if iterable(cursor):
            for x in cursor:
                _.append(x)

        # l(cursor, 'getEmployeeIdsOnRealProject():: findedListOfEmployes()')
        return _




    def getEmployeeIdsOnRealProject(self, project_id):
        l = MyLog().l()
        p = MyLog().p()

        searchDoc =\
        {
            ProjectAppendedEmployeeRoleDoc.projectId: ObjectId(project_id)
        }
        ids = []
        roles = []
        with MyDB:
            cursor = ProjectAppendedEmployeeRoleDoc.find(searchDoc)
            if iterable(cursor):
                for obj in cursor:
                    roles.append(obj)
                    if iterable(obj):
                        if str(ProjectAppendedEmployeeRoleDoc.employeeId) in obj:
                            ids.append(obj[str(ProjectAppendedEmployeeRoleDoc.employeeId)])

        # l(roles, 'roles3849756')
        return ids, roles


    def getEmployeeIdsOnRealProject_(self, userId, project_id):
        l = MyLog().l()
        p = MyLog().p()
        findedListOfEmployes = None
        ids = []

        # FIXME: Everywhere check length of string which is used as ObjectId(): MUST HAVE length == len('541a89374f452d177481b671')

        if isValidObjectId(project_id):

            searchDoc =\
            {
                ProjectAppendedEmployeeRoleDoc.projectId: ObjectId(project_id)
            }
            l(searchDoc, 'getEmployeeIdsOnRealProject():: searchDoc')


            with MyDB:
                cursor = ProjectAppendedEmployeeRoleDoc.find(searchDoc)

                if isinstance(cursor, collections.Iterable):
                    for x in cursor:
                        if isinstance(x, collections.Iterable):
                            if 'employeeId' in x:
                                ids.append(x['employeeId'])


            # l(cursor, 'getEmployeeIdsOnRealProject():: findedListOfEmployes()')
        return ids


    def getEmployeeIdsOnEmptyProject(self, appenderId):
        l = MyLog().l()
        p = MyLog().p()
        findedListOfEmployes = None
        with MyDB:
            findedListOfEmployes = ProjectAppendedEmployeeRoleDoc.find(
                    {
                        ProjectAppendedEmployeeRoleDoc.appenderId: appenderId,
                        ProjectAppendedEmployeeRoleDoc.projectId: { '$exists': False }
                    }
            )
        return findedListOfEmployes


    def bindEmployeeToProject(self, appenderId, projectId):
        result = None
        with MyDB:
            result = ProjectAppendedEmployeeRoleDoc.update(
                {
                    ProjectAppendedEmployeeRoleDoc.appenderId: appenderId,
                    ProjectAppendedEmployeeRoleDoc.projectId: { '$exists': False }
                },
                {
                    '$set':
                         {
                            ProjectAppendedEmployeeRoleDoc.projectId: projectId,
                            ProjectAppendedEmployeeRoleDoc.removed_from_project_: False
                         }
                },
                upsert = False,
                multi = True
            )
        return result

    def removeEmployeeFromEmptyProject(self, appenderId, employeeId):
        result = None
        l = MyLog().l()

        removeDoc = {  ProjectAppendedEmployeeRoleDoc.appenderId: int(appenderId),
                       ProjectAppendedEmployeeRoleDoc.employeeId: int(employeeId),
                       ProjectAppendedEmployeeRoleDoc.projectId: { '$exists': False }
                    }
        l(removeDoc, 'removeDoc')


        with MyDB:
            result = ProjectAppendedEmployeeRoleDoc.remove(removeDoc)


        l(result, 'removeEmployeeFromEmptyProject()::result')
        return result


    def updateEmployeeWorkPeriodOnProject(self, **opt):

        p = MyLog().p()
        l = MyLog().l()

        projectRoleId = opt['projectRoleId']
        startDayOnProject = opt['startDayOnProject']
        finishDayOnProject = opt['finishDayOnProject']


        l(finishDayOnProject, 'finishDayOnProject')


        compareResult = MyDate().compare(startDayOnProject, finishDayOnProject, '/')
        #  and (compareResult == 1 or compareResult == False)

        obj = None

        startDateCorrect = MyDate().isValidDate(startDayOnProject)


        updateResult = None
        if startDateCorrect == True \
            and ( compareResult == 1 or finishDayOnProject == '' ):

            with MyDB:

                criteriaDoc = {
                    '_id': ObjectId(projectRoleId),
                }
                l(criteriaDoc, 'criteriaDoc')

                setDoc = {
                             ProjectAppendedEmployeeRoleDoc.startDayOnProject: startDayOnProject,
                             ProjectAppendedEmployeeRoleDoc.finishDayOnProject: finishDayOnProject,
                         }
                l(setDoc, 'setDoc')

                updateResult = ProjectAppendedEmployeeRoleDoc.update( criteriaDoc, {'$set': setDoc } )

                l(updateResult, 'updateResult')

        return updateResult



    def updateEmployeeRoleOnProject(
            self,
            appenderId,
            employeeId,
            roleOnProject,
            startDayOnProject,
            finishDayOnProject
    ):
        p = MyLog().p()
        l = MyLog().l()

        obj = None
        updateResult = None

        if type(appenderId) == int and type(employeeId) == int:
            criteriaDoc = {
                ProjectAppendedEmployeeRoleDoc.appenderId: appenderId,
                ProjectAppendedEmployeeRoleDoc.employeeId: employeeId,
                ProjectAppendedEmployeeRoleDoc.projectId: { '$exists': False }
            }
            setDoc = {
                         ProjectAppendedEmployeeRoleDoc.roleOnProject: roleOnProject,
                         ProjectAppendedEmployeeRoleDoc.startDayOnProject: startDayOnProject,
                         ProjectAppendedEmployeeRoleDoc.finishDayOnProject: finishDayOnProject,
                     }

            with MyDB:
                updateResult = ProjectAppendedEmployeeRoleDoc.update( criteriaDoc, {'$set': setDoc } )

            if updateResult['updatedExisting'] == False:
                insertResult = ProjectAppendedEmployeeRoleDoc()\
                    .appendUserOnEmptyProject(
                        appenderId,
                        employeeId,
                        roleOnProject,
                        startDayOnProject,
                        finishDayOnProject
                )

            # l(insertResult, 'insertResult')
            with MyDB:
                _ = ProjectAppendedEmployeeRoleDoc.find( criteriaDoc )
                for x in _:
                    obj = x
                    # break
        # else:
        #     raise Exception({
        #         'CLASS': self.__class__.__name__,
        #         'message': 'appenderId or employeeId is not \'int\' type'
        #     })

        return obj


# - Что вы можете сказать о Питоне?
# - Он опять упал... (rofl)


    def updateEmployeeRoleOnRealProject (
            self,
            appenderId,
            projectId,
            employeeId,
            roleOnProject,
            startDayOnProject,
            finishDayOnProject
    ):
        p = MyLog().p()
        l = MyLog().l()

        obj = None
        updateResult = None

        l(projectId, 'projectId')
        l(type(employeeId), 'type(employeeId)')


        l(roleOnProject, '1: roleOnProject')
        roleOnProject = roleOnProject.encode('utf-8')
        l(roleOnProject, '2: roleOnProject')



        roleOnProject = str(roleOnProject)
        l(roleOnProject, '3: roleOnProject')



        if projectId != None and type(employeeId) == int:
            criteriaDoc =   {
                                ProjectAppendedEmployeeRoleDoc.appenderId: appenderId,
                                ProjectAppendedEmployeeRoleDoc.projectId: ObjectId(projectId),
                                ProjectAppendedEmployeeRoleDoc.employeeId: employeeId,
                            }
            setDoc = {
                         ProjectAppendedEmployeeRoleDoc.roleOnProject: roleOnProject,
                         ProjectAppendedEmployeeRoleDoc.startDayOnProject: startDayOnProject,
                         ProjectAppendedEmployeeRoleDoc.finishDayOnProject: finishDayOnProject,
                     }

            l(criteriaDoc, 'criteriaDoc')
            l(setDoc, 'setDoc')

            with MyDB:
                updateResult = ProjectAppendedEmployeeRoleDoc.update( criteriaDoc, {'$set': setDoc } )
                l(updateResult, 'updateResult')




            if updateResult['updatedExisting'] == False:
                insertResult = self\
                    .appendUserOnRealProject(
                        appenderId,
                        projectId,
                        employeeId,
                        roleOnProject,
                        startDayOnProject,
                        finishDayOnProject
                )
                l(insertResult, 'insertResult')




            with MyDB:
                cursor = ProjectAppendedEmployeeRoleDoc.find( criteriaDoc )
                # l(cursor, 'cursor')
                for x in cursor:
                    obj = x
                    # l(obj, 'obj')
                    # break
        # else:
        #     raise Exception({
        #         'CLASS': self.__class__.__name__,
        #         'message': 'appenderId or employeeId is not \'int\' type'
        #     })

        return obj

    def getAllUsersAppendedOnEmptyProject(self, appenderId):
        l = MyLog().l()
        _ = None
        with MyDB:
            __ = ProjectAppendedEmployeeRoleDoc.find(
                {
                    ProjectAppendedEmployeeRoleDoc.appenderId: appenderId,
                    ProjectAppendedEmployeeRoleDoc.projectId:{'$exists':False}
                }
            )
            employeesRolesOnProject = [_ for _ in __]

        # l(employeesRolesOnProject, 'call:: getAllUsersAppendedOnEmptyProject() employeesRolesOnProject  <<<<-----')
        return employeesRolesOnProject


    def appendUserOnEmptyProject(
            self,
            appenderId,
            employeeId,
            roleOnProject,
            startDayOnProject,
            finishDayOnProject
    ):
        l = MyLog().l()


        appenderId = int(appenderId)
        employeeId = int(employeeId)


        result = None
        doc = {
            ProjectAppendedEmployeeRoleDoc.appenderId : appenderId,
            ProjectAppendedEmployeeRoleDoc.employeeId: employeeId,
            ProjectAppendedEmployeeRoleDoc.roleOnProject: roleOnProject,

            ProjectAppendedEmployeeRoleDoc.startDayOnProject: startDayOnProject,
            ProjectAppendedEmployeeRoleDoc.finishDayOnProject: finishDayOnProject,
        }


        with MyDB:
            removeResult = ProjectAppendedEmployeeRoleDoc.remove({
                    ProjectAppendedEmployeeRoleDoc.appenderId: appenderId,
                    ProjectAppendedEmployeeRoleDoc.employeeId: employeeId,
                    ProjectAppendedEmployeeRoleDoc.projectId: { '$exists': False }}
            )

            l(removeResult, 'removeResult')

            result = ProjectAppendedEmployeeRoleDoc.insert(doc)
            l(result, 'result INSERT ')

            if type(result) != ObjectId:
                result = None
            else:
                result = str(result)

        return result

    def getAllUsersAppendedOnProjects(self):
        l = MyLog().l()
        employeesRolesOnProjects = []
        with MyDB:
            cursor = ProjectAppendedEmployeeRoleDoc.find(
                {
                    ProjectAppendedEmployeeRoleDoc.projectId:
                        {
                            '$exists':True
                        }
                }
            )
            if iterable(cursor):
                employeesRolesOnProjects = [ obj for obj in cursor]
        return employeesRolesOnProjects

###########################################################################################################


# class ProjectAppendedEmployeeRoleDoc(Document):
#
#     config_collection = 'project_appended_employee_role'
#     config_database = 'tt'
#
#     appenderId = 'appenderId'
#     employeeId = 'employeeId'
#     roleOnProject = 'roleOnProject'
#
#     startDayOnProject = 'startDayOnProject'
#     finishDayOnProject = 'finishDayOnProject'
#
#     projectId = 'projectId'  # !ATTENTION! Set only for already created projects
#     # Cause when this key is absent the project's employee are set to unexisting/hav been creating project










