#!/usr/bin/python


import rrdtool

print "create db..."
ret = rrdtool.create("active_users.rrd", "--step", "60",
        "DS:minsk_u:GAUGE:600:U:U",
        "DS:gomel_u:GAUGE:600:U:U",
        "DS:ulianovsk_u:GAUGE:600:U:U",
        "RRA:LAST:0.5:1:576")


