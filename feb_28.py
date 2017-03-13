import RPi.GPIO as GPIO
import cv2
import math
import time
import numpy as np
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.OUT)
main_flag = 1
pwm = GPIO.PWM(18, 100)
pwm.start(5)
area_flag = 0
flag_90 = 0
vc=cv2.VideoCapture(0)
vc.set(3, 160)
vc.set(4, 120)
harish=0
retr= 0

cross_area = 0
oldangle=0
area_45 = 1
cross = 0  
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
    if areas == [] and area_flag == 1 and main_flag!=4:
     if main_flag == 1: 
         duty1 = int(60)/10 + 2.5
         pwm.ChangeDutyCycle(duty1)
         harish = duty1
         cross_area = 0
         print "main Flag passed ! "
         main_flag+=1
    if areas!=[] and main_flag!=4: 
        if main_flag == 2 and cross_area != 0:
           main_flag = 3 
        max_index = np.argmax(areas)
        print str(max(areas))
        if max(areas) > 2500:
           cross_area = 1
        cnt=im2[max_index]
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        main_y = y    
        #print x,y,x+w,y+h
        cv2.line(img,(((2*x+w)/2),y),(((2*x+w)/2),((2*y+h))),(255,0,0),2)
        cv2.line(img,(x,((2*y+h)/2)),(((x+w)),((2*y+h)/2)),(255,0,0),2)
        cv2.line(img,(80,0),(80,120),(255,0,255),2)
        cv2.line(img,(0,60),(160,60),(255,0,255),2)
        cv2.line(img,((2*x+w)/2,(2*y+h)/2),(80,120),(0,0,255),2)

            #FIX: 0 check for a,b,c,d
        a = 120 - (2*y + h)/2
        cv2.line(img, ((2*x + w)/2, (2*y + h)/2), (80, (2*y + h)/2), (50,50,50), 2) 
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
        cv2.drawContours(img,cnt,-1,(0,255,0),1)
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
        cv2.imshow("Show",img)
            
        k=cv2.waitKey(10)
        if k==27:
            break

vc.release()
cv2.destroyAllWindows()

