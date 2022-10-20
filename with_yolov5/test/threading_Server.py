
#for stream processing
import torch
import numpy as np
import cv2
import time 
import sys
import av

#tello stuff
from djitellopy import Tello
import tellopy

#for socket estimating
import socket
import pickle
import struct
import imutils
import threading

#connecting with Tello-edu's to initialize object



import base64



output = ""

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
		self.model.conf = 0.5 # set inference threshold at 0.3
		self.model.iou = 0.4 # set inference IOU threshold at 0.3
		self.model.classes = [0] # set model to only detect "Person" class
		self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
		self.results = ""
	def get_video_from_file(self):
		"""
		Function creates a streaming object to read the video from the file frame by frame.
		:param self:  class object
		:return:  OpenCV object to stream video frame by frame.
   		"""
		drone = tellopy.Tello()
		drone.connect()
		drone.wait_for_connection(60.0)
		retry = 3
		self.container = None
		while self.container is None and 0 < retry:
			retry -= 1
			try:
				container = av.open(drone.get_video_stream())
			except av.AVError as ave:
				print(ave)
				print('retry...')
		assert container is not None
		print("Tello initialized successfully")
		return container.decode(video=0)

	def load_model(self):
		"""
		Function loads the yolo5 model from PyTorch Hub.
		"""
		path = r'/Applications/yolov5'
		model = torch.hub.load(path, 'yolov5n',source='local', pretrained=True)
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

	def modeling(self):
		while True:
			self.results = self.score_frame(self.frame)
			time.sleep(1)

	def __call__(self):
		player = self.get_video_from_file() # create streaming service for application
		#frame = player(frame)
		
		WIDTH =400
		frame_skip = 300
		for frame in player:	
			if 0 < frame_skip:
				frame_skip = frame_skip - 1
				continue
			break

		for frame in player:
			frame = cv2.cvtColor(np.array(frame.to_image()), cv2.COLOR_RGB2BGR)
			stream_modeling = threading.Thread(target = self.modeling)
			Server_processing = threading.Thread(target = Server_process)
			stream_modeling.daemon = True		
			self.frame = imutils.resize(frame,width=WIDTH)
			output=self.frame
			stream_modeling.start()
			Server_processing.start()
			time.sleep(2)
			break

		print("thread initialized")
	
		for frame in player:
			frame = cv2.cvtColor(np.array(frame.to_image()), cv2.COLOR_RGB2BGR)		
			self.frame = imutils.resize(frame,width=WIDTH)
			output = self.plot_boxes(self.results, self.frame)
			#cv2.imshow("ewe",self.frame)
			#cv2.waitKey(1)
			#print("ewe")

def Server_process():

	# Server socket
	# create an INET, STREAMing socket
	server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	host_name  = socket.gethostname()
	host_ip = socket.gethostbyname(host_name)

	print('HOST IP:',"192.168.0.101")
	port = 60050
	socket_address = ("192.168.0.101",port)
	print('Socket created')


	# bind the socket to the host. 
	#The values passed to bind() depend on the address family of the socket
	server_socket.bind(socket_address)
	print('Socket bind complete')
	#listen() enables a server to accept() connections
	#listen() has a backlog parameter. 
	#It specifies the number of unaccepted connections that the system will allow before refusing new connections.

	indata, Client_addr = server_socket.recvfrom(1024)
	while True:
		print('Connection from:',Client_addr)
		WIDTH=500
		while(vid.isOpened()):
			encoded,buffer = cv2.imencode('.jpg',output)
			message = base64.b64encode(buffer)
			server_socket.sendto(message,Client_addr)
			cv2.imshow('Sending...',frame)
			key = cv2.waitKey(10) 
			if key ==13:
				break		

if __name__ == "__main__":
	a = ObjectDetection()
	a()



