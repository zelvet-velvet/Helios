import torch
import torch
import numpy as np
import cv2
from time import time
import sys

cap = cv2.VideoCapture(0)
# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5n - yolov5x6, custom

# Images
img = 'https://ultralytics.com/images/zidane.jpg'  # or file, Path, PIL, OpenCV, numpy, list

"""
for ret in cap.read():
	assert ret,"nope"
	ret, frame = cap.read()
	# Inference
	results = model(frame)

	# Results
	results.print()
"""

ret, frame = cap.read()
results = model(frame)
results.print()
cv2.imshow("ewe",results)
cv2.waitKey(0)
