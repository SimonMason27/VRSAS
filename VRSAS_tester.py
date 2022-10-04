#most importantly for this code to run is to import OpenCV
import cv2
import csv

#timing function
import time

#adding time and date stuff and rearranging it
from datetime import date, datetime
today = date.today()
date = today.strftime("%d-%b-%Y")
now = datetime.now()
timeRN = now.strftime("%H:%M:%S")
start = time.process_time()
finish = time.process_time()

# set up camera object called Cap which we will use to find OpenCV
cap = cv2.VideoCapture(0)

# QR code detection Method


#This creates an Infinite loop to keep your

#configs
#frameheight = int(cap.get(4))
#framewidth = int(cap.get(3))
#size = (framewidth, framewidth)
#below is a frame writer
fps = 20
ret,frame = cap.read()
height, width, channels = frame.shape
result = cv2.VideoWriter('/home/pi/Desktop/opened_%s_%s.avi' %(date, timeRN),cv2.VideoWriter_fourcc(*"XVID"), float(fps), (width, height))
#camera searching for data when the box is closed

while (finish-start)<5:
    ret,frame = cap.read()

#    if len(frame.shape)>2 and frame.shape[2]==4:
#        frame = cv2.cvtColor(img,cv2.COLOR_BGRA2BGRA)
    if ret:
        result.write(frame)
        cv2.imshow('Frame',frame)
        
    finish = time.process_time()
    
    if (cv2.waitKey(1) == ord('q')):    
        break

#5 seconds has passed
cap.release()
result.release()
cv2.destroyAllWindows()

            
