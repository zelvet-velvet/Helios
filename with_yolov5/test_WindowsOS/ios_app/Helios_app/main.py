
# app establishing import
from kivy.app import App
# file and window manager import
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import Config
# widget import
from kivy_garden.mapview import MapView
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.uix.button import Button
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
fall = False
hands_up = False


class UI_filter(Widget):
	pass

class Profile_page(Screen):
	pass

class Drone_page(Screen):
	pass
#	def on_pre_enter(self, *args):


class Stream_page(Screen):
	pass 
class Stream(Image):
	def __init__(self,  **kwargs):
		super(Stream, self).__init__(**kwargs)
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.port = 60050 
		socket_address = ('192.168.0.101', self.port)
		#socket_address = ('10.22.48.120',self.port)
		self.client_socket.bind(socket_address)
		print("Client binded")
		data = b""
		payload_size = struct.calcsize("Q")
		ip=('192.168.0.100',self.port)
		#ip=('10.22.75.87',self.port)
		#self.client_socket.sendto(b"ewe!",ip)
		Clock.schedule_interval_free(self.update, 0.017)
	
	def update(self, dt):
		global fall
		global hands_up
	
		packet,_ = self.client_socket.recvfrom(65536)
		if packet.decode() == "fall":
			fall = True
		if packet.decode() == "hands_up":
			hands_up = True
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
		Clock.schedule_interval_free(self.notice,3)
	def notice(self, dt):
		global fall
		global hands_up

		if fall:
			App.get_running_app().root.get_screen('list').notification_1.text = "Drn_3 fall warning !"
			App.get_running_app().root.get_screen('drone').ids.drn3_notice.source = "drawable/yellow_notice.png"
			App.get_running_app().root.get_screen('drone').ids.drn3_notice.size_hint_x = .1		
			
			App.get_running_app().root.get_screen('drone').ids.notice_drone.source = "drawable/red_notice.png"
			App.get_running_app().root.get_screen('drone').ids.notice_drone.size_hint_x = .06
			App.get_running_app().root.get_screen('list').ids.notice_drone.source = "drawable/red_notice.png"
			App.get_running_app().root.get_screen('list').ids.notice_drone.size_hint_x = .06
			App.get_running_app().root.get_screen('profile').ids.notice_drone.source = "drawable/red_notice.png"
			App.get_running_app().root.get_screen('profile').ids.notice_drone.size_hint_x = .06
			App.get_running_app().root.get_screen('map').ids.notice_drone.source = "drawable/red_notice.png"
			App.get_running_app().root.get_screen('map').ids.notice_drone.size_hint_x = .06
			App.get_running_app().root.get_screen('notification').ids.notice_drone.source = "drawable/red_notice.png"
			App.get_running_app().root.get_screen('notifacation').ids.notice_drone.size_hint_x = .06
		if hands_up:
			App.get_running_app().root.get_screen('list').notification_1.text = "Drn_3 hamds up warning !"
			App.get_running_app().root.get_screen('drone').ids.drn3_notice.source = "drawable/yellow_notice.png"
			App.get_running_app().root.get_screen('drone').ids.drn3_notice.size_hint_x = .06	
			
			App.get_running_app().root.get_screen('drone').ids.notice_drone.source = "drawable/yellow_notice.png"
			App.get_running_app().root.get_screen('drone').ids.notice_drone.size_hint_x = .1	
			App.get_running_app().root.get_screen('list').ids.notice_drone.source = "drawable/yellow_notice.png"
			App.get_running_app().root.get_screen('list').ids.notice_drone.size_hint_x = .1	
			App.get_running_app().root.get_screen('profile').ids.notice_drone.source = "drawable/yellow_notice.png"
			App.get_running_app().root.get_screen('profile').ids.notice_drone.size_hint_x = .1	
			App.get_running_app().root.get_screen('map').ids.notice_drone.source = "drawable/yellow_notice.png"
			App.get_running_app().root.get_screen('map').ids.notice_drone.size_hint_x = .1	
			App.get_running_app().root.get_screen('notification').ids.notice_drone.source = "drawable/yellow_notice.png"
			App.get_running_app().root.get_screen('notification').ids.notice_drone.size_hint_x = .1	
		
		"""
		global fall
		global hands_up
		img = Image(source='
		App.get_running_app().get_screen('drone').add_widget()
		if fall:
				
		if hands_up:
		"""


if __name__ == "__main__":
	main().run()


