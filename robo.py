#CREATED BY ADITYA SRIVASTAVA TECHNICAL DEVELOPER FOR ROBOCON 2016.
import cv2
import sys
import os
import time
sys.path.append("../..")
import multiprocessing
from classifier import NearestNeighbor
from model import PredictableModel
from feature import Fisherfaces
from PIL import Image
import scipy
from util import asRowMatrix
import numpy as np
import logging
import matplotlib.cm as cm
import pyttsx
engine=pyttsx.init()

engine.say('Hello SID,Welcome to the future,I am part of Romeos network')
engine.runAndWait()
engine.say('use this code no issues,there are a few bugs in me hope You will correct me')
engine.runAndWait()
model = PredictableModel(Fisherfaces(), NearestNeighbor())
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
recognizer = cv2.createLBPHFaceRecognizer()
video_capture = cv2.VideoCapture(0)




def read_images(path, sz=(256,256)):
    
    
    X,y = [], []
    folder_names = []
    default='Unknown'
    for dirname, dirnames, filenames in os.walk(path):
        for subdirname in dirnames:
            default='Unknown'
            folder_names.append(subdirname)
            subject_path = os.path.join(dirname, subdirname)
            for filenames in os.listdir(subject_path):
                try:
                    im = cv2.imread(os.path.join(subject_path, filenames), cv2.IMREAD_GRAYSCALE)
                    nbr = int(os.path.split(filenames)[1].split(".")[0].replace("Image", ""))
                    # resize to given size (if given)
                    if (sz is not None):
                        im = cv2.resize(im, sz)
                    X.append(np.asarray(im, dtype=np.uint8))
                    y.append(nbr)
                except IOError, (errno, strerror):
                    print "I/O error({0}): {1}".format(errno, strerror)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    raise
                nbr=nbr+1
        
    return [X,y,folder_names]

    
    

pathdir='C:\Users\user\Desktop\Trained Images/'
engine.say('How many are you in front of the webcam,Please type below')
engine.runAndWait()

quanti = int(raw_input('Number:'))
for i in range(quanti):
    engine.say('HELLO USER '+str(i+1)+' what is your name?')
    engine.runAndWait()
    nome = raw_input('Name:')
    if not os.path.exists(pathdir+nome): os.makedirs(pathdir+nome)
    engine.say(str(nome)+'Collecting Specimens,Please Look At me!!!! ')
    engine.runAndWait()
    while (1):
        ret,frame = video_capture.read(0)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 3)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.imshow('Recognition',frame)

        
        if cv2.waitKey(10) == ord('s'):
            break
    cv2.destroyAllWindows()




    
    start = time.time()
    count = 0
    count2=0
    while int(time.time()-start) <=2:
        
        ret,frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 3)
        for (x,y,w,h) in faces:
            cv2.putText(frame,'Click!', (x,y), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,250),3,1)
            count +=1
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            resized_image = cv2.resize(frame[y:y+h,x:x+w], (256, 256))
            if count%5 == 0:
                print  (pathdir+nome+str(count2)+'.jpg')
                cv2.imwrite( pathdir+nome+'/'+str(count2)+'.jpg', resized_image );
                count2+=1
        cv2.imshow('Recognition',frame)
        cv2.waitKey(10)
    cv2.destroyAllWindows()

engine.say('Training Has Begun')
engine.runAndWait()
path='C:\Users\user\Desktop\Trained Images/'
[X,y,folder_names] = read_images(path, sz=(256,256))
list_of_labels = list(xrange(max(y)+1))
subject_dictionary = dict(zip(list_of_labels,folder_names))
recognizer.train(X, np.array(y))
recognizer.save('C:\Users\user\Desktop\Trained Images\LBPH.yml')
engine.say('Training Has Finished Successfully')
engine.runAndWait()


                      

while (1):
    rval, frame = video_capture.read()
    recognizer.load('C:\Users\user\Desktop\Trained Images\LBPH.yml')
    img = frame
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.2, 3)

    for (x,y,w,h) in faces:
        try:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            [predicted_label, confidence] = recognizer.predict(gray[y:y+h, x:x+w])
            print [predicted_label, confidence]
            if confidence<=100.00:
                cv2.putText(img,'YOU ARE : '+str(subject_dictionary[predicted_label]), (x,y), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,250),3,1)
                engine.say('HELLO' + str(subject_dictionary[predicted_label]))
                engine.runAndWait()
        except KeyError:
            pass
    cv2.imshow('result',img)
    if cv2.waitKey(10) == 27:
        break

         
        


video_capture.release()
cv2.destroyAllWindows()
