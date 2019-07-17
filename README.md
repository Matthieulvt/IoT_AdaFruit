# IoT Adafruit

IoT setup on a Raspberry PI 3 with Adafruit Sensors (Ultimate GPS Breakout v3 + BMP280/BME280). [ESILV PROJECT]

![Alt text](/Screenshots/Fritzing.png?raw=true "Fritzing schema")

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

For this project you will need :

* A raspberry PI 3 B (or B+).
* Adafruit Sensor : BMP280 or BME280. Thoses are for Temp, Pressure and Humidity.
* Adafruit Sensor : Ultimate GPS Breakout V3.

### Setting up

Thoses dependencies are going to be usefull on your raspberry (Assuming you have Raspbian installed on it):

Raspbian-Config
```
Camera: Enabled
SSH: Enabled
VNC: Disabled
SPI: Enabled
I2C: Enabled
Serial: Enabled
1-Wire: Disabled
Remote GPIO: Enabled
```

## Connect Sensors

![Alt text](/Screenshots/Fritzing_zoom.png?raw=true "Fritzing schema zoom")

## BMP280 / BME280

### Connection (UART)

Either you get BMP or BME sensor the connections are the same:
```
BMP280---------Raspberry Pi
VIN------------Pin 1 (3.3V) (red wire)
Ground---------Pin 6        (black wire)
SCK------------Pin 5 (SCL1) (white wire)
SDI------------Pin 3 (SDA1) (cyan wire)
```

Test the sensor, you should see 77 on row 7, lines 70:
```
sudo i2cdetect -y 1
```
![Alt text](/Screenshots/i2cdetect.png?raw=true "i2cdetect")

### Libraries

Either you can use BMP280 or BME280, we are going to use libraries for BME280. This sensor got temp, pressure and humidity meanwhile BMP280 only got temp and pressure. Humidity will remain at 0 if you use this one.

Assuming you got python dependencies, load thoses libraries

For Debian based Linux:
```
sudo apt-get update
sudo apt-get install build-essential python-pip python-dev python-smbus git
git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
cd Adafruit_Python_GPIO
sudo python setup.py install
```

For MacOs (assuming you got pip installed)
```
git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
cd Adafruit_Python_GPIO
sudo python setup.py install
```

For Windows (assuming you got pip installed
```
git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
cd Adafruit_Python_GPIO
python setup.py install
```

Once it's done, move forward to the folder that was just created :
```
sudo python setup.py install
git clone https://github.com/adafruit/Adafruit_Python_BME280.git
```

Everything is loaded now, you can test the script BME280.py :
```
python ./Scripts/BME280.py
```
![Alt text](/Screenshots/bme280py.png?raw=true "BME280 script")

## Ultimate GPS Breakout V3 Adafruit

"We designed the Ultimate GPS with a built-in regulator, so even if it's powered with 5V, the signal levels are still 3.3V - safe for your Pi!", Adafruit

You should use 3.3V pins instead of 5V in order to keep your Pi safe.

### Connection (UART)

Connect your gps following thoses instructions:
```
GPS Vin-----------3.3V (red wire)
GPS Ground--------Ground (black wire)
GPS RX------------TX (orange wire)
GPS TX------------RX (green wire)
```

### Librarires

Install gpsd
```
sudo apt-get install gpsd gpsd-clients
```
We need to disable gpsd and restart it linked on the serial port (uart)
```
sudo killall gpsd
sudo gpsd /dev/serial0 -F /var/run/gpsd.sock
```

And you can test it:
```
python3 ./Scripts/gpstest.py
```
![Alt text](/Screenshots/gpsdtest.png?raw=true "GPS test")

## Create MYSQL Database for the sensor

Now if you want to send your data into a mysql database follow thoses instructions:

### Prerequitises

* Mysql-server and Python-mysqldb installed

### Setup

Go in the mysql shell
```
mysql -u root -p
Enter password:
mysql> 
```
Make a database called sensor and then use it
```
CREATE DATABASE sensor;
USE sensor;
```
In this database we will create a tablle called bmesensor. We will there send all data collected from both BME280 sensor and GPS sensor.
```
CREATE TABLE bmesensor(datetime VARCHAR(25) NOT NULL, temperature FLOAT (6,3) NOT NULL, pressure FLOAT (8,3) NOT NULL, humidity FLOAT (6,3) NOT NULL, latitude FLOAT (6,3) NOT NULL, lontitude FLOAT (6,3) NOT NULL, altitude FLOAT (6,3) NOT NULL);
```
To leave Mysql Shell hit `Ctrl+Z`

### Send data

That make us moving to our last script : sensor.py. Pay attention to the connect section to Mysql:
![Alt text](/Screenshots/mysql_section.png?raw=true "GPS test")

You need to change the actual `username` and `password` by yours.

Once it's done you are now ready to use the `sensor.py` script:
```
./Scripts/sensor.py
```
![Alt text](/Screenshots/sensorpy.png?raw=true "GPS test")

You can then go back in your MysqlShell to check the data.
```
mysql -u root -p
Enter password:
mysql> 
```
```
USE sensor;
SELECT * FROM bmesensor;
```

## Authors

This project was made for a BLOCKCHAIN + IOT project from this team :
* **Matthieu LANVERT**
* **Dean CHERIF**
* **Alexandre LEVRET**
* **Lucile JEANNERET**
