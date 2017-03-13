import RPi.GPIO as GPIO
import cv2
import math
import time
import numpy as np
import Queue
import threading

exitFlag=0

class myThread (threading.Thread):
     def __init__(self,p0,p1,p2,i,d0,d1,d2):
       threading.Thread.__init__(self)
       self.p0=p0
       self.p1=p1
       self.p2=p2
       self.i=i
       self.d0=d0
       self.d1=d1
       self.d2=d2
     def run(self):
          i = 0.0
          while i <= 1:
              p = (1-i)*(1-i)*p0 + 2*i*(1-i)*p1 + i*i*p2
              p = int(p)
              print "p : " + str(p)
              i+=0.12
              duty1 = int(p)/10 + 2.5
              time.sleep(0.15)
              pwm.ChangeDutyCycle(duty1)
              #time.sleep(0.35)
          duty1=int(p2+90)/10 + 2.5
          pwm.ChangeDutyCycle(duty1)
          time.sleep(1)
          i=0.0
          while i <= 1:
              d = (1-i)*(1-i)*d0 + 2*i*(1-i)*d1 + i*i*d2
              d = int(d)
              i+=0.12
              time.sleep(0.15)
              print "d : " + str(d)
              duty1 = int(d)/10 + 2.5
              pwm.ChangeDutyCycle(duty1)
              #time.sleep(0.35) 
          print "Exiting Thread ! "
          exitFlag=0
          queue_ins=0
          

q=Queue.Queue()
q2 = Queue.Queue()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.OUT)

pwm = GPIO.PWM(18, 100)
pwm.start(5)
angleq=0
vc=cv2.VideoCapture(0)
vc.set(3, 160)
vc.set(4, 120)
harish=0
oldangle=0
queue_ins=0
qsize=0
framecount=0
while(vc.isOpened()):
    #img=cv2.imread("1.png")
    ret,imgi =vc.read()
    framecount+=1
    #cv2.imshow('Output',img)
    img = cv2.flip(imgi, 1)
    #img = cv2.flip(imgr, 1)
    img2 =cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    x=200
    imgthreshold=cv2.inRange(img,cv2.cv.Scalar(x,x,x),cv2.cv.Scalar(255,255,255),)
    #cv2.imshow('threshold',imgthreshold)
    
    
    edges=cv2.Canny(imgthreshold,100,200)
    #cv2.imshow('Filter',edges)
    im2, hierarchy = cv2.findContours(imgthreshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


    areas = [cv2.contourArea(c) for c in im2]
    #FIX: max_index will be null if argmax has no arguments

    if areas == []:
        queue_ctr=1
        sum=0
        sum2=0
        flag = False
        while not q.empty() and exitFlag==0:
              angleq = q.get()
              angleq2=q2.get()
              if queue_ctr == 1:
                 p0 = angleq
                 d0=angleq2
                 print "p0 : " + str(p0)
              elif queue_ctr == qsize:
                 p2 = angleq
                 d2 = angleq2
                 print "p2 : " + str(p2)
                 p1 = float(sum)/(qsize-2)
                 d1 = float(sum2)/(qsize-2)
                 print "p1 : " + str(p1) + "qsize : " + str(qsize)
              else:
                 sum+=angleq
                 sum2+=angleq2
                 #print "Angle inside else : " + str(sum)
              #print "Dequeue : "+str(angleq)
              queue_ctr+=1
              flag = True
        #p1=float(sum)/(qsize-2) 
        old_p = 0
        i=0.0
        if flag:
           thread1=myThread(p0,p1,p2,i,d0,d1,d2)
           if not thread1.isAlive():
              exitFlag=1
              thread1.start()
           print "KeepAlive : " + str(thread1.isAlive())
    else:
        max_index = np.argmax(areas)
        cnt=im2[max_index]
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            
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
        cenx = (2*x + w )/2
        c = math.fabs(a)
        d = math.fabs(b)
        e = math.atan(d/c)
        #print e
        angle1 = e*180/3.142857
        #print (90-angle1)
        if cenx <= 80:
           angle2 = 90+angle1
        else:
           angle2 = 90-angle1
        #print int(angle2)
        cv2.drawContours(img,cnt,-1,(0,255,0),1)
        diff = math.fabs(oldangle-angle2)
        if oldangle == 0:
           duty1 = int(angle2)/10 + 2.5
           oldangle=angle2
           pwm.ChangeDutyCycle(duty1)
        if diff>=1 and diff<=30 and exitFlag==0:
           duty1 = int(angle2)/10 + 2.5
           oldangle=angle2
           pwm.ChangeDutyCycle(duty1)
        #print (duty1)
        if diff>30 or queue_ins==1:
           q.put(int(angle2))
           q2.put(int(180-angle2))
           qsize+=1
           print int(angle2)
           queue_ins=1
        time.sleep(0.03)
        #resized = cv2.resize(img, (320, 240))
        cv2.imshow("Show",img)
            
        k=cv2.waitKey(10)
        if k==27:
            break

vc.release()
cv2.destroyAllWindows()

