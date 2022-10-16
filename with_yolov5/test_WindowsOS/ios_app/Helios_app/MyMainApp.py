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
# screen stuff
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder


import cv2
import imutils

class MainWindow(Screen):
	pass


class SecondWindow(Screen):
	pass

class UI_filter(Widget):
	pass

class WindowManager(ScreenManager):
	pass


#kv = Builder.load_file("my.kv")


class MyMainApp(App):
	def build(self):
		Window.size = (321, 694.5)
		#return kv
		pass


if __name__ == "__main__":
	MyMainApp().run()
