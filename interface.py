# import libraries
import os
import sys
import time
import datetime
import pigpio
import pygame

from pygame.locals import *
from time import sleep
from time import *
from datetime import datetime

pygame.init()

pi = pigpio.pi()

# GPIO pin connections

# motors (camera control)
servo_pan = 13
servo_tilt = 19

# lighting
led_vis1 = 16
led_vis2 = 20
led_ir = 21
led_uv = 12

# ir filter
filter_on = 6
filter_off = 5

# define filter mode (0 OFF, 1 ON)
filter_state = 0

# initialize pin i/o
pi.set_mode(servo_pan, pigpio.OUTPUT)
pi.set_mode(servo_tilt, pigpio.OUTPUT)
pi.set_mode(led_vis1, pigpio.OUTPUT)
pi.set_mode(led_vis2, pigpio.OUTPUT)
pi.set_mode(led_ir, pigpio.OUTPUT)
pi.set_mode(led_uv, pigpio.OUTPUT)

# initialize motor position at 0,0 (home)
angle_pan = 0
angle_tilt = 0
angle_rotate = 0

# component statuses
led1_state = 'OFF'
led2_state = 'OFF'
ir_state = 'OFF'
uv_state = 'OFF'

# initialize lighting pwm parameters
pi.set_PWM_dutycycle(led_vis1, 0)
pi.set_PWM_frequency(led_vis1, 200)

pi.set_PWM_dutycycle(led_vis2, 0)
pi.set_PWM_frequency(led_vis2, 200)

# Colours
grey_bg = (237, 236, 236)
white = (255, 255, 255)
bcit_blue = (19, 64, 107)
black = (0, 0, 0)

window_height = 470
window_width = 854

font_main = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 16)
font_title = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 16)
font_header = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 20)

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Undersea Laboratory Interface")

# sets position in degrees
def set_pos(angle):
	# normalize angle (-90 to 90) -> (0 to 1)
	angle_norm = (angle - -90) / (90 - -90)
	
	# linear transformation angle -> pwm
	return(angle_norm * (2500 - 500) + 500)
	
def camera_up():
	global servo_tilt, angle_tilt
	
	if (angle_tilt > -45):
		angle_tilt = angle_tilt - 0.2

		pi.set_servo_pulsewidth(servo_tilt, set_pos(angle_tilt))

# jog camera down
def camera_down():
	global servo_tilt, angle_tilt
	
	if (angle_tilt < 45):
		angle_tilt = angle_tilt + 0.2

		pi.set_servo_pulsewidth(servo_tilt, set_pos(angle_tilt))
		
# jog camera left until +17 deg
def camera_left():
	global servo_pan, angle_pan
	
	if (angle_pan < 17):
		angle_pan = angle_pan + 0.2

		pi.set_servo_pulsewidth(servo_pan, set_pos(angle_pan))
	
# jog camera right until -23 deg
def camera_right():
	global servo_pan, angle_pan
	
	if (angle_pan > -23):
		angle_pan = angle_pan - 0.2
		
		pi.set_servo_pulsewidth(servo_pan, set_pos(angle_pan))

# move camera home 0,0 center position
def camera_home():
	global servo_pan, servo_tilt
	global angle_pan, angle_tilt
	
	pi.set_servo_pulsewidth(servo_tilt, set_pos(0))
	pi.set_servo_pulsewidth(servo_pan, set_pos(0))
	
	angle_pan = 0
	angle_tilt = 0
	
def irFilterOn():
	global filter_state
	
	if filter_state == 0:
		filter_state = 1
		
		# pulse pin (10 ms)
		pi.write(filter_on, 1)
		pi.write(filter_off, 0)
		
		sleep(0.01)
		pi.write(filter_on, 0)
		pi.write(led_ir, 1)
		
def irFilterOff():
	global filter_state
	
	if filter_state == 1:
		filter_state = 0
		
		# pulse pin (10 ms)
		pi.write(filter_off, 1)
		pi.write(filter_on, 0)
		
		sleep(0.01)
		pi.write(filter_off, 0)
		pi.write(led_ir, 0)
		
		

