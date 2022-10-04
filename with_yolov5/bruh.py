from threading import Thread
from djitellopy import Tello
import cv2, math, time
import os


tello = Tello()
tello.connect(False)
tello.streamon()
print(tello.get_udp_video_address())
print(type(tello.get_udp_video_address()))
cap = cv2.VideoCapture(tello.get_udp_video_address())
try:
    while True:
        img = cap.read()
        cv2.imshow('frame', img)
except KeyboardInterrupt:
    exit(1)
finally:
    print("fin")








