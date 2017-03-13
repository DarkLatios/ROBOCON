import RPi.GPIO as GPIO
import cv2
import math
import time
import numpy as np
import threading
GPIO.setmode(GPIO.BOARD)
GPIO.setup(36, GPIO.OUT)
pwm = GPIO.PWM(36, 100)
pwm.start(5)
area_flag = 0
flag_90 = 0
vc=cv2.VideoCapture(0)
vc.set(3, 160)
vc.set(4, 120)
harish=0
retr= 0

cross_area = 0
main_flag = 1
dist_thresh = 0
thread_flag = 0

oldangle=0
area_45 = 1
cross = 0  

#-------------------------Encoder---------------------------------------------------------------
RoAPin = 11    # pin11
RoBPin = 12    # pin12

GPIO.setup(RoAPin, GPIO.IN)    # input mode
GPIO.setup(RoBPin, GPIO.IN)
 
globalCounter = 0
dist = 0.0 
flag = 0
sum = 0
Last_RoB_Status = 0
Current_RoB_Status = 0
 
     
def rotaryDeal():
    global flag
    global Last_RoB_Status
    global Current_RoB_Status
    global globalCounter
    global dist
    global sum
    global RoBPin
    global RoAPin
    
    Last_RoB_Status = GPIO.input(RoBPin)
    while(not GPIO.input(RoAPin)):
        Current_RoB_Status = GPIO.input(RoBPin)
        flag = 1 
    print "AAAAAAAAAAAAAAAAAa" 
    if flag == 1:
        flag = 0
        if (Last_RoB_Status == 0) and (Current_RoB_Status == 1):
            globalCounter = globalCounter + 1
            #print "Dist : " + str(globalCounter*1.475)
        if (Last_RoB_Status == 1) and (Current_RoB_Status == 0):
            globalCounter = globalCounter - 1
    return
 
def loop():
    global globalCounter 
    global main_flag
    global dist_thresh
    print (" Entering Loop")
    if main_flag == 4:
        globalCounter = 0
        main_flag = 4.5
    if main_flag == 6:
        globalCounter = 0
        main_flag = 6.5
    
    if dist_thresh == 1 and globalCounter < 3:
       print 'globalCounter = %d' % globalCounter
       print 'Dist = ' + str(globalCounter*1.475) 
    if main_flag == 4.5 and globalCounter >= 3:
        main_flag = 5   
    if dist_thresh == 2 and globalCounter < 10:   
       print 'globalCounter = %d' % globalCounter
       print 'Dist = ' + str(globalCounter*1.475)
    if main_flag == 6.5 and globalCounter >= 10:
        main_flag = 7   
    print ("exit loop")      
 
def destroy():
    GPIO.cleanup()             # Release resource
#-----------------------------------------------------------------------------------------------


#--------------------------------------------
myThread = threading.Thread(target=rotaryDeal)
myThread.daemon = True
if not myThread.isAlive():
     myThread.start()
while(vc.isOpened()):
    #img=cv2.imread("1.png")
    ret,imgi =vc.read()
    #cv2.imshow('Output',img)
    img = cv2.flip(imgi, 1)
    #img = cv2.flip(imgr, 1)
    img2 =cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    x=200
    imgthreshold=cv2.inRange(img,cv2.cv.Scalar(x,x,x),cv2.cv.Scalar(255,255,255),)
    cv2.imshow('threshold',imgthreshold)
    
    edges=cv2.Canny(imgthreshold,100,200)
    #cv2.imshow('Filter',edges)
    im2, hierarchy = cv2.findContours(imgthreshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


    areas = [cv2.contourArea(c) for c in im2]
    #FIX: max_index will be null if argmax has no arguments


    #check max area
    if areas != []:
       if max(areas) > 2800:
         cross_area = 1
       else:
         cross_area = 0         
    
    #------------------------------------main code------------------------------------------

    print "Main Flag: " + str(main_flag)
    if areas != [] :
        print "HELLO : " + str(max(areas))

    #rotaryDeal()
    
    
    if main_flag == 1 and areas == [] and area_flag == 1:
        duty1 = int(45)/10 + 2.5
        pwm.ChangeDutyCycle(duty1)
        harish = duty1         
        print "main flag 1 passed : 60 degrees "
        main_flag = 2
        cross_area = 0

    elif main_flag == 2 and cross_area == 1:
        main_flag = 3
      
    elif main_flag == 3 and areas != []:
        max_index = np.argmax(areas)
        cnt=im2[max_index]
        x,y,w,h = cv2.boundingRect(cnt)
        if y > 14:
           duty1 = int(60)/10 + 2.5
           pwm.ChangeDutyCycle(duty1)
           harish = duty1         
           print "main flag 3 passed == 60 degrees "
           cross_area = 0
           dist_thresh = 1
           main_flag = 4
           print "Encoder1 Started :"
           loop()

    elif main_flag == 4.5:
        loop()     
    
    elif main_flag == 5:
        duty1 = int(90)/10 + 2.5
        pwm.ChangeDutyCycle(duty1)
        harish = duty1         
        print "main flag 5 passed == 90 degrees "
        dist_thresh = 2
        main_flag = 6
        loop()
        cross_area = 0

    elif main_flag == 6.5:
        loop()

    elif main_flag == 7:
        duty1 = int(135)/10 + 2.5
        pwm.ChangeDutyCycle(duty1)
        harish = duty1         
        print "main flag 7 passed == 135 degrees "
        main_flag = 1        

    elif areas!=[] and main_flag<=2: 
        
        max_index = np.argmax(areas)
        print str(max(areas))
        cnt=im2[max_index]
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        main_y = y    
        #print x,y,x+w,y+h

        #FIX: 0 check for a,b,c,d
        a = 120 - (2*y + h)/2
        b = (80 - (2*x + w)/2)
        area_flag = 1
        ang = math.fabs(b/2.5)
        cenx = (2*x + w )/2
        #print e
        #print (90-ang)
        if cenx <= 80:
           angle2 = (90+ang)
        else:
           angle2 = (90-ang)
        print int(angle2)
        #cv2.drawContours(img,cnt,-1,(0,255,0),1)
        diff = math.fabs(oldangle-angle2)
        if diff>=0:
           duty1 = int(angle2)/10 + 3
           oldangle=angle2
        #print (duty1)
        if harish!=duty1 and cross_area != 1:
           pwm.ChangeDutyCycle(duty1)
           harish = duty1
        #time.sleep(0.03)
        #resized = cv2.resize(img, (320, 240))
        #cv2.imshow("Show",img)

           
        k=cv2.waitKey(10)
        if k==27:
            break

vc.release()
cv2.destroyAllWindows()


    

