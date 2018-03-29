# -*- coding: utf-8 -*-

__author__ = 'DMitriy Morozov'
# from datetime import *
import datetime


from ..doctordog import *
from timecard.app_classes.MyLog import MyLog


class MyDate:

    def blablabla(self):
        day = None
        return day


    def isValidDate(self, dd_mm_yyyyy):
        l = MyLog().l()
        response = False
        d_, m_, y_ = self.validateDate(dd_mm_yyyyy)

        l(d_, 'd_')
        # l([d_, m_, y_], '[d_, m_, y_]')

        if d_ != None and m_ != None and y_ != None:

            if isinstance(d_, unicode) and isinstance(m_, unicode) and isinstance(y_, unicode):
                d_ = int(d_)
                m_ = int(m_)
                y_ = int(y_)
                if d_ > 0 and d_ < 32 and m_ > 0 and m_ < 13 and y_ > 0 and y_ < 9999:
                    response = True

        return response





    def validateDate(self, dd_mm_yyyyy, splitter = '/'):
        l = MyLog().l()
        day = None
        month = None
        year = None
        # l(dd_mm_yyyyy, '-->>>dd_mm_yyyyy')
        if type(splitter) == str:
            lst = dd_mm_yyyyy.split('/')
            # l(lst, '!!lst')
            if len(lst) == 3:
                year = lst.pop()
                month = lst.pop()
                day = lst.pop()



        # l(day, '!!day')
        # l(month, '!!month')
        # l(year, '!!year')
        return day, month, year


    def compare(self, aDateStr, bDateStr, splitter = '/'):
        l = MyLog().l()
        result = False
        # l(aDateStr, '-->> aDateStr')
        # l(bDateStr, '-->> bDateStr')
        aDay, aMonth, aYear = self.validateDate(aDateStr, splitter)
        bDay, bMonth, bYear = self.validateDate(bDateStr, splitter)

        if aDay != None and aMonth != None and aYear != None and bDay != None and bMonth != None and bYear != None:

            # l(aYear, 'aYear')
            # l(aMonth, 'aMonth')
            # l(aDay, 'aDay')
            #
            # l(bYear, 'bYear')
            # l(bMonth, 'bMonth')
            # l(bDay, 'bDay')

            # aDate = datetime.strptime(str(aYear) + str(aMonth) + str(aDay), "%Y%m%d")
            # bDate = datetime.strptime(str(bYear) + str(bMonth) + str(bDay), "%Y%m%d")

            aDate = None
            bDate = None

            _aStr = str(aYear) + str(aMonth) + str(aDay)
            _bStr = str(bYear) + str(bMonth) + str(bDay)

            # l(_aStr, '_aStr')
            # l(_bStr, '_bStr')

            aDate = datetime.datetime.strptime(_aStr, "%Y%m%d")
            bDate = datetime.datetime.strptime(_bStr, "%Y%m%d")


            # l(aDate, 'aDate')
            # l(bDate, 'bDate')
            if aDate.date() < bDate.date():
                result = 1
            else:
                if aDate.date() == bDate.date():
                    result = 0
                else:
                    result = -1
        return result





