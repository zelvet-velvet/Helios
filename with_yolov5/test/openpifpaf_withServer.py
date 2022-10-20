
# stream processing
import torch
import numpy as np
import cv2
import time 
import sys
import av
import random
import openpifpaf


# tello lib
from djitellopy import Tello
import tellopy

# socket estimating and sending data 
import socket
import pickle
import struct
import imutils
import threading
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
		self.predictor = openpifpaf.Predictor(checkpoint='resnet50', json_data=True )
		self.predictions = ""
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

	def plot_boxes(self, predictions, ok):
		"""
		plots boxes and labels on frame.
		:param results: inferences made by model
		:param frame: frame on which to  make the plots
		:return: new frame with boxes and labels plotted.
		"""
		fall = False
		box_filter = ok.copy()
		for l in range(len(predictions)):
			# the color of each person's body dot
			b, g, r = 255, 255, 255
			# list title 
			kp = predictions[l]["keypoints"] 
			bbox = predictions[l]["bbox"]
			# body line's width and color
			body_trunk = 4
			bgr_body = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

			face_bgr = (0, 0, 255)		#	
			neck_bgr = (255, 255, 255)	#
			body_bgr = (100, 255, 77)	#

			leftHand_bgr = (245, 0, 231)	#
			leftLeg_bgr = (194, 102, 255)	#
			rightHand_bgr = (149, 94, 255)	#
			rightLeg_bgr = (237, 101, 23)	#

			# --------------- Face ------------------	
			if kp[0] and kp[3]: # nose to left eye
				cv2.line(box_filter, (int(kp[0]),int(kp[1])), (int(kp[3]),int(kp[4])), face_bgr, body_trunk)	
			if kp[0] and kp[6]: # nose to right eye
				cv2.line(box_filter, (int(kp[0]),int(kp[1])), (int(kp[6]),int(kp[7])), face_bgr, body_trunk)	
			if kp[6] and kp[12]:# right eye to ear
				cv2.line(box_filter, (int(kp[6]),int(kp[7])), (int(kp[12]),int(kp[13])), face_bgr, body_trunk)	
			if kp[3] and kp[9]: # left eye to ear
				cv2.line(box_filter, (int(kp[3]),int(kp[4])), (int(kp[9]),int(kp[10])), face_bgr, body_trunk)	
			if kp[0] and kp[15]: # nose to left shoulder
				cv2.line(box_filter, (int(kp[0]),int(kp[1])), (int(kp[15]),int(kp[16])), neck_bgr, body_trunk)	
			if kp[0] and kp[18]: # nose to right shoulder 
				cv2.line(box_filter, (int(kp[0]),int(kp[1])), (int(kp[18]),int(kp[19])), neck_bgr, body_trunk)	
			# --------------- Face ------------------

			# --------------- Hands ------------------
			if kp[24] and kp[18]: # right elbow to shoulder
				cv2.line(box_filter, (int(kp[24]),int(kp[25])), (int(kp[18]),int(kp[19])), rightHand_bgr, body_trunk)	
			if kp[21] and kp[15]: # left elbow to shoulder 
				cv2.line(box_filter, (int(kp[21]),int(kp[22])), (int(kp[15]),int(kp[16])), leftHand_bgr, body_trunk)	
			if kp[24] and kp[30]: # right elbow to wrist
				cv2.line(box_filter, (int(kp[24]),int(kp[25])), (int(kp[30]),int(kp[31])), rightHand_bgr, body_trunk)	
			if kp[21] and kp[27]: # left elbow to wrist
				cv2.line(box_filter, (int(kp[21]),int(kp[22])), (int(kp[27]),int(kp[28])), leftHand_bgr, body_trunk)	
			# ---------------- Hands ------------------

			# ---------------- Body ------------------
			if kp[15] and kp[18]: # left shoulder to right shoulder 
				cv2.line(box_filter, (int(kp[15]),int(kp[16])), (int(kp[18]),int(kp[19])), body_bgr, body_trunk)
			if kp[18] and kp[36]: # right shoulder to hip 
				cv2.line(box_filter, (int(kp[36]),int(kp[37])), (int(kp[18]),int(kp[19])), body_bgr, body_trunk)	
			if kp[15] and kp[33]: # left shoulder to hip
				cv2.line(box_filter, (int(kp[15]),int(kp[16])), (int(kp[33]),int(kp[34])), body_bgr, body_trunk)	
			if kp[33] and kp[36]: # right hip to left hip 
				cv2.line(box_filter, (int(kp[33]),int(kp[34])), (int(kp[36]),int(kp[37])), body_bgr, body_trunk)	
			# ---------------- Body ------------------

			# ---------------- Legs ------------------
			if kp[36] and kp[42]: # right hip to knee 
				cv2.line(box_filter, (int(kp[36]),int(kp[37])), (int(kp[42]),int(kp[43])), rightLeg_bgr, body_trunk)	
			if kp[33] and kp[39]: # left hip to knee
				cv2.line(box_filter, (int(kp[33]),int(kp[34])), (int(kp[39]),int(kp[40])), leftLeg_bgr, body_trunk)	
			if kp[42] and kp[48]: # right knee to right ankle  
				cv2.line(box_filter, (int(kp[42]),int(kp[43])), (int(kp[48]),int(kp[49])), rightLeg_bgr, body_trunk)	
			if kp[39] and kp[45]: # left knee to ankle  
				cv2.line(box_filter, (int(kp[39]),int(kp[40])), (int(kp[45]),int(kp[46])), leftLeg_bgr, body_trunk)
			# ---------------- Legs ------------------

			# plot the body parts' dot 
			i=0
			while i<(len(kp)):
				cv2.circle(box_filter,(int(kp[i]), int(kp[i+1])), 2, (b, g, r), -1)
				i=i+3

			# detect if someone gonna fall down
			if abs( int(kp[1]) - ( int(kp[34]) + int(kp[37]) )/2 ) < 20:
				# plot the frame of this person
				upl = int(bbox[0]), int(bbox[1])
				buttomr = int(bbox[0]+bbox[2]), int(bbox[1]+bbox[3])
				cv2.rectangle(box_filter, upl, buttomr, (0,0,255) , 1)		
				cv2.putText(box_filter,"!!!Fall detected!!!", (int(bbox[0]),int(bbox[1])-5), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,0,255), 1)	
				fall = True
		Transparency = 0.7
		ok = cv2.addWeighted(box_filter, Transparency, ok, 1 - Transparency, 0)

		return ok, fall

	def modeling(self):
		while True:
			self.predictions, gt_anns, image_meta = predictor.numpy_image(output)

	def __call__(self):
		player = self.get_video_from_file() # create streaming service for application
		
		WIDTH =400
		frame_skip = 300
		for frame in player:	
			if 0 < frame_skip:
				frame_skip = frame_skip - 1
				continue
			break
		with frame in player:
			frame = cv2.cvtColor(np.array(frame.to_image()), cv2.COLOR_RGB2BGR)
			stream_modeling = threading.Thread(target = self.modeling)
			Server_processing = threading.Thread(target = Server_process)
			stream_modeling.daemon = True		
			self.frame = imutils.resize(frame,width=WIDTH)
			output=self.frame
			stream_modeling.start()
			Server_processing.start()
			time.sleep(2)

		print("-------- Thread initialized --------")
	
		for frame in player:
			frame = cv2.cvtColor(np.array(frame.to_image()), cv2.COLOR_RGB2BGR)		
			self.frame = imutils.resize(frame,width=WIDTH)
			output, fall = self.plot_boxes(self.results, self.frame)
			if fall:
				print("Warning! Warning!")
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