def display():
	global angle_pan, angle_tilt, angle_rotate
	global led1_state, led2_state, ir_state, uv_state
	
	camera_home()
	
	bcit_logo = pygame.image.load('/mnt/usb/Media/bcit_header.png').convert_alpha()
	
	# layout panels
	header = pygame.Rect(10, 10, window_width - 20, 75)
	system_panel = pygame.Rect(10, 95, 250, window_height - 95 - 10)
	sensors_panel = pygame.Rect(270, 95, window_width - 270 - 10, 230)
	camera_panel = pygame.Rect(270, 75 + 20 + 200 + 10 + 30, window_width - 270 - 10, 125)
	
	system_header = pygame.Rect(10, 95, 250, 40)
	sensors_header = pygame.Rect(270, 95, window_width - 270 - 10, 40)
	camera_header = pygame.Rect(270, 75 + 20 + 200 + 10 + 30, window_width - 270 - 10, 40)
	
	# panel header titles
	system_title = font_header.render("SYSTEM", True, white)
	sensors_title = font_header.render("SENSORS", True, white)
	camera_title = font_header.render("CAMERA", True, white)
	
	# system labels
	light1_label = font_main.render("Light 1: ", True, bcit_blue)
	light2_label = font_main.render("Light 2: ", True, bcit_blue)
	ir_label = font_main.render("IR: ", True, bcit_blue)
	uv_label = font_main.render("UV: ", True, bcit_blue)
	
	# sensor labels
	ext_label = font_title.render("External", True, black)
	int_label = font_title.render("Internal", True, black)
	
	ext_temperature_label = font_main.render("Temperature: ", True, bcit_blue)
	ext_turbidity_label = font_main.render("Turbidity: ", True, bcit_blue)
	ext_salinity_label = font_main.render("Salinity: ", True, bcit_blue)
	ext_oxygen_label = font_main.render("Oxygen: ", True, bcit_blue)
	ext_depth_label = font_main.render("Depth: ", True, bcit_blue)
	ext_pressure_label = font_main.render("Pressure: ", True, bcit_blue)
	
	int_temperature_label = font_main.render("Temperature: ", True, bcit_blue)
	int_humidity_label = font_main.render("Humidity: ", True, bcit_blue)
	
	# camera labels
	pan_angle_label = font_main.render("Pan Angle: ", True, bcit_blue)
	tilt_angle_label = font_main.render("Tilt Angle: ", True, bcit_blue)
	rotate_angle_label = font_main.render("Rotate Angle: ", True, bcit_blue)
	
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
				
			if event.type == pygame.KEYDOWN:
				# move camera home
				if event.key == pygame.K_HOME:
					camera_home()
				
				# lighting control
				
				# control light 1
				if event.key == pygame.K_q:
					if (pi.read(led_vis1) == 1):
						pi.set_PWM_dutycycle(led_vis1, 0)
						led1_state = 'OFF'
					else:
						pi.set_PWM_dutycycle(led_vis1, 255)
						led1_state = 'ON'
				
				# control light 2
				if event.key == pygame.K_e:
					if (pi.read(led_vis2) == 1):
						pi.set_PWM_dutycycle(led_vis2, 0)
						led2_state = 'OFF'
					else:
						pi.set_PWM_dutycycle(led_vis2, 255)
						led2_state = 'ON'
						
				# control IR LEDs + filter
				if event.key == pygame.K_RIGHTBRACKET:
					irFilterOn()
					ir_state = 'ON'
						
				if event.key == pygame.K_LEFTBRACKET:
					irFilterOff()
					ir_state = 'OFF'

				with open("/mnt/usb/Component Status/light1.txt", "w") as txt:
					txt.write(led1_state)
					
				with open("/mnt/usb/Component Status/light2.txt", "w") as txt:
					txt.write(led2_state)
					
				with open("/mnt/usb/Component Status/ir_filter.txt", "w") as txt:
					txt.write(ir_state)
					
				with open("/mnt/usb/Component Status/uv_filter.txt", "w") as txt:
					txt.write(uv_state)
		
		# camera control
		key = pygame.key.get_pressed()

		if key[pygame.K_UP] or key[pygame.K_w]:
			camera_up()
		if key[pygame.K_DOWN] or key[pygame.K_s]:
			camera_down()
		if key[pygame.K_LEFT] or key[pygame.K_a]:
			camera_left()
		if key[pygame.K_RIGHT] or key[pygame.K_d]:
			camera_right()
		
		window.fill(grey_bg)
		
		# draw panels
		pygame.draw.rect(window, bcit_blue, header, 0)
		pygame.draw.rect(window, white, system_panel, 0)
		pygame.draw.rect(window, white, sensors_panel, 0)
		pygame.draw.rect(window, white, camera_panel, 0)
		
		# draw panel headers
		pygame.draw.rect(window, bcit_blue, system_header, 0)
		pygame.draw.rect(window, bcit_blue, sensors_header, 0)
		pygame.draw.rect(window, bcit_blue, camera_header, 0)
		
		# header bcit logo
		window.blit(bcit_logo, (10, 10))
		
		# header date and time
		date_data = font_main.render(strftime("%A, %b %-d, %Y"), True, white)
		date_width, date_height = font_main.size(strftime("%A, %b %-d, %Y"))
		window.blit(date_data, (window_width - date_width - 20, 20))
		
		time_data = font_main.render(strftime("%r"), True, white)
		time_width, time_height = font_main.size(strftime("%r"))
		window.blit(time_data, (window_width - time_width - 20, 40))
		
		# draw panel header titles
		window.blit(system_title, (20, 105))
		window.blit(sensors_title, (280, 105))
		window.blit(camera_title, (280, 75 + 20 + 200 + 10 + 40))
		
		# draw system labels
		window.blit(light1_label, (20, 145))
		window.blit(light2_label, (20, 145 + 16 + 10))
		window.blit(ir_label, (20, 145 + 32 + 20))
		window.blit(uv_label, (20, 145 + 48 + 30))
		
		# draw sensor labels
		window.blit(ext_label, (280, 145))
		window.blit(int_label, (560, 145))
		
		window.blit(ext_temperature_label, (280, 145 + 16 + 10))
		window.blit(ext_turbidity_label, (280, 145 + 32 + 20))
		window.blit(ext_salinity_label, (280, 145 + 48 + 30))
		window.blit(ext_oxygen_label, (280, 145 + 64 + 40))
		window.blit(ext_pressure_label, (280, 145 + 80 + 50))
		window.blit(ext_depth_label, (280, 145 + 96 + 60))

		window.blit(int_temperature_label, (560, 145 + 16 + 10))
		window.blit(int_humidity_label, (560, 145 + 32 + 20))
		
		# draw system data
		light1_data = font_main.render(led1_state, True, bcit_blue)
		window.blit(light1_data, (20 + 75, 145))
		
		light2_data = font_main.render(led2_state, True, bcit_blue)
		window.blit(light2_data, (20 + 75, 145 + 16 + 10))
		
		ir_data = font_main.render(ir_state, True, bcit_blue)
		window.blit(ir_data, (20 + 75, 145 + 32 + 20))
		
		uv_data = font_main.render(uv_state, True, bcit_blue)
		window.blit(uv_data, (20 + 75, 145 + 48 + 30))
		
		# draw sensors data
		ext_temperature_data = font_main.render(str(open('/mnt/usb/Sensor Data/DS18B20/ds18b20_temp_c.txt').read()) + ', ' + str(open('/mnt/usb/Sensor Data/DS18B20/ds18b20_temp_f.txt').read()), True, bcit_blue)
		window.blit(ext_temperature_data, (280 + 125, 145 + 16 + 10))
		
		ext_turbidity_data = font_main.render('N/A', True, bcit_blue)
		window.blit(ext_turbidity_data, (280 + 125, 145 + 32 + 20))
		
		ext_salinity_data = font_main.render('N/A', True, bcit_blue)
		window.blit(ext_salinity_data, (280 + 125, 145 + 48 + 30))
		
		ext_oxygen_data = font_main.render('N/A', True, bcit_blue)
		window.blit(ext_oxygen_data, (280 + 125, 145 + 64 + 40))
		
		ext_pressure_data = font_main.render('N/A', True, bcit_blue)
		window.blit(ext_pressure_data, (280 + 125, 145 + 80 + 50))
		
		ext_depth_data = font_main.render('N/A', True, bcit_blue)
		window.blit(ext_depth_data, (280 + 125, 145 + 96 + 60))
		
		int_temperature_data = font_main.render(str(open('/mnt/usb/Sensor Data/DHT22/dht22_temp_c.txt').read()) + ', ' + str(open('/mnt/usb/Sensor Data/DHT22/dht22_temp_f.txt').read()), True, bcit_blue)
		window.blit(int_temperature_data, (560 + 125, 145 + 16 + 10))
		
		int_humidity_data = font_main.render(str(open('/mnt/usb/Sensor Data/DHT22/dht22_hum.txt').read()), True, bcit_blue)
		window.blit(int_humidity_data, (560 + 125, 145 + 32 + 20))
		
		# draw camera labels
		window.blit(pan_angle_label, (280, 75 + 20 + 200 + 10 + 40 + 40))
		window.blit(tilt_angle_label, (280, 75 + 20 + 200 + 10 + 40 + 40 + 16 + 10))
		window.blit(rotate_angle_label, (280, 75 + 20 + 200 + 10 + 40 + 40 + 32 + 20))
		
		# draw camera data
		pan_angle_data = font_main.render(str(f"{-angle_pan:.1f}") + '°', True, bcit_blue)
		window.blit(pan_angle_data, (280 + 125, 75 + 20 + 200 + 10 + 40 + 40))
		
		tilt_angle_data = font_main.render(str(f"{-angle_tilt:.1f}") + '°', True, bcit_blue)
		window.blit(tilt_angle_data, (280 + 125, 75 + 20 + 200 + 10 + 40 + 40 + 16 + 10))
		
		rotate_angle_data = font_main.render(str(f"{-angle_rotate:.1f}") + '°', True, bcit_blue)
		window.blit(rotate_angle_data, (280 + 125, 75 + 20 + 200 + 10 + 40 + 40 + 32 + 20))
		
		pygame.display.update()
