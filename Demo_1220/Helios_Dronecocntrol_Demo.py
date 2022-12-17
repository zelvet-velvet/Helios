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
import tellopy

# socket estimating and sending data 
import socket
import pickle
import struct
import imutils
import threading


output = ""
player=""
fall = False
hands_up = False

class ObjectDetection:
	def __init__(self):
		self.predictor = self.load_model()
		self.predictions = ""
	def get_video_from_file(self):
		self.drone = tellopy.Tello()
		self.drone.connect()
		self.drone.wait_for_connection(60.0)
		retry = 3
		self.container = None
		while self.container is None and 0 < retry:
			retry -= 1
			try:
				container = av.open(self.drone.get_video_stream())
			except av.AVError as ave:
				print(ave)
				print('retry...')
		assert container is not None
		print("Tello initialized successfully")
		return container.decode(video=0)

	def load_model(self):
		# mobilenetv3small, mobilenetv3large, resnet50, shufflenetv2k16, shufflenetv2k30
		predictor = openpifpaf.Predictor(checkpoint='mobilenetv3large', json_data=True )
		return predictor

	def score_frame(self, frame):
		predictions, gt_anns, image_meta = self.predictor.numpy_image(frame)
		return predictions, gt_anns, image_meta

	def plot_boxes(self, predictions, ok):
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
			elif kp[10]>0 and kp[13]>0:
				face_datumpoint = (int(kp[10])+int(kp[13]))/2
			elif kp[16]>0 and kp[19]>0:
				face_datumpoint = (int(kp[16])+int(kp[19]))/2	


			if kp[34]>0 and kp[37]>0:
				body_datumpoint = ( int(kp[34]) + int(kp[37]) )/2 
			elif kp[40]>0 and kp[43]>0:
				body_datumpoint = ( int(kp[40]) + int(kp[43]) )/2 
			elif kp[46]>0 and kp[49]>0:
				body_datumpoint = ( int(kp[46]) + int(kp[49]) )/2 


			# detect if someone gonna fall down
			if abs( face_datumpoint - body_datumpoint ) < 30 and face_datumpoint!=-3 and body_datumpoint!=-3:
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

		return ok, fall

	def modeling(self):
		while True:
			self.predictions, gt_anns, image_meta = self.score_frame(self.frame)

			"""
			st = time.time()
			et = time.time()
			elapsed_time = et - st
			print('Execution time:', elapsed_time, 'seconds')
			"""
	def __call__(self):
		global player
		global output

		player = self.get_video_from_file() # create streaming service for application

		frame_skip = 300
		for frame in player:	
			if 0 < frame_skip:
				frame_skip = frame_skip - 1
				continue
			break

		WIDTH =400
		for frame in player:
			frame = cv2.cvtColor(np.array(frame.to_image()), cv2.COLOR_RGB2BGR)
			self.frame = imutils.resize(frame,width=WIDTH)
			output=self.frame

			stream_modeling = threading.Thread(target = self.modeling)
			#Server_processing = threading.Thread(target = Server_process)
			input_getting = threading.Thread(target = get_input)
			stream_modeling.daemon = True	
			#Server_processing.daemon = True	
			input_getting.daemon = True
			stream_modeling.start()
			#Server_processing.start()
			input_getting.start()
			time.sleep(2)
			break

		print("-------- Thread initialized --------")


		try:
			for frame in player:
				frame = cv2.cvtColor(np.array(frame.to_image()), cv2.COLOR_RGB2BGR)		
				self.frame = imutils.resize(frame,width=WIDTH)
				output, fall = self.plot_boxes(self.predictions, self.frame)
				"""
				if fall:
					print("Warning! Warning!")
				"""
				local_show = imutils.resize(output, 700)
				cv2.imshow("ewe",local_show)
				key = cv2.waitKey(1)
				if key == ord('g'):
					self.drone.land()
				if key == ord('t'):
					self.drone.takeoff()
				if key == ord('r'):
					self.drone.set_throttle(0.5)
				if key == ord('f'):
					self.drone.set_throttle(-0.5)
				if key == ord('e'):
					self.drone.set_yaw(0.5)
				if key == ord('q'):
					self.drone.set_yaw(-0.5)
				if key == ord('z'):
					self.drone.set_throttle(0)
					self.drone.set_yaw(0)
				if key == ord('x'):
					self.drone.set_throttle(0)
					self.drone.set_yaw(0)
					self.drone.land()
					time.sleep(2.5)
					exit()
		except SystemExit:
			self.drone.land()

sent = b""
def get_input():
	global sent
	while True:
		data = b""
		while not data:
			data = input().encode()
		sent = data


if __name__ == "__main__":
	a = ObjectDetection()
	a()



