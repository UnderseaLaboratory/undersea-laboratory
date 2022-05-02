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
from time import *

# load 1-wire comm kernel
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# find sensor address
base_dir = '/sys/bus/w1/devices/'
dev_folder = glob.glob(base_dir + '28*')[0]
dev_file = dev_folder + '/w1_slave'

# read raw data
def getData():
	f = open(dev_file, 'r')
	data = f.readlines()
	f.close()
	
	return data

# extract and format temperature values
def getTemp():
	data = getData()	# retrieve 2 lines of 1-wire data
	
	# strip first line
	while data[0].strip()[-3:] != 'YES':
		data = getData()
		
	# extract temperature value
	temp_pos = data[1].find('t=')
	temp = float(data[1][temp_pos+2:])
	
	# format temperature values
	temp_c = temp / 1000.0
	temp_f = temp_c * 9.0 / 5.0 + 32.0
	
	return temp_c, temp_f	
	
