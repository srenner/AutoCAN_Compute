import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

while True:
    GPIO.output(20, 0)
    GPIO.output(21, 0)
    time.sleep(5)

    GPIO.output(20, 1)
    GPIO.output(21, 0)
    time.sleep(5)

    GPIO.output(20, 0)
    GPIO.output(21, 1)
    time.sleep(5)
