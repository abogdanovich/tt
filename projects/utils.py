# -*- coding: utf-8 -*-
__author__ = 'ABKorotky'
__email__ = ['akorotky@minsk.ximxim.com', 'aleksandr.korotky@ximad.com']


class ProjectRequirementDict(object):
    def __init__(self, source={}):
        self.source = {}
        for req, tags in source.items():
            self.source[req] = {}
            for tag in tags:
                self.source[req][tag] = 0

    def add_cv_skills(self, needed={}):
        for req, tags in needed.items():
            for tag in tags:
                self.source[req][tag] += 1