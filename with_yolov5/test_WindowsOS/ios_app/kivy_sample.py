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


class SayHello(App):
	def build(self):
		Config.set('kivy', 'kivy_clock', 'free_all')
		Config.getint('kivy', 'kivy_clock')
		#Config.write()
		#Clock.schedule_interval(self.a, 1)
		#CyClockBaseFree.create_trigger_free(self.a)
		#CyClockBaseFree.schedule_interval()
		#CyClockBaseFree.schedule_interval_free(self.a)	
		#Clock.schedule_once(self.a,0)
		#b=Clock.create_trigger(self.a)
				
		
	def a(self,dt):
		print("ewe")


if __name__ == "__main__":
	SayHello().run()




