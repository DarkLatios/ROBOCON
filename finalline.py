# import the necessary packages
from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100,
	help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1,
	help="Whether or not frames should be displayed")
args = vars(ap.parse_args())

# grab a pointer to the video stream and initialize the FPS counter
print("[INFO] sampling frames from webcam...")
stream = cv2.VideoCapture(0)
fps = FPS().start()

# loop over some frames
while fps._numFrames < args["num_frames"]:
	# grab the frame from the stream and resize it to have a maximum
	# width of 400 pixels
	(grabbed, frame) = stream.read()
	frame = imutils.resize(frame, width=400)

	# check to see if the frame should be displayed to our screen
	if args["display"] > 0:
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

	# update the FPS counter
	fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
stream.release()
cv2.destroyAllWindows()

# created a *threaded* video stream, allow the camera sensor to warmup,
# and start the FPS counter
print("[INFO] sampling THREADED frames from webcam...")
vs = WebcamVideoStream(src=0).start()
fps = FPS().start()

# loop over some frames...this time using the threaded stream
while fps._numFrames < args["num_frames"]:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
    ret,imgi =vs.read()
    #cv2.imshow('Output',img)
    imgr = cv2.flip(imgi, 1)
    img = cv2.flip(imgr, 1)
    img2 =cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    x=150
    imgthreshold=cv2.inRange(img,cv2.cv.Scalar(x,x,x),cv2.cv.Scalar(255,255,255),)
    #cv2.imshow('threshold',imgthreshold)
    
    
    edges=cv2.Canny(imgthreshold,100,200)
    #cv2.imshow('Filter',edges)
    im2, hierarchy = cv2.findContours(imgthreshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


    areas = [cv2.contourArea(c) for c in im2]
    #FIX: max_index will be null if argmax has no arguments


    if areas!=[]:
        max_index = np.argmax(areas)
        cnt=im2[max_index]
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            
        #print x,y,x+w,y+h
        cv2.line(img,(((2*x+w)/2),y),(((2*x+w)/2),((2*y+h))),(255,0,0),5)
        cv2.line(img,(x,((2*y+h)/2)),(((x+w)),((2*y+h)/2)),(255,0,0),5)
        cv2.line(img,(320,0),(320,480),(255,0,255),5)
        cv2.line(img,(0,240),(640,240),(255,0,255),5)
        cv2.line(img,((2*x+w)/2,(2*y+h)/2),(320,480),(0,0,255),5)

            #FIX: 0 check for a,b,c,d
        a=360-((2*y+h)/2)
        b=320-((2*x+w)/2)

        if math.fabs(a)==0:
            c=1
        else:
            c=math.fabs(a)

        if math.fabs(b)==0:
            d=1
        else:
            d=math.fabs(b)

        e=math.atan(d/c)
        print (e)

        cv2.drawContours(img,cnt,-1,(0,255,0),4)
        resized = cv2.resize(img, (320, 240))
        cv2.imshow("Show",resized)
            
        k=cv2.waitKey(10)
        if k==27:
            break
    fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
