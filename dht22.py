#!/usr/bin/python
# -*- coding: utf-8 -*-

########################################################################
##					      {DHT22 Sampling Script}				      ##
########################################################################
"""

Description: Receives data from dht22 sensor and formats data strings 
			 to display values of interest. Script returns temperature
			 values in celsius and farenheit as well as humidity values.
			 
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
import adafruit_dht
import board
import time
from time import *

dht_device = adafruit_dht.DHT22(board.D17, use_pulseio=False)
err_flag = 1

temp_c = 0
temp_f = 0
hum = 0

# extract and format temperature and humidity values
def getTempHum():
	global temp_c, temp_f, hum
	try:
		temp_c = dht_device.temperature
		temp_f = temp_c * (9/5) + 32
		hum = dht_device.humidity

	except RuntimeError as error:
		pass
	except Exception as error:
		dht_device.exit()
	except TypeError as error:
		dht_device.exit()
	
	return temp_c, temp_f, hum
			
# view/debug sensor via terminal
def displayTerminal():
	while True:
		temp_c, temp_f, hum = getTempHum()
	
		print("{0}, {1}, {2}, {3}, {4}\n".format("DATE: "+ strftime("%Y-%m-%d"), "TIME: " + strftime("%H:%M:%S"), str(temp_c) + " C", str(temp_f) + " F", str(hum) + "%"))
		sleep(1)
