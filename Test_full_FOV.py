from picamera import PiCamera
import time

camera = PiCamera(sensor_mode=3,resolution = (1920,1080))
time.sleep(2)

camera.capture("/home/pi/Desktop/TestFOVimg.jpg")
camera.capture("/home/pi/Desktop/TestFOVimg.jpg")
print("done")