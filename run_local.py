#!/usr/bin/python
# -*- coding: utf-8 -*-

########################################################################
##               	         {Main Program}                           ##
########################################################################
"""s

Description: Main Undersea Laboratory program. Allocates processes and
			 threads. Runs all control and module scripts concurrently
			 with display and user feedback.

"""
########################################################################

# import libraries
import os
import subprocess
import threading

from time import *
from time import sleep
from multiprocessing import Process
from threading import Thread

# import system modules
from stream_local import runCommand
from interface import display
from data_log_local import dataRun

def main(args):
	stream_proc = Process(target = runCommand)
	stream_proc.start()
	
	interface_proc = Process(target = display)
	interface_proc.start()
	
	data_proc = Thread(target = dataRun)
	data_proc.start()
	
	stream_proc.join()
	interface_proc.join()
	data_proc.join()
	
	return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

