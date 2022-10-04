#importing GPIO code
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#pin 4 is switch

GPIO.setup(4, GPIO.IN)

#pin 27 is yellow output
GPIO.setup(27, GPIO.OUT)
GPIO.output(27, GPIO.LOW)

while True:
    if GPIO.input(4) == 1:
        GPIO.output(27, GPIO.HIGH)
    if GPIO.input(4)==0:
        GPIO.output(27, GPIO.LOW)

        