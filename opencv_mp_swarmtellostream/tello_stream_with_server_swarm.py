
#for stream processing
import sys
import traceback
import tellopy
import av
import cv2 
import numpy
import time
import PoseModule as pm

#for socket estimating
import socket
import pickle
import struct
import imutils
import threading

image = ""


#set up Tello-edu's static ip addr and call tellopy.Tello()
#from Swarm 
Tello1 = TelloSwarm.fromIps([
        "192.168.0.103"
])

def Server_estimate():

	server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	host_name  = socket.gethostname()
	host_ip = "192.168.0.101"
	#socket.gethostbyname(host_name)
	port = 60500


	print('HOST IP:', host_ip )
	socket_address = (host_ip, port)
	print('Socket created')
	

	server_socket.bind(socket_address)
	print('Socket bind complete')
	server_socket.listen(5)
	print('Socket now listening')


	while True:
		client_socket,addr = server_socket.accept()
		print('Connection from:',addr)
		if client_socket:
			for frame in s.container.decode(video=0):
				a = pickle.dumps(image)		
				message = struct.pack("Q",len(a))+a
				client_socket.sendall(message)
				#cv2.imshow('Sending...',image)
				#key = cv2.waitKey(10) 
				#if key ==13:	
				#	client_socket.close()
				time.sleep(0.2)

class Stream_Stuff():
	def __init__(self):
		# skip first 300 frames
		self.frame_skip = 400

	def tello_init(self):
		Tello1 = tellopy.Tello()
		try:
			Tello1.connect()
			Tello1.wait_for_connection(60.0)

			retry = 3
			self.container = None
			while self.container is None and 0 < retry:
				retry -= 1
				try:
					self.container = av.open(Tello1.get_video_stream())
				except av.AVError as ave:
					print(ave)
					print('retry...')
		except Exception as ex:
			exc_type, exc_value, exc_traceback = sys.exc_info()	
			traceback.print_exception(exc_type, exc_value, exc_traceback)		
			print(ex)
		print("Tello initialized successfully")


	def Stream_processing(self):
		global image
		detector = pm.poseDetector()
		try:
			for frame in self.container.decode(video=0):
				if 0 < self.frame_skip:
					self.frame_skip = self.frame_skip - 1
					continue
				start_time = time.time()	
				image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)	
				image = detector.findPose(image)
				lmList = detector.findPosition(image,draw=False)
				#cv2.imshow('Original', image) 
				cv2.waitKey(1)
				if frame.time_base < 1.0/60:
					time_base = 1.0/60
				else:
					time_base = frame.time_base
				self.frame_skip = int((time.time() - start_time)/time_base)
       	             						

		except Exception as ex:
			exc_type, exc_value, exc_traceback = sys.exc_info()	
			traceback.print_exception(exc_type, exc_value, exc_traceback)		
			print(ex)	
		finally:	
			Tello1.quit()	
			cv2.destroyAllWindows()


if __name__ == "__main__":
	#create class Stream_Stuff
	s = Stream_Stuff()

	s.tello_init()

	Stream_processing_thread = threading.Thread(target = s.Stream_processing)
	Server_processing_thread = threading.Thread(target = Server_estimate)

	Stream_processing_thread.start()
	i=1
	while(i==1):
		if image!="":
			Server_processing_thread.start()
			i-=1
			time.sleep(1)

