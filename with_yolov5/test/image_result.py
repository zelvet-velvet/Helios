
#for stream processing
import torch
import numpy as np
import cv2
from time import time
import sys

#tello stuff
from djitellopy import TelloSwarm
from djitellopy import Tello

#for socket estimating
import socket
import pickle
import struct
import imutils
import threading



class ObjectDetection:
	"""
	The class performs generic object detection on a video file.
	It uses yolo5 pretrained model to make inferences and opencv2 to manage frames.
	Included Features:
	1. Reading and writing of video file using  Opencv2
	2. Using pretrained model to make inferences on frames.
	3. Use the inferences to plot boxes on objects along with labels.
	Upcoming Features:
	"""
	def __init__(self):
		"""
		:param input_file: provide youtube url which will act as input for the model.
		:param out_file: name of a existing file, or a new file in which to write the output.
		:return: void
		"""
		self.model = self.load_model()
		self.model.conf = 0.4 # set inference threshold at 0.3
		self.model.iou = 0.3 # set inference IOU threshold at 0.3
		self.model.classes = [0] # set model to only detect "Person" class
		self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

	def load_model(self):
		"""
		Function loads the yolo5 model from PyTorch Hub.
		"""
		path = r'/Applications/yolov5'
		model = torch.hub.load(path, 'yolov5s',source='local', pretrained=True)
		return model

	def score_frame(self, frame):
		"""
		function scores each frame of the video and returns results.
		:param frame: frame to be infered.
		:return: labels and coordinates of objects found.
		"""
		self.model.to(self.device)
		results = self.model([frame])
		labels, cord = results.xyxyn[0][:, -1].to('cpu').numpy(), results.xyxyn[0][:, :-1].to('cpu').numpy()
		return labels, cord

	def plot_boxes(self, results, frame):
		"""
		plots boxes and labels on frame.
		:param results: inferences made by model
		:param frame: frame on which to  make the plots
		:return: new frame with boxes and labels plotted.
		"""
		labels, cord = results
		n = len(labels)
		x_shape, y_shape = frame.shape[1], frame.shape[0]
		for i in range(n):
			row = cord[i]
			x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
			bgr = (0, 0, 255)
			cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 1)
			label = f"{int(row[4]*100)}"
			cv2.putText(frame, label, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
			cv2.putText(frame, f"Total Targets: {n}", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

		return frame

	def __call__(self):
		frame = cv2.imread("000000081988.jpg")	
		frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
		x_shape = int(frame.shape[0])
		y_shape = int(frame.shape[1])
		results = self.score_frame(frame)
		frame = self.plot_boxes(results, frame)
		labels, cord = results
		print(labels)
		print(cord)
		print(len(labels) == 0)
		cv2.imshow("ewe",frame)
		cv2.waitKey(0)


a = ObjectDetection()
a()


