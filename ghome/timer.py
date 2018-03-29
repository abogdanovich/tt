#!/usr/bin/python
# -*- coding: utf-8 -*-
# timer.py

"""
    Модуль timer.py
    Классы:
        Timer:
            Реализация класса для вызова действий по таймеру.
"""

__author__    = 'unregistered <black@tmnhy.su>'
__version__   = '$Revision: 0.0.1 $'
__date__      = '$Date: 2011/05/15 $'
__copyright__ = ''
__license__   = 'GPLv2'

import threading

class Timer(threading.Thread):
    """
        Реализует следующую схему работы таймера:
        в отдельном потоке вызывает заданную функции с заданным инетрвалом.

        Name: Timer

        Атрибуты:
            interval - время срабатывания таймера в секундах,
            func     - функция задаёт действие по таймеру,
            param    - параметры функции func.

        Методы:
            start() - запустить таймер,
            stop()  - остановить таймер,
            set_timer() - установить таймер.

        Использование:
            from time import gmtime, strftime, sleep
            from processtimer import TimerThread

            def print_time():
                print strftime('%a, %d %b %Y %H:%M:%S', gmtime())

            timer = TimerThread(5, print_time, '')
            timer.start()
            print 'Ждём 60 секунд и останавливаем таймер'
            sleep(60)
            timer.stop()


        @author unregistered <black@tmnhy.su>
        @version 0.0.1
        @date 2011/05/15
    """

    def __init__(self, interval, func, param):
        """
            Проинициализировать атрибуты класса.
            @param int interval : значение таймера в секундах
            @param func
            @param param
            @return : None
        """
        threading.Thread.__init__(self)
        self._finished = threading.Event()
        self.func      = func
        self.param     = param
        self.set_timer(interval)

    def set_timer(self, interval):
        """
            Установить таймер.
            @param int interval
            @return : None
        """
        self.interval = interval

    def stop(self):
        """
            Остановить таймер.
            @return : None
        """
        self._finished.set()

    def run(self):
        """
            Запускает поток.
            @return : None
        """
        while 1:
            if self._finished.isSet():
                return
            self.processing()
            self._finished.wait(self.interval)

    def processing(self):
        """
            Выполняет необходимое действие.
            @return : None
        """
        apply(self.func, self.param)

if __name__ == '__main__':
    print __doc__
    print Timer.__doc__