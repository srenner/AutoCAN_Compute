# test3

#import pyscreenshot as ImageGrab
#im = ImageGrab.grab()
#im.save("fullscreen.png")

import cv2
import time

camera = cv2.VideoCapture(0)
for i in range(100):
	return_value, image = camera.read()
	cv2.imwrite('screenshot'+str(i)+'.png', image)
del(camera)
