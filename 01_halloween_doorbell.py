# Halloween Scary doorbell v1 

import RPi.GPIO as GPIO
import subprocess
import time
import os

GPIO.setmode(GPIO.BCM)

leds_pin = 22
btn_pin = 24

GPIO.setup(leds_pin,GPIO.OUT)

GPIO.setup(btn_pin, GPIO.IN,pull_up_down=GPIO.PUD_UP)

GPIO.output(leds_pin,False)

proc = 0
blnflash = False

def play_evil():
	GPIO.output(leds_pin,True)
	subprocess.call(['mpg321', '/opt/ween/evillaugh.mp3','-q'])
	proc = subprocess.Popen(['mpg321', '/opt/ween/thisishalloweentrimmed.mp3','-q'])
	return proc

def stop_play(proc):
	subprocess.Popen.kill(proc)
	GPIO.output(leds_pin,False)
	proc = 0

def check_proc_running():
	proc = subprocess.Popen(["ps aux | grep 'mpg321' | grep 'defunct'"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	
	
	for line in iter(proc.stdout.readline,''):
		line = line.replace('\r','').replace('\n','')
		if 'mpg321' in line and 'defunct' in line and not 'ps' in line: 
			return True
		
		proc.stdout.flush
	
try:        

	while True:
			
         	if proc != 0:		
				
	        	blnflash = not blnflash
				
                        GPIO.output(leds_pin,blnflash)
                        blnflash = blnflash
			time.sleep(0.1)
				
			if check_proc_running():
				stop_play(proc)
				proc = 0
		

 		if GPIO.input(btn_pin) == False:
			if proc == 0 :
				proc = play_evil()
			else:
				stop_play(proc)
				proc = 0
				time.sleep(1.0)	
 		

		if proc == 0:
			time.sleep(0.4)

#finally:  
#    	print("Cleaning up")
#    	GPIO.cleanup()
except KeyboardInterrupt:
	GPIO.cleanup() # Clean up GPIO on CTRL+C exit

GPIO.cleanup() # Clean up GPIO on normal exit
