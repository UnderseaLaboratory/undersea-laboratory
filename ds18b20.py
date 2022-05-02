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
	
# view/debug sensor via terminal
def displayTerminal():
	while True:
		temp_c, temp_f = getTemp()
	
		print("{0}, {1}, {2}, {3}\n".format("DATE: "+ strftime("%Y-%m-%d"), "TIME: " + strftime("%H:%M:%S"), str(temp_c) + " C", str(temp_f) + " F"))
		sleep(1)

# view/debug sensor via curses
def displayCurses():
	stdscreen = curses.initscr()
	curses.curs_set(0)
	
	key = 0
	
	while (key != curses.KEY_BACKSPACE):
		temp_c, temp_f = getTemp()
			
		stdscreen.addstr(0, 0, "DS18B20 (C): ")
		stdscreen.addstr(0, 15, str(temp_c))
		
		stdscreen.addstr(1, 0, "DS18B20 (F): ")
		stdscreen.addstr(1, 15, str(temp_f))
		
		stdscreen.refresh()
		stdscreen.nodelay(1)
		key = stdscreen.getch()
	
