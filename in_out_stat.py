    #!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb

import rrdtool

# Open database connection
# db = MySQLdb.connect("mysql.dmz", "tt", "zD5FNdTeJyrGxxaP", "tt")
db = MySQLdb.connect("localhost", "root", "panda2014", "timetracker")
# prepare a cursor object using cursor() method
cursor = db.cursor()

# we have to extract the names of offices
cursor2 = db.cursor()
cursor2.execute("SELECT short_name, full_name FROM timecard_offices")

users = []
offices = []#not used currently
for row in cursor2:
    # execute SQL query using execute() method.
    cursor.execute("SELECT * FROM timecard_user WHERE status=1 AND office='%s'" % row[0])
    if cursor.rowcount:
        users.append(cursor.rowcount)
    else: #if we have not found anything and mysql return NULL
        users.append(0)
    offices.append(row[0])#not used currently

# disconnect from server
db.close()
# OK. Now we have to pass the current users quantity to the rrd database
args = ''
limit = len(users) - 1
counter = 0
while True:
    if counter < limit:
        args += str(users[counter]) + ':'
        counter += 1
    else:
        args += str(users[counter])
        break
ret = rrdtool.update('active_users.rrd','N:'+args)
# currently we pass the harcoded style into the rrdtool because not everything can be taken from DB :(
ret = rrdtool.graph("static/css/images/active_users.png", "--vertical-label=active users/s",
                    "--width","616", "--height","251","--full-size-mode",
                    "DEF:minsk_u=active_users.rrd:minsk_u:LAST",
                    "DEF:gomel_u=active_users.rrd:gomel_u:LAST",
                    "DEF:ulianovsk_u=active_users.rrd:ulianovsk_u:LAST",
                    "LINE1:minsk_u#FF4747:Minsk active users    ",
                    "GPRINT:minsk_u:LAST:\: %1.0lf",
                    "COMMENT:\\n",
                    "LINE1:gomel_u#006633:Gomel active users    ",
                    "GPRINT:gomel_u:LAST:\: %1.0lf",
                    "COMMENT:\\n",
                    "LINE1:ulianovsk_u#FF6600:Ulianovsk active users",
                    "GPRINT:ulianovsk_u:LAST:\: %1.0lf",
                    "COMMENT:\\n")
