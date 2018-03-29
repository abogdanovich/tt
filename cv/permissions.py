# -*- coding: utf-8 -*-
__author__ = 'ABKorotky'
__email__ = ['akorotky@minsk.ximxim.com', 'aleksandr.korotky@ximad.com']


from django.forms import Form
from django.forms import BooleanField
from django.forms.forms import DeclarativeFieldsMetaclass


PERMISSIONS = (
    "View premissions",                             # 0 !!! PERMISSIONS !!! 0-1 flags
    "Edit Permissions",                             # 1
    "View Customer data",                           # 2 Customer permissions 2-9 flags
    "Manage Customer data",                         # 3
    "",                                             # 4
    "",                                             # 5
    "",                                             # 6
    "",                                             # 7
    "",                                             # 8
    "",                                             # 9
    "View Project data",                            # 10 Project permissions 10-24 flags
    "View Project Customer data",                   # 11
    "Create/Delete new empty Project",              # 12
    "Create/Delete new Project from Preset",        # 13
    "Make copy of Project",                         # 14
    "Edit Project data",                            # 15
    "Manage Project Requirements",                  # 16
    "Manage Project ScreenShots",                   # 17
    "Add/Delete Employee to Project Work Group",    # 18
    "Edit Employee data in Project Work Group",     # 19
    "",                                             # 20
    "",                                             # 21
    "",                                             # 22
    "",                                             # 23
    "",                                             # 24
    "View Preset data",                             # 25 Presets permissions 25-29 flags
    "Manage Preset data",                           # 26
    "",                                             # 27
    "",                                             # 28
    "",                                             # 29
    "View Skill/Requirement data",                  # 30 Skills/Requirements permissions 30-34 flags
    "Manage Skill/Requirement data",                # 31
    "",                                             # 32
    "",                                             # 33
    "",                                             # 34
    "View Position data",                           # 35 Positions permissions 35-39 flags
    "Manage Position data",                         # 36
    "",                                             # 37
    "",                                             # 38
    "",                                             # 39
    "View CV data",                                 # 40 Curriculum Vitae, CV 40 - 55 flags
    "Edit CV Personal data",                        # 41
    "Manage CV Foreign Language data",              # 42
    "Manage Technical Skill data",                  # 43
    "Manage Certificate data",                      # 44
    "Edit Project data",                            # 45
    "Manage Previous Project data",                 # 46
    "View CV Service data",                         # 47
    "Edit CV Service data",                         # 48
    "Create new CV",                                # 49
    "Delete CV",                                    # 50
    "",                                             # 51
    "",                                             # 52
    "",                                             # 53
    "",                                             # 54
    "",                                             # 55
)


class PermissionMetaclass(DeclarativeFieldsMetaclass):

    def __new__(cls, name, bases, attrs):
        i = 0
        for perm in PERMISSIONS:
            if perm:
                attrs["p%u" % i] = BooleanField(label=perm, required=False)
            i += 1
        new_class = super(PermissionMetaclass, cls).__new__(cls, name, bases, attrs)
        return new_class


class PermissionForm(Form):
    __metaclass__ = PermissionMetaclass