#!/usr/bin/python
# -*- coding: utf-8 -*-

########################################################################
##               		{FFMPEG Command Script}                       ##
########################################################################
"""

Description: This script builds and runs the FFMPEG command needed to
			 stream to YouTube. The command parameters are described and
			 only intended to work with the Undersea Laboratory camera
			 setup. 

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
	params_dict["video_codec"] = "h264_v4l2m2m"
	
	# variable bitrate (not needed?)
	params_dict["variable_br"] = "820k"
	
	# pixel format 
	params_dict["pixel_format"] = "yuyv422"
	
	# picture group (depracated)
	params_dict["pic_group"] = "60"
	
	#framerate (adjust to experienced fps)
	params_dict["framerate"] = "30"
	
	# output file
	params_dict["output_format"] = "flv"
		
	# force image to 1280x720 pixels
	params_dict["scale"] = "scale=1280:720"
	
	# flip screen (vertical)
	params_dict["flip_vertical"] = "vflip"
	
	# flip screen (horizontal)
	params_dict["flip_horizontal"] = "hflip"

	
	# send output to rtmp server (youtube)
	# replace with your livestream key!
	params_dict["youtube"] = "rtmp://a.rtmp.youtube.com/live2/m1qh-wagz-bm0p-axdh-6wak"
	
	params_dict["filters"] = params_dict["scale"] + "," +  params_dict["flip_vertical"] + "," +  params_dict["flip_horizontal"]
	return params_dict
	
def buildCommand():
	params_build = setCommand()
	
	command = [
			"ffmpeg",
			"-nostdin", 	# prevent clogging
			"-f",
			params_build["video_format"],
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
