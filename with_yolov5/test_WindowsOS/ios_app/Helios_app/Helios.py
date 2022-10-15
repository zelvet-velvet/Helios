# app establishing import
from kivy.app import App
# layout import 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
# widget import
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
# file and window manager import
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import Config
	
import cv2
import imutils

Config.set('graphics', 'resizable', True)
Config.set('graphics', 'width', '321')
Config.set('graphics', 'height', '694.5')

#Builder.load_file("Homepage.kv")

class bottom_bar(BoxLayout):
	pass
	
class Homepage(RelativeLayout):
	def __init__(self, **var_args):	
		super(Homepage, self).__init__(**var_args)
		"""
		self.btn = Button(text ='',
			size_hint =(.2, .2),
			background_normal = '/drawable/middle.png')
		self.ids['middle_btn'] = self.btn
		"""

				
				
class Helios(App):
	def build(self):
		Window.size = (321, 694.5)
		return Homepage()

if __name__ == "__main__":
	Helios().run()

