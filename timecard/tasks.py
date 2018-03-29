# Django celery tasks
# -*- coding: utf-8 -*-
from celery.task import periodic_task
from celery.schedules import crontab
import sys
sys.path.append("C:/Python27/Lib/site-packages/PyRRD-0.1.0/")
sys.path.append("C:/Python27/Lib/site-packages/rrdtool-1.4.8/")
import rrdtool
from rrdtool import update as rrd_update
import os
import ow


@periodic_task(run_every=crontab(hour="*", minute="*/1", day_of_week="*"))
def get_temperature():
    path = os.path.realpath(os.path.dirname(__file__))
    dbname = "database.rrd"
    image = "image.png"
    fullpath = "%s/%s" % (path, dbname)
    fullimage = "%s/%s" % (path, image)
        
    if os.path.isfile(fullpath):

	ow.init('localhost:4444')
	sensors = ow.Sensor("/").sensorList()
	metric1 = sensors[0].temperature
	metric2 = sensors[1].temperature
	metric3 = sensors[2].temperature
	    
	ret = rrd_update(fullpath, 'N:%s:%s:%s' % (metric1, metric2, metric3))
	
	ret = rrdtool.graph(fullimage, "--start", "0", "--vertical-label=Temperature",
	     "-w 500",
	     "DEF:t1=/home/nc/tt/timecard/database.rrd:metric1:LAST",
	     "DEF:t2=/home/nc/tt/timecard/database.rrd:metric2:LAST",
	     "DEF:t3=/home/nc/tt/timecard/database.rrd:metric3:LAST",
	     "LINE2:t1#006633:metric 1\\r",
	     "GPRINT:t1:LAST:Average temperature\: %1.0lf ",
	     "COMMENT:\\n",
	     "LINE2:t2#0000FF:metric 2\\r",
	     "GPRINT:t2:LAST:Average temperature\: %1.0lf ",
	     "COMMENT:\\n",
	     "LINE2:t3#0073E6:metric 3\\r",
	     "GPRINT:t3:LAST:Average temperature\: %1.0lf",
	     "COMMENT:\\n")
	     	     
    else:
	
	ret = rrdtool.create(fullpath, "--step", "300",
	    "DS:metric1:GAUGE:600:U:U",
	    "DS:metric2:GAUGE:600:U:U",
	    "DS:metric3:GAUGE:600:U:U",
	    "RRA:LAST:0.5:1:576")

    