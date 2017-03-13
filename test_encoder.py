import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
global lastDataPin
global currentDataPin
lastDataPin=0
currentDataPin=0
global globalCounter
globalCounter = 0

def myinput(channel):
   global currentDataPin
   global lastDataPin
   global globalCounter
   currentDataPin = GPIO.input(12)
   if lastDataPin == 0 and currentDataPin == 1:
      if GPIO.input(11) == 0:
         globalCounter += 1
      else:
         globalCounter -=1
      print "globalCounter: " + str(globalCounter)
   lastDataPin = currentDataPin

GPIO.add_event_detect(12, GPIO.BOTH, callback=myinput, bouncetime=1)

try:
   print "H"
   time.sleep(3)#time.sleep()
except KeyboardInterrupt:   
   GPIO.cleanup()
GPIO.cleanup()
