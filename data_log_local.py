#!/usr/bin/python
# -*- coding: utf-8 -*-

########################################################################
##					  {Local Data Logging Script}			  	      ##
########################################################################
"""

Description: Receives data from all system sensors and return formatted
			 values for display and logging. Send data to relative
			 destinations such as local CSV files, SQL databases, and
			 IoT platforms."
"""
########################################################################

__author__ = "Aleks Zawadzki"
__copyright__ = "Open-Source, Undersea Laboratory 2021"
__credits__ = ""

__version__ = "1.1.0"
__maintainer__ = "Aleks Zawadzki"
__email__ = "undersealaboratory@gmail.com"
__status__ = "Production"

# import libraries
import math
import time

from time import *
from time import sleep, perf_counter

import ds18b20
import dht22

# maintains 3 sig figs
def dataFormat(data):
	if data > 100 or data < -100:
		data = (f"{data:.0f}")
		
	elif data > 10 or data < -10:
		data = (f"{data:.1f}")
		
	else:
		data = (f"{data:.2f}")
	
	return data

# DS18B20 External Sensor
def writeDs18b20():
	temp_c, temp_f = ds18b20.getTemp()	# retreive data
	
	# format data
	temp_c = dataFormat(temp_c)
	temp_f = dataFormat(temp_f)
	
	# write data to .txt files
	if ds18b20.read_status == 1:
		with open("/mnt/usb/Sensor Data/DS18B20/ds18b20_temp_c.txt", "w") as txt:
			txt.write(str(temp_c) + '°C')
			
		with open("/mnt/usb/Sensor Data/DS18B20/ds18b20_temp_f.txt", "w") as txt:
			txt.write(str(temp_f) + '°F')
		
		# write data to .csv files
		with open("/mnt/usb/Sensor Data/DS18B20/ds18b20_temp_c_log.csv", "a") as log:
			log.write("{0},{1},{2}\n".format(strftime("%Y-%m-%d"), strftime("%H:%M:%S"),str(temp_c)))
			
		with open("/mnt/usb/Sensor Data/DS18B20/ds18b20_temp_f_log.csv", "a") as log:
			log.write("{0},{1},{2}\n".format(strftime("%Y-%m-%d"), strftime("%H:%M:%S"),str(temp_f)))
			
		#print("DS18B20: " + str(temp_c))
		
# DHT22 Internal Sensor
def writeDht22():
	temp_c, temp_f, hum = dht22.getTempHum()	# retreive data
	
	# format data
	temp_c = dataFormat(temp_c)
	temp_f = dataFormat(temp_f)
	hum = dataFormat(hum)
	
	# write data to .txt files
	with open("/mnt/usb/Sensor Data/DHT22/dht22_temp_c.txt", "w") as txt:
		txt.write(str(temp_c) + '°C')

	with open("/mnt/usb/Sensor Data/DHT22/dht22_temp_f.txt", "w") as txt:
		txt.write(str(temp_f) + '°F')
		
	with open("/mnt/usb/Sensor Data/DHT22/dht22_hum.txt", "w") as txt:
		txt.write(str(hum) + '%')
		
	# write data to .csv files
	with open("/mnt/usb/Sensor Data/DHT22/dht22_temp_c_log.csv", "a") as log:
		log.write("{0},{1},{2}\n".format(strftime("%Y-%m-%d"), strftime("%H:%M:%S"),str(temp_c)))
		
	with open("/mnt/usb/Sensor Data/DHT22/dht22_temp_f_log.csv", "a") as log:
		log.write("{0},{1},{2}\n".format(strftime("%Y-%m-%d"), strftime("%H:%M:%S"),str(temp_f)))
		
	with open("/mnt/usb/Sensor Data/DHT22/dht22_hum_log.csv", "a") as log:
		log.write("{0},{1},{2}\n".format(strftime("%Y-%m-%d"), strftime("%H:%M:%S"),str(hum)))
		
	#print("DHT22: " + str(temp_c))
		
def dataExport():
	writeDs18b20()
	writeDht22()
	
def dataRun():
	while True:
		dataExport()
		sleep(1)
