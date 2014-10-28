# Halloween Scary doorbell with interrupt v1 

import RPi.GPIO as GPIO
import subprocess
import time
import os

GPIO.setmode(GPIO.BCM)

# set pins used
leds_pin = 17
btn_pin = 24
stop_pin = 23

GPIO.setup(leds_pin,GPIO.OUT)

GPIO.setup(btn_pin, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(stop_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# switch  off leds
GPIO.output(leds_pin,False)

proc = 0
blnflash = False
playing = False

# location of files used
mp3_laugh = "/opt/ween/evillaugh.mp3" # evil laugh file 3 to 5 seconds
mp3_tune = "/opt/ween/thisishalloweentrimmed.mp3" # tune to play whilst trick or treaters collect sweets


def play_evil(channel):
	global proc
	if proc == 0:
		proc = 1
		GPIO.output(leds_pin,True)
		subprocess.call(['mpg321', mp3_laugh ,'-q'])
		proc = subprocess.Popen(['mpg321', mp3_tune,'-q'])
		time.sleep(0.5)

def stop_play(channel): 
	global proc	
	if proc != 0 and not type(proc) is int:
		subprocess.Popen.kill(proc)
		GPIO.output(leds_pin,False)
		proc = 0

def check_proc_running():
	global proc
	p = subprocess.Popen(["ps aux | grep 'mpg321' | grep 'defunct'"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	if proc != 0:
		for line in iter(p.stdout.readline,''):
			line = line.replace('\r','').replace('\n','')
			if 'mpg321' in line and 'defunct' in line and not 'ps' in line and not type(proc) is int: 
				subprocess.Popen.kill(proc)
				GPIO.output(leds_pin,False)
				proc = 0
				return True
		
			p.stdout.flush

#Set interrupt for play laugh and tune
GPIO.add_event_detect(btn_pin,GPIO.FALLING,callback=play_evil, bouncetime=500)
#set interrupt to stop playing tune
GPIO.add_event_detect(stop_pin,GPIO.FALLING,callback=stop_play, bouncetime=500)	

try:        

	while True:
			
         	if proc != 0:		
				
	        	blnflash = not blnflash
				
                        GPIO.output(leds_pin,blnflash)
                        blnflash = blnflash
			time.sleep(0.1)

		if proc !=0 :
			check_proc_running()
		
 		
		if proc == 0:
			time.sleep(0.4)
		

except KeyboardInterrupt:
	GPIO.cleanup() # Clean up GPIO on CTRL+C exit

GPIO.cleanup() # Clean up GPIO on normal exit
