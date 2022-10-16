# app establishing import
from kivy.app import App
# file and window manager import
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import Config
# widget import
from kivy.uix.widget import Widget
# screen stuff
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, NoTransition
from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder
# socket and stream processing stuff import
import socket
import cv2
import pickle
import struct
import imutils
import numpy as np
import base64
import sys
import time

class UI_filter(Widget):
	pass

class Profile_page(Screen):
	pass

class Drone_page(Screen):
	pass
class Stream_page(Screen):
	pass 

class RunnerList_page(Screen):
	pass

class Notifications_page(Screen):
	pass

class Map_page(Screen):
	pass


class ScreenManager(ScreenManager):
	pass

#kv = Builder.load_file("tt.kv")

class test(App):
	def build(self):
		Window.size = (321, 694.5)
		return 
if __name__ == "__main__":
	test().run()



