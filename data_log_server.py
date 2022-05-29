#!/usr/bin/python
# -*- coding: utf-8 -*-

########################################################################
##					      {Data Logging Script}			    	      ##
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
import thingspeak
import time
import mysql.connector

from time import *
from time import sleep, perf_counter
from mysql.connector import Error
from datetime import datetime

import ds18b20
import dht22

# thingspeak initialization
channel_id = 1666401 # channel ID
write_key  = 'ITW2N7X4XTPOH2IH' # write key
read_key   = 'WTUPZAC91RQMPB45' # read key

channel = thingspeak.Channel(channel_id, write_key, read_key)

# initialize mysql database
read_interval = 1
host = '50.87.232.245'
database = 'undersf3_temp'
user = 'undersf3_admin'
password = 'aaabb'

format = ("%Y-%m-%d %H:%M:%S")

sql_list = ''

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
	global sql_list 
	
	temp_c, temp_f = ds18b20.getTemp()	# retreive data
	
	# format data
	temp_c = dataFormat(temp_c)
	temp_f = dataFormat(temp_f)
	
	# write data to .txt files
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
	
	sql_list = [datetime.now().strftime(format), str(temp_c)]
		
	ds18b20_ts_Data = channel.update({'field3': temp_c})	# write data to thingspeak

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
		
	dht22_ts_data = channel.update({'field1':temp_c, 'field2': hum})	# write data to thingspeak

def dataExport():
	writeDs18b20()
	writeDht22()
	writeSql()
	
	read_ts = channel.get()
	
def dataRun():
	while True:
		dataExport()
		sleep(1)

# exports data to mySQL database
def writeSql():
	global sql_list
	start = perf_counter()
	
	try:
		connection = mysql.connector.connect(host = host, database = database, user = user, password = password)
		if connection.is_connected():
			db = connection.get_server_info()
			#print("Connected to MySQL Server Version ", db)
			
			cursor = connection.cursor()
			cursor.execute("select database();")
			
			record = cursor.fetchone()
			#print("You're connected to database: ", record)
			
			cursor.execute('Insert into waterTemperature(sample_date, water_temperature)' 'values(%s, %s)', sql_list)
			connection.commit()
			
			#print(f'{datetime.now().strftime(format)}Done inserting into SQL Database')
			connection.close()
			
			# calculate elapsed time
			end = perf_counter()
			elapse_time = end - start
			#print(f"elapse time: {elapse_time}")
			
			if elapse_time >= read_interval:
				elapse_time = read_interval
				#print(f"elapse time exceed, sleep will be set to {read_interval - elapse_time}")
			sleep(read_interval - elapse_time)
		
	except Error as err:
		print("Error while connecting to MySQL", err)
	
	finally:
		connection.close()
