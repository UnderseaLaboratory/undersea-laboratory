#!/usr/bin/python
# -*- coding: utf-8 -*-

########################################################################
##					    {DS18B20 Sampling Script}				      ##
########################################################################
"""

Description: Receives data from ds18b20 sensor and formats data strings 
			 to display values of interest. Script returns temperature
			 values in celsius and farenheit.
			 
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
import os
import glob
import curses
from time import *
from time import sleep

# initialize variable placeholders
dev_folder = ''
dev_file = ''

temp = 0
temp_c = 0
temp_f = 0

conn_status = 0
read_status = 0

# connection error handling
def checkStatus():
	global dev_folder, dev_file
	
	# check if sensor is connected
	try:
		# load 1-wire comm kernel
		os.system('modprobe w1-gpio')
		os.system('modprobe w1-therm')
				
		# find sensor address
		base_dir = '/sys/bus/w1/devices/'
		
		dev_folder = glob.glob(base_dir + '28*')[0]
		dev_file = dev_folder + '/w1_slave'
	except IndexError:
		return 0
	else:
		return 1

# read raw data
def getData():
	global dev_file, dev_folder
	
	f = open(dev_file, 'r')
	data = f.readlines()
	f.close()
	
	return data

# extract and format temperature values
def getTemp():
	global conn_status, read_status
	global temp, temp_c, temp_f
	
	if checkStatus() == 1:
		try:
			data = getData()	# retrieve 2 lines of 1-wire data
			
			# strip first line
			while data[0].strip()[-3:] != 'YES':
				data = getData()
				
			# extract temperature value
			temp_pos = data[1].find('t=')
			temp = float(data[1][temp_pos+2:])
		except IndexError:
			#print("failed to poll ds18b20")
			pass
			
			temp_c = temp / 1000.0
			temp_f = temp_c * 9.0 / 5.0 + 32.0
				
		return temp_c, temp_f
	else:
		return 0.0, 0.0

# view/debug sensor via terminal
def displayTerminal():
	while True:
		temp_c, temp_f = getTemp()
	
		print("{0}, {1}, {2}, {3}\n".format("DATE: "+ strftime("%Y-%m-%d"), "TIME: " + strftime("%H:%M:%S"), str(temp_c) + " C", str(temp_f) + " F"))

def run():
	while True:
		print("Connection: " + str(checkStatus()))
		print("Data: " + str(getTemp()))
		sleep(1)
