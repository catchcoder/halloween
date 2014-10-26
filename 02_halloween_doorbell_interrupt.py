# Halloween Scary doorbell with interrupt v1 

import RPi.GPIO as GPIO
import subprocess
import time
import os

GPIO.setmode(GPIO.BCM)

leds_pin = 17
btn_pin = 24
stop_pin = 23

GPIO.setup(leds_pin,GPIO.OUT)

GPIO.setup(btn_pin, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(stop_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(leds_pin,False)

proc = 0
blnflash = False
playing = False
#time_stamp = time.time()


def play_evil(channel):


	global proc
	if proc == 0:
		proc = 1
		#print ('Start')
		GPIO.output(leds_pin,True)
		subprocess.call(['mpg321', '/opt/ween/evillaugh.mp3','-q'])
		proc = subprocess.Popen(['mpg321', '/opt/ween/thisishalloweentrimmed.mp3','-q'])
		time.sleep(0.5)
	
def stop_play(channel):
	#print channel
	#print('Stopping')
	global proc	
	if proc != 0:
		#print ('pid ' + str(proc.pid))
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

GPIO.add_event_detect(btn_pin,GPIO.FALLING,callback=play_evil, bouncetime=500)
GPIO.add_event_detect(stop_pin,GPIO.FALLING,callback=stop_play, bouncetime=500)	
try:        

	while True:
			
         	if proc != 0:		
				
	        	blnflash = not blnflash
				
                        GPIO.output(leds_pin,blnflash)
                        blnflash = blnflash
			time.sleep(0.1)
				
			#if check_proc_running():
			#	stop_play()
		#		proc = 0
			
 		

		if proc == 0:
			time.sleep(0.4)

#finally:  
#    	print("Cleaning up")
#    	GPIO.cleanup()
except KeyboardInterrupt:
	GPIO.cleanup() # Clean up GPIO on CTRL+C exit

GPIO.cleanup() # Clean up GPIO on normal exit
