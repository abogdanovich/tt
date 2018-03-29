#!/usr/bin/env python
# -*- coding: utf-8 -*-
# tictac.py

from time import sleep
from datetime import datetime
from timer import Timer
import sys
import ow


def print_time():
	print datetime.now().strftime('%H:%M:%S')

def init_sensors():
	ow.init('localhost:4444')	
	return ow.Sensor("/").sensorList()

def get_temp(sensors):
	for sensor in sensors[:]:
		print "sensor: %s -> %s C" % (sensor.address, sensor.temperature)
	

if __name__ == '__main__':
	print 'OW init'
	slist = init_sensors()
	print ""
	print slist
	print "Start timer to ask sensors each 10 secs during 1 minute...."
	print ""

	#timer = Timer(10, get_temp(slist), '')
	timer = Timer(10, print_time, '')
	timer.start()
	sleep(60)
	timer.stop()


#s1 = ow.Sensor('/10.4AEC29CDBAAB')
#s2 = ow.Sensor('/3A.67C6697351FF')

#for sensor in sensors[:]:
#    print "sensor: %s -> %s C" % (sensor.address, sensor.temperature)

"""

print "------switcher sensor:-------"
print "PIO.A %s" % s2.PIO_A
print "PIO.B %s" % s2.PIO_B
print ">>> change PIO A"

ow.owfs_put(s2.PIO_A, '1')
ow.owfs_put(s2.PIO_B, '1')
print s2.PIO_A
print s2.PIO_B
print "---------------------------"
"""
