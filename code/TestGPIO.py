import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#map gpio pins to the port on BOYO VTSW4 video splitter
VIDEO_2 = 21
VIDEO_3 = 20
VIDEO_4 = 16

GPIO.setup(VIDEO_2, GPIO.OUT) #connected to BOYO VTSW4 output 2
GPIO.setup(VIDEO_3, GPIO.OUT) #connected to BOYO VTSW4 output 3
GPIO.setup(VIDEO_4, GPIO.OUT) #connected to BOYO VTSW4 output 4

while True:
    GPIO.output(VIDEO_2, 0)
    GPIO.output(VIDEO_3, 0)
    GPIO.output(VIDEO_4, 0)

    time.sleep(5)

    GPIO.output(VIDEO_2, 1)
    GPIO.output(VIDEO_3, 0)
    GPIO.output(VIDEO_4, 0)

    time.sleep(5)

    GPIO.output(VIDEO_2, 0)
    GPIO.output(VIDEO_3, 1)
    GPIO.output(VIDEO_4, 0)

    time.sleep(5)

    GPIO.output(VIDEO_2, 0)
    GPIO.output(VIDEO_3, 0)
    GPIO.output(VIDEO_4, 1)

    time.sleep(5)
