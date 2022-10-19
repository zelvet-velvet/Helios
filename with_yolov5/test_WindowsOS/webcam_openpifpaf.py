
#for stream processing
import torch
import numpy as np
import cv2
import time
import sys
import random
import openpifpaf

#tello stuff
from djitellopy import TelloSwarm
from djitellopy import Tello

#for socket estimating
import socket
import pickle
import struct
import imutils
import threading
import base64


try:
	local_ip = sys.argv[1]
	if local_ip == "--help":
		print("usage: python3 webcam_openpifpaf.py [self_IP_addr]")
		exit()
except:
	print("error : missing local IP parameter")
	print("usage: python3 webcam_openpifpaf.py [self_IP_addr]")
	exit()

output = ""
player = ""
fall = False
hands_up = False

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
		self.predictor = self.load_model()
		self.predictions = ""
	def get_video_from_file(self):
		"""
		Function creates a streaming object to read the video from the file frame by frame.
		:param self:  class object
		:return:  OpenCV object to stream video frame by frame.
		"""
		cap = cv2.VideoCapture(0)
		assert cap is not None
		return cap

	def load_model(self):
		"""
		Function loads the yolo5 model from PyTorch Hub.
		"""
		# mobilenetv3small, mobilenetv3large, resnet50, shufflenetv2k16, shufflenetv2k30
		predictor = openpifpaf.Predictor(checkpoint='mobilenetv3small', json_data=True )
		return predictor

	def score_frame(self, frame):
		"""
		function scores each frame of the video and returns results.
		:param frame: frame to be infered.
		:return: labels and coordinates of objects found.
		"""	
		predictions, gt_anns, image_meta = self.predictor.numpy_image(frame)
		return predictions, gt_anns, image_meta

	def plot_boxes(self, predictions, ok):
		"""
		plots boxes and labels on frame.
		:param results: inferences made by model
		:param frame: frame on which to  make the plots
		:return: new frame with boxes and labels plotted.
		"""
		global fall
	        global hands_up	
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

			# set upper and lower body's datum point to detect if this person fall  
			face_datumpoint, body_datumpoint=-3,-3, 
			if kp[1]>0:
				face_datumpoint = int(kp[1])
			elif kp[4]>0 and kp[7]>0:
		        	face_datumpoint = (int(kp[4])+int(kp[7]))/2
			elif kp[13]>0 and kp[15]>0:
				face_datumpoint = (int(kp[13])+int(kp[15]))/2	

			if kp[34]>0 and kp[37]>0:
				body_datumpoint = ( int(kp[34]) + int(kp[37]) )/2 
			elif kp[40]>0 and kp[43]>0:
				body_datumpoint = ( int(kp[40]) + int(kp[43]) )/2 
			elif kp[46]>0 and kp[49]>0:
				body_datumpoint = ( int(kp[46]) + int(kp[49]) )/2 

			# detect if someone gonna fall down
			if abs( face_datumpoint - body_datumpoint ) < 10 and face_datumpoint!=-3 and body_datumpoint!=-3:
				# plot on red frame if this person fall								
				upl = int(bbox[0]), int(bbox[1])
				buttomr = int(bbox[0]+bbox[2]), int(bbox[1]+bbox[3])
				cv2.rectangle(box_filter, upl, buttomr, (0,0,255) , 1)		
				cv2.putText(box_filter,"Fall detected", (int(bbox[0]),int(bbox[1])-5), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,0,255), 1)	
				fall = True


			# set hands up pose detection
			hands  = -3
			if kp[22]>0 and kp[25]>0:
				hands = (int(kp[22])+int(kp[25]))/2
			if kp[28]>0 and kp[31]>0:
				hands = (int(kp[28])+int(kp[31]))/2

			if ( face_datumpoint - hands)  > 30 and hands!=-3:
				# plot on the frame if this person put her hands up
				upl = int(bbox[0])+2, int(bbox[1])+2
				buttomr = int(bbox[0]+bbox[2]), int(bbox[1]+bbox[3])
				cv2.rectangle(box_filter, upl, buttomr, (0,255,255) , 1)
				cv2.putText(box_filter,"Hands up", (int(bbox[0]),int(bbox[1])-5), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,255,255), 1)
				hands_up  = True	

		Transparency = 0.7
		ok = cv2.addWeighted(box_filter, Transparency, ok, 1 - Transparency, 0)

		return ok
	
	"""
	def runner_stop(self):
		runner_buffer = []
		while(True):
			for l in range(len(self.predictions)):
				bbox = predictions[l]["bbox"]
				try:
					if runner_buffer[l] = 


			if len(runner_buffer)<len(predictions):
				new_pp_index = len(predictions)-len(runner_buffer)
				bbox = predictions[l]["bbox"]
				runner_buffer[l].append(bbox[0],bbox[1])

	
	[0][1][2][3]
	[0][1][2]
	"""
			

	def modeling(self):
		while True:
			st = time.time()
			self.predictions, gt_anns, image_meta = self.score_frame(self.frame)
			et = time.time()
			elapsed_time = et - st
			#print('Execution time:', elapsed_time, 'seconds')

	def __call__(self):
		global player
		global output
		player = self.get_video_from_file() # create streaming service for application

		stream_modeling = threading.Thread(target = self.modeling)
		Server_processing = threading.Thread(target = Server_process)
		stream_modeling.daemon = True
		Server_processing.daemon = True

		#skip frame	
		skip_frame=300
		while skip_frame != 0:
			skip_buffer = player.read()
			skip_frame = skip_frame - 1

		ret, self.frame = player.read()
		stream_modeling.start()
		Server_processing.start()
		time.sleep(2)
		assert player.isOpened()

		WIDTH = 400
		while True:
			ret, frame = player.read()
			self.frame = imutils.resize(frame,width=WIDTH)
			if not ret:
				break
			output = self.plot_boxes(self.predictions, self.frame)
			local_show = imutils.resize(output, 1200)
			"""
			if fall:
				print("Warning!!! Warning!!!")
			"""
			cv2.imshow("ewe",local_show)
			cv2.waitKey(1)
		player.release()

def Server_process():

	global fall 
	global hands_up

	# Server socket
	# create an INET, STREAMing socket
	server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	host_name  = socket.gethostname()
	host_ip = socket.gethostbyname(host_name)

	print('Local IP:',local_ip)
	port = 60050
	socket_address = (local_ip,port)
	print('Socket created')


	# bind the socket to the host. 
	#The values passed to bind() depend on the address family of the socket
	server_socket.bind(socket_address)
	print('Socket bind complete')
	#listen() enables a server to accept() connections
	#listen() has a backlog parameter. 
	#It specifies the number of unaccepted connections that the system will allow before refusing new connections.
	print("Wait for Client response")
	indata, Client_addr = server_socket.recvfrom(1024)
	while True:
		print('Connection from:',Client_addr)
		while(player.isOpened()):
			if fall:
				server_socket.sendto("fall".encode(), Client_addr)
				print(fall)
				fall = False
			if hands_up:
				server_socket.sendto("hands_up".encode(), Client_addr)
				print(hands_up)
				hands_up = False

			encoded,buffer = cv2.imencode('.jpg',output)
			message = base64.b64encode(buffer)
			server_socket.sendto(message,Client_addr)



if __name__ == "__main__":
	a = ObjectDetection()
	a()


