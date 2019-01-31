#!/usr/bin/env python
 
import os
import time
import datetime
import glob
import MySQLdb
import gps
from time import strftime
from Adafruit_BME280 import *

# Setup Sensor value 
sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)
 
# Listen on port 2947 (gpsd) of localhost
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

#Variables for MySQL
db = MySQLdb.connect(host="localhost", user="username", passwd="password", db="sensor") # replace password with your password
cur = db.cursor()

 
#------------TIME----------------
hours = str(time.localtime()[3])
mins = str(time.localtime()[4])
secs = str(time.localtime()[5])
days = str(time.localtime()[2])
months = str(time.localtime()[1])
years = str(time.localtime()[0])

if len(hours) == 1:
        hours = '0'+hours
if len(mins) == 1:
        mins = '0'+mins
if len(secs) == 1:
        secs = '0'+secs
if len(days) == 1:
        days = '0'+days
if len(months) == 1:
        months = '0'+months

HMS = hours+':'+mins+':'+secs
DMY = days+'/'+months+'/'+years
times = DMY+' '+HMS

#-----------BMP280---------------

def tempRead(): #read temperature, return float with 3 decimal places
        degrees = float('{0:.3f}'.format(sensor.read_temperature()))
        return degrees
 
def pressRead(): #read pressure, return float with 3 decimal places
        pascals = float('{0:.3f}'.format(sensor.read_pressure()/100))
        return pascals
 
def humidityRead(): #read humidity, return float with 3 decimal places
        humidity = float('{0:.3f}'.format(sensor.read_humidity()))
        return humidity

temperature = tempRead()
pressure = pressRead()
humidity = humidityRead() 

# ------GPS--------------
a = 1
while a == 1:
	report = session.next()
	if report['class'] == 'TPV':
  		if hasattr(report, 'lat') and hasattr(report, 'lon') and hasattr(report, 'alt'):
                	latitude = report.lat
			lontitude = report.lon
			altitude = report.alt
			a = 2

sql = ("""INSERT INTO bmesensor (datetime,temperature,pressure,humidity,latitude,lontitude,altitude) VALUES (%s,%s,%s,%s,%s,%s,%s)""", (times, temperature, pressure, humidity,latitude, lontitude, altitude))
 
try:
    print "Writing to the database..."
    cur.execute(*sql)
    db.commit()
    print "Write complete"
 
except:
    db.rollback()
    print "We have a problem"
 
cur.close()
db.close()

print times
print temperature
print pressure
print humidity
print latitude
print lontitude
print altitude
