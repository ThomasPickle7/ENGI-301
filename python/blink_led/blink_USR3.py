import Adafruit_BBIO.GPIO as GPIO
import time


GPIO.setup("USR3", GPIO.OUT)

while True:
    GPIO.output("USR3", GPIO.HIGH)
    time.sleep(.1)
    GPIO.output("USR3", GPIO.LOW)
    time.sleep(.1)