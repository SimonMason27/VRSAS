#most importantly for this code to run is to import OpenCV
import cv2
import csv
import argparse
import imutils
from pyzbar import pyzbar
from imutils.video import VideoStream

#import code for checking the internet access
import urllib.request
#import code to run the sync file to the Onedrive
import subprocess

#importing GPIO code
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#pin 4 is the switch
GPIO.setup(4, GPIO.IN)
#pin 27 is yellow output
GPIO.setup(27, GPIO.OUT)
#GPIO.output(27, 1)

#starts as a closed system
closed = False
opened = False
previous_state = 1
current_state=0 

#adding time and date stuff and rearranging it
from datetime import date, datetime
import time
today = date.today()
date = today.strftime("%d-%b-%Y")
now = datetime.now()
timeRN = now.strftime("%H:%M:%S")
start = time.process_time()
finish = time.process_time()
delete_timer= time.process_time()

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
	help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())
fps = 20

#This creates an Infinite loop to keep the program running always
while True:
        current_time = time.process_time()
        #Uploads and then wipes the local content every (x) amount of seconds. Allows for a buffer before deleting local storage
        if current_time- delete_timer > 1200:# Has to buffer for 5 mins of power off, do 20 mins for safety    

	    def connect(host='https://www.microsoft.com/en-za/microsoft-365/onedrive/online-cloud-storage'):
    		try:
		#different between python 2 and python 3
        	urllib.request.urlopen(host)
        		return True
    		except:
        		return False
	    if connect():
		print("[INFO] uploading data to cloud...")            	
		subprocess.run("/home/pi/Documents/sync_Images_from_Pi.sh", shell=True)
            	subprocess.run("/home/pi/Documents/sync_Videos_from_Pi.sh", shell=True)
		print("[INFO] clearing local storage...")
            	subprocess.run("/home/pi/Documents/wipe_Images_from_Pi.sh", shell=True)
            	subprocess.run("/home/pi/Documents/wipe_Videos_from_Pi.sh", shell=True)
		delete_timer = time.process_time()
	    #else carry on

            
    #detect a change of state from high to low or low to high with opening and closing the box
    #(set close and open flag)
        current_state = GPIO.input(4)
        if previous_state == current_state:
            opened = False
            closed = False
        if previous_state == 1 and current_state==0:
            opened = False
            closed = True
        if previous_state == 0 and current_state==1:
            opened = True
            closed = False  
 
        if opened:
            #Start the capture
            cap = cv2.VideoCapture(0)

            #below is a frame writer using OpenCV
            now = datetime.now()
            timeRN = now.strftime("%H:%M:%S")
            result = cv2.VideoWriter('/home/pi/Documents/Videos_from_Pi/opened_%s_%s.avi' %(date, timeRN),cv2.VideoWriter_fourcc(*"XVID"), float(fps), (int(cap.get(3)), int(cap.get(4))))
            start = time.process_time()
            finish = time.process_time()
            print("[INFO] starting video stream...")

            #camera searching for data when the box is closed
            while finish-start<5:
                ret,frame = cap.read()
                if ret:
                    result.write(frame)
                    cv2.imshow('Frame',frame)
                    if (cv2.waitKey(1) == ord('q')):   #check 
                        break
                finish = time.process_time()
            print("[INFO] writing video...")

            #5 seconds has passed
            cv2.destroyAllWindows()
            cap.release()
            result.release()
            print("[INFO] uploading video stream to cloud...")
	    def connect(host='https://www.microsoft.com/en-za/microsoft-365/onedrive/online-cloud-storage'):
    		try:
		#different between python 2 and python 3
        	urllib.request.urlopen(host)
        		return True
    		except:
        		return False
	    if connect():
            	subprocess.run("/home/pi/Documents/sync_Videos_from_Pi.sh", shell=True)
		#else carry on

        if closed:
            #Turn on the LEDs for controlled lighting
            GPIO.output(27, 1)
            # initialize the video stream and allow the camera sensor to warm up
            vs = VideoStream(usePiCamera=True,  resolution = (1648, 1232)).start()
            print("[INFO] camera warming up...")
            time.sleep(2.0)
            start = time.process_time()e
            finish = time.process_time()
            print("[INFO] starting QR scanner...")

            #camera searching for data when the box is opened (maybe change to 10 seconds)
            while finish-start<5:
                frame = vs.read()
                frame = imutils.resize(frame, width = 1648)
                # find the barcodes in the frame and decode each of the barcodes
                barcodes = pyzbar.decode(frame)
                
                # extract the bounding box location of each barcode and draw the bounding box surrounding the barcode on the image
                for barcode in barcodes:
                    (x, y, w, h) = barcode.rect
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    # the barcode data is a bytes object so if we want to draw it on our output image we need to convert
                    #it to a string first
                    barcodeData = barcode.data.decode("utf-8")
                    barcodeType = barcode.type
                    # draw the barcode data and barcode type on the image
                    text = "{} ({})".format(barcodeData, barcodeType)
                    cv2.putText(frame, text, (x, y - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    # write the timestamp + barcode to disk and update the set

                    print("data found: ", barcodeData, date, timeRN)
                    with open('/home/pi/Documents/Data_from_Pi/Database_%s.csv' %date, mode='a') as csvfile:
                        #get most recent time
                        now = datetime.now()
                        timeRN = now.strftime("%H:%M:%S")
                        csvfileWriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                        csvfileWriter.writerow([barcodeData, date, timeRN]) 
   
                #get most recent time
                now = datetime.now()
                timeRN = now.strftime("%H:%M:%S")
                cv2.imwrite('/home/pi/Documents/Images_from_Pi/%s_%s.png' %(date, timeRN),frame)
                finish = time.process_time()

                # Below will display the live camera feed to the Desktop on Raspberry Pi OS preview
                cv2.imshow("Barcode Scanner", frame)
                if (cv2.waitKey(1) == ord('q')): #check   
                    break
            #end of while
            GPIO.output(27, 0)
            cv2.destroyAllWindows()
            vs.stop()
	    
	    def connect(host='https://www.microsoft.com/en-za/microsoft-365/onedrive/online-cloud-storage'):
    		try:
		#different between python 2 and python 3
        	urllib.request.urlopen(host)
        		return True
    		except:
        		return False
	    if connect():
            	print("[INFO] uploading data to cloud...")
            	subprocess.run("/home/pi/Documents/sync_Data_from_Pi.sh", shell=True)
            	print("[INFO] uploading images to cloud...")
            	subprocess.run("/home/pi/Documents/sync_Images_from_Pi.sh", shell=True)
            #else carry on
        #sent the new current state as the previous state
        previous_state = current_state
    #end the entire programs loop if q is pressed
        if (cv2.waitKey(1) == ord('q')):    
            break
# When the code is stopped the below closes all the applications/windows that the above has created
cap.release()
cv2.destroyAllWindows()
