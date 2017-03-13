#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
 
RoAPin = 11    # pin11
RoBPin = 12    # pin12
 
globalCounter = 0
dist = 0.0 
flag = 0
sum = 0
Last_RoB_Status = 0
Current_RoB_Status = 0
 
def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(RoAPin, GPIO.IN)    # input mode
    GPIO.setup(RoBPin, GPIO.IN)
 
def rotaryDeal():
    global flag
    global Last_RoB_Status
    global Current_RoB_Status
    global globalCounter
    global dist
    global sum
    Last_RoB_Status = GPIO.input(RoBPin)
    while(not GPIO.input(RoAPin)):
        Current_RoB_Status = GPIO.input(RoBPin)
        flag = 1
    if flag == 1:
        flag = 0
        if (Last_RoB_Status == 0) and (Current_RoB_Status == 1):
            globalCounter = globalCounter + 1
            #print "Dist : " + str(globalCounter*1.475)
        if (Last_RoB_Status == 1) and (Current_RoB_Status == 0):
            globalCounter = globalCounter - 1
 
def loop():
    global globalCounter
    while True:
        rotaryDeal()
        print 'globalCounter = %d' % globalCounter
        print 'Dist = ' + str(globalCounter*1.475)
 
def destroy():
    GPIO.cleanup()             # Release resource
 
if __name__ == '__main__':     # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()