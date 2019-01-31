from Adafruit_BME280 import *

sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)

degrees = sensor.read_temperature()
pascals = sensor.read_pressure()
hectopascals = pascals / 100
humidity = sensor.read_humidity()

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

print('Date on the BMP280 is : '+times)
print 'Temp      = {0:0.3f} deg C'.format(degrees)
print 'Pressure  = {0:0.2f} hPa'.format(hectopascals)
print 'Humidity  = {0:0.2f} %'.format(humidity)
