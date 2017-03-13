import cv2
import math
import numpy as np
from matplotlib import pyplot as plt
vc=cv2.VideoCapture(0)

    
count=0
while(vc.isOpened()):
    #img=cv2.imread("2.png")
    ret,img=vc.read()
    cv2.imshow('Output',img)
    img2 =cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    x=200
    imgthreshold=cv2.inRange(img,cv2.cv.Scalar(x,x,x),cv2.cv.Scalar(255,255,255),)
    cv2.imshow('threshold',imgthreshold)
    
    
    edges=cv2.Canny(imgthreshold,100,200)
    cv2.imshow('Filter',edges)
    im2, hierarchy = cv2.findContours(imgthreshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


    areas = [cv2.contourArea(c) for c in im2]
    max_index = np.argmax(areas)
    cnt=im2[max_index]

    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    
    print x,y,x+w,y+h
    cv2.line(img,(((2*x+w)/2),y),(((2*x+w)/2),((2*y+h))),(255,0,0),5)
    cv2.line(img,(x,((2*y+h)/2)),(((x+w)),((2*y+h)/2)),(255,0,0),5)
    cv2.line(img,(320,0),(320,480),(255,0,255),5)
    cv2.line(img,(0,240),(640,240),(255,0,255),5)
    cv2.line(img,((2*x+w)/2,(2*y+h)/2),(320,480),(0,0,255),5)
    a=480-((2*y+h)/2)
    b=320-((2*x+w)/2)
    
    c=math.fabs(a)
    d=math.fabs(b)
    e=math.atan(d/c)
    print (e)
    cv2.drawContours(img,cnt,-1,(0,255,0),4)
    cv2.imshow("Show",img)
    
    k=cv2.waitKey(10)
    if k==27:
        break

vc.release()
cv2.destroyAllWindows()
