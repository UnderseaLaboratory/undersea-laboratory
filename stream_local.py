#!/usr/bin/python
# -*- coding: utf-8 -*-

########################################################################
##                  	{FFMPEG UDP Command Script}                   ##
########################################################################
"""

Description: This script builds and runs the FFMPEG command needed to
			 stream to a client device on the same network. The command 
			 parameters are described and only intended to work with the
			 Undersea Laboratory camera setup. 

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

def setCommand():
	
	params_dict = {}
	
	# input video format (v4l2 = video4linux2)
	params_dict["video_format"] = "v4l2"
	
	# input source. camera stream or video file 
	# check src with cmd: v4l2-ctl --list-devices
	params_dict["video_source"] = "/dev/video0"
	
	# audio loop in the case hydrophone is not used
	#params_dict["audio_format"] = "mp3"
	
	#params_dict["audio_loop"] = "-1"
	
	#params_dict["audio_source"] = "/home/pi/Undersea_Laboratory/Soundtracks/undersea_ambience.mp3"
	
	#params_dict["audio_codec"] = "mp2"
	
	# hydrophone input
	# type command aplay -l to check card number
	params_dict["hydrophone_source"] = "plughw:1,0"
	
	params_dict["hydrophone_interface"] = "alsa"
	
	params_dict["hydrophone_codec"] = "libmp3lame"
	
	# audio bitrate
	params_dict["audio_br"] = "128k"
	
	# audio sampling rate 
	params_dict["audio_sr"] = "44100"
	
	# audio channels
	params_dict["audio_ch"] = "2"
	
	# standard adherance priority
	params_dict["standards"] = "experimental"
	
	# frame size
	params_dict["frame_size"] = "1280x720"
	
	# video bitrate
	params_dict["video_br"] = "6000000"
	
	# aspect ratio
	params_dict["aspect_ratio"] = "16:9"
	
	# video codec (hw accelerated)
	params_dict["video_codec"] = "mpeg4"
	
	# variable bitrate (not needed?)
	params_dict["variable_br"] = "820k"
	
	# pixel format 
	params_dict["pixel_format"] = "yuyv422"
	
	# picture group (depracated)
	params_dict["pic_group"] = "60"
	
	#framerate (adjust to experienced fps)
	params_dict["framerate"] = "30"
	
	# output file
	params_dict["output_format"] = "mpegts"
		
	# force image to 1280x720 pixels
	params_dict["scale"] = "scale=1280:720"
	
	# flip screen (vertical)
	params_dict["flip_vertical"] = "vflip"
	
	# flip screen (horizontal)
	params_dict["flip_horizontal"] = "hflip"
	
	# send output to udp client (local)
	params_dict["youtube"] = "udp://192.168.0.102:5000"
	
	# date display (strftime)
	params_dict["time"] = "drawtext=expansion=strftime:fontfile=/usr/share/fonts/truetype/freefont/FreeSans.ttf:fontsize=24:fontcolor=white:shadowx=1:shadowy=1:text="'%r'":x=5:y=32"
	
	# time display (strftime)
	params_dict["date"] = "drawtext=expansion=strftime:fontfile=/usr/share/fonts/truetype/freefont/FreeSans.ttf:fontsize=24:fontcolor=white:shadowx=1:shadowy=1:text="'%A\\\\\, %b %-d\\\\\, %Y'":x=5:y=5"
	
	# ds18b20 temperature display (.txt file)
	params_dict["temp_label"] = "drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeSans.ttf:fontsize=24:fontcolor=white:shadowx=1:shadowy=1:text="'Temperature\\\\\: '":x=5:y=691"
	params_dict["temp_data"] = "drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeSans.ttf:fontsize=24:fontcolor=white:shadowx=1:shadowy=1:textfile=/mnt/usb/Sensor Data/DS18B20/ds18b20_temp_c.txt:reload=1:x=155:y=692"
	
	# turbidity display (TEMPLATE)
	params_dict["turb_label"] = "drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeSans.ttf:fontsize=24:fontcolor=white:shadowx=1:shadowy=1:text="'Turbidity\\\\\:          NTU'":x=275:y=691"
	params_dict["turb_data"] = "drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeSans.ttf:fontsize=24:fontcolor=white:shadowx=1:shadowy=1:text="'?'":x=400:y=691"
	
	# salinity display (TEMPLATE)
	params_dict["sal_label"] = "drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeSans.ttf:fontsize=24:fontcolor=white:shadowx=1:shadowy=1:text="'Salinity\\\\\:          S/m'":x=540:y=691"
	params_dict["sal_data"] = "drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeSans.ttf:fontsize=24:fontcolor=white:shadowx=1:shadowy=1:text="'?'":x=650:y=691"
	
	# IR status display
	params_dict["ir_label"] = "drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeSans.ttf:fontsize=24:fontcolor=white:shadowx=1:shadowy=1:text="'IR\\\\\: '":x=1179:y=664"
	params_dict["ir_data"] = "drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeSans.ttf:fontsize=24:fontcolor=white:shadowx=1:shadowy=1:textfile=/mnt/usb/Component Status/ir_filter.txt:reload=1:x=1225:y=664"
	
	# UV status display
	params_dict["uv_label"] = "drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeSans.ttf:fontsize=24:fontcolor=white:shadowx=1:shadowy=1:text="'UV\\\\\: '":x=1171:y=691"
	params_dict["uv_data"] = "drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeSans.ttf:fontsize=24:fontcolor=white:shadowx=1:shadowy=1:textfile=/mnt/usb/Component Status/uv_filter.txt:reload=1:x=1225:y=691"
	
	# LED1 status display
	params_dict["led1_label"] = "drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeSans.ttf:fontsize=24:fontcolor=white:shadowx=1:shadowy=1:text="'LED1\\\\\: '":x=1145:y=610"
	params_dict["led1_data"] = "drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeSans.ttf:fontsize=24:fontcolor=white:shadowx=1:shadowy=1:textfile=/mnt/usb/Component Status/light1.txt:reload=1:x=1225:y=610"

	# LED2 status display
	params_dict["led2_label"] = "drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeSans.ttf:fontsize=24:fontcolor=white:shadowx=1:shadowy=1:text="'LED2\\\\\: '":x=1145:y=637"
	params_dict["led2_data"] = "drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeSans.ttf:fontsize=24:fontcolor=white:shadowx=1:shadowy=1:textfile=/mnt/usb/Component Status/light2.txt:reload=1:x=1225:y=637"
	
	# BCIT logo
	params_dict["logo1"] = "drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeSansBold.ttf:fontsize=50:fontcolor=white:shadowx=1:shadowy=1:text="'BCIT'":x=1005:y=5"
	params_dict["logo2"] = "drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeSansBold.ttf:fontsize=40.5:fontcolor=white:shadowx=1:shadowy=1:text="'|'":x=1127:y=5"
	params_dict["logo3"] = "drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeSans.ttf:fontsize=19:fontcolor=white:shadowx=1:shadowy=1:text="'UNDERSEA'":x=1142:y=6"
	params_dict["logo4"] = "drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeSans.ttf:fontsize=19:fontcolor=white:shadowx=1:shadowy=1:text="'LABORATORY'":x=1142:y=28"
	
	
	params_dict["filters"] = params_dict["scale"] + "," +  params_dict["flip_vertical"] + "," +  params_dict["flip_horizontal"] + "," + params_dict["time"] + "," + params_dict["date"] + "," + params_dict["temp_label"] + "," + params_dict["temp_data"] + "," + params_dict["turb_label"] + "," + params_dict["sal_label"] + "," + params_dict["ir_label"] + "," + params_dict["ir_data"] + "," + params_dict["led1_label"] + "," + params_dict["led1_data"] + "," + params_dict["led2_label"] + "," + params_dict["led2_data"]  + "," + params_dict["uv_label"] + "," + params_dict["uv_data"] + "," + params_dict["logo1"] + "," + params_dict["logo2"] + "," + params_dict["logo3"] + "," + params_dict["logo4"]
	return params_dict
	
def buildCommand():
	params_build = setCommand()
	
	command = [
			"ffmpeg",
			"-nostdin", 	# prevent clogging
			"-f",
			params_build["video_format"],
			"-re",
			"-i",
			params_build["video_source"],
			#"-f",
			#params_build["audio_format"],
			#"-stream_loop",
			#params_build["audio_loop"],
			#"-i",
			#params_build["audio_source"],
			#"-acodec",
			#params_build["audio_codec"],
			"-f",
			params_build["hydrophone_interface"],
			"-i",
			params_build["hydrophone_source"],
			"-ab",
			params_build["audio_br"],
			"-ar",
			params_build["audio_sr"],
			"-ac",
			params_build["audio_ch"],
			"-strict",
			params_build["standards"],
			"-s",
			params_build["frame_size"],
			"-b:v",
			params_build["video_br"],
			"-aspect",
			params_build["aspect_ratio"],
			"-vcodec",
			params_build["video_codec"],
			"-vb",
			params_build["variable_br"],
			"-pix_fmt",
			params_build["pixel_format"],
			"-g",
			params_build["pic_group"],
			"-r",
			params_build["framerate"],
			"-f",
			params_build["output_format"],
			"-vf",
			params_build["filters"],
			params_build["youtube"]
			]
		
	return command
	
def runCommand():
	command = buildCommand()
	#print(command)
	
	while True:
		try:
			if subprocess.run(command, stdin=None, stdout=None, timeout=1800, check=True).returncode == 0:
				print("Stream Succesfull...")
			else:
				print("Stream Failed. Restarting...")
				continue
		except subprocess.TimeoutExpired:
			continue
		except subprocess.CalledProcessError:
			continue
