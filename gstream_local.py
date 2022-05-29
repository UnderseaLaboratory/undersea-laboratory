#!/usr/bin/python
# -*- coding: utf-8 -*-

########################################################################
##               	   {GStreamer Command Script}                     ##
########################################################################
"""

Description: This script builds and runs the GStreamer command needed to
			 stream to a client on a local network.

"""
########################################################################

__author__ = "Aleks Zawadzki, Eric Cheng"
__copyright__ = "Open-Source 2021, Undersea Laboratory"
__credits__ = "Aleks Zawadzki, Eric Cheng, Mo Amirian, David Tang"

__version__ = "1.1.0"
__maintainer__ = "Aleks Zawadzki"
__email__ = "alekzawadzki@outlook.com"
__status__ = "Production"

# import libraries
import subprocess
import sys
import time
import datetime
import os

# stream parameters
video_width = 640
video_height = 480

host = '192.168.0.102'
port = '5000'


def run():
	os.system(f"gst-launch-1.0 -vv -e v4l2src device='/dev/video0' ! videoflip method=vertical-flip ! video/x-raw,width={video_width},height={video_height},framerate=15/1 ! jpegenc ! rtpjpegpay ! udpsink host={host} port={port}")  

run()
