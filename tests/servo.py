import Adafruit_BBIO.GPIO as GPIO
import time

for i in range(4):
    GPIO.setup("P2_1", GPIO.OUT)

while True:
    for i in range(4):
        GPIO.output("P2_1", GPIO.HIGH)
        time.sleep(1)
    for i in range(4):
        GPIO.output("P2_1", GPIO.LOW)
        time.sleep(1)