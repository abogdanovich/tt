#/usr/bin/env python
"""
OWFS test program
See owfs.sourceforge.net for details
{copyright} 2005 Peter Kropf
GPL license
"""

import sys
import ow
import time

"""
temperature sensor 10.4AEC29CDBAAB
switcher sensor 3A.67C6697351FF

"""

ow.init('localhost:3000')
sensors = ow.Sensor("/").sensorList()


#s1 = ow.Sensor('/10.4AEC29CDBAAB')
#s2 = ow.Sensor('/3A.67C6697351FF')

for sensor in sensors[:]:
    print "%s >>> %s" % (sensor.type,sensor.address)



"""
print "-------temperature sensor:----------"
print "%s - %s C" % (s1.type, s1.temperature)
print "----------------"

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
