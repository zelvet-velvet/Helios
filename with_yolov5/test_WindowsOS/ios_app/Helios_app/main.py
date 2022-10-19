# app establishing import
from kivy.app import App
# file and window manager import
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import Config
# widget import
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
# screen stuff
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, NoTransition
from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder
# socket and stream processing stuff import
from kivy.clock import Clock
from kivy.clock import CyClockBaseFree
import socket
import cv2
import pickle
import struct
import imutils
import numpy as np
import base64
import sys
import time


stream_on = False

class UI_filter(Widget):
	pass

class Profile_page(Screen):
	pass

class Drone_page(Screen):
	pass
class Stream_page(Screen):
	pass 
class Stream(Image):
	def __init__(self,  **kwargs):
		super(Stream, self).__init__(**kwargs)
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.port = 60050 
		socket_address = ('192.168.0.101', self.port)
		self.client_socket.bind(socket_address)
		print("Client binded")
		data = b""
		payload_size = struct.calcsize("Q")
		ip=('192.168.0.100',self.port)
		#self.client_socket.sendto(b"ewe!",ip)
		Clock.schedule_interval_free(self.update, 0.017)
	def update(self, dt):
		packet,_ = self.client_socket.recvfrom(65536)
		if packet.decode() == "fall":
			print("fall")		
		if packet.decode() == "hands_up":
			print("hands_up")
		else:
			start_time = time.time()
			data = base64.b64decode(packet,' /')
			npdata = np.frombuffer(data,dtype=np.uint8)
			frame = cv2.imdecode(npdata,1)
			frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
			frame = imutils.resize(frame, 1200)
			buf1 = cv2.flip(frame, 0)
			buf = buf1.tobytes()
			image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
			image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
			# display image from the texture
			self.texture = image_texture
			#print("FPS: ", 1.0 / (time.time() - start_time)) # FPS = 1 / time to process loop

class RunnerList_page(Screen):
	pass

class Notifications_page(Screen):
	pass

class Map_page(Screen):
	pass


class ScreenManager(ScreenManager):
	pass




class main(App):
	def build(self):
		Config.set('kivy', 'kivy_clock', 'free_all')
		Window.size = (321, 694.5)
		pass
	#def on_stop(self):

if __name__ == "__main__":
	main().run()



