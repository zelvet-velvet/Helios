

import numpy as np
import cv2
import time
import imutils


cap = cv2.VideoCapture(0)
skip_frame=500
player = cap
while skip_frame != 0:
	skip_buffer = player.read()
	skip_frame = skip_frame - 1
while True:
	ret, frame = player.read()
	frame = imutils.resize(frame,400)
	cv2.imshow("Zaviel on line",frame)
	cv2.waitKey(1)

