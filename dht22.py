#!/usr/bin/python
# -*- coding: utf-8 -*-

########################################################################
##					    {DHT22 Sampling Script}				      ##
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

dht_device = adafruit_dht.DHT22(board.D17, use_pulseio=False)

# extract and format temperature and humidity values
def getTempHum():
    try:
        temp_c = dht_device.temperature
        temp_f = temp_c * (9/5) + 32
        hum = dht_device.humidity
        
        return temp_c, temp_f, hum
    
    except RuntimeError as error:
        time.sleep(2)
    except Exception as error:
        dht_device.exit()
        raise error

    
    
