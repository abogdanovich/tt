# -*- coding: utf-8 -*-

__author__ = 'DMitriy Morozov'

import logging

class MyLog:

    def empty(self):
        def func(a, b):
            pass
        return func

    def p(self):
        def func(obj, objStr = ''):
            # print 'type(objStr) [ ', type(objStr), ' ] '
            if type(objStr) == str:
                print objStr
            else:
                print '[...]'
            print type(obj)
            print '['
            print obj
            print ']'
        return func

    def l(self):
        func = None
        l_ = MyLog().get()

        def func(obj, objStr = ''):
            l_(objStr)

            if type(objStr) == str:
                l_(objStr)
            else:
                l_('[...]')


            l_(type(obj))
            l_('[')
            l_(obj)
            l_(']')
        return func


    def get(self, filename = 'log.txt'):
        lgr = None
        if(type(filename) != 'string'):
            filename = 'log.txt'
        lgr = logging.getLogger('TimeTracker')
        lgr.setLevel(logging.DEBUG)
        fh = logging.FileHandler(filename)
        fh.setLevel(logging.DEBUG)
        frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(frmt)
        lgr.addHandler(fh)
        return lgr.critical


