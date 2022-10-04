
from threading import Thread
from djitellopy import Tello
import cv2, math, time
import torch
import os
import numpy as np
import asyncio
import imutils
from PIL import Image
from matplotlib import pyplot as plt



class VideoStreamWidget(object):
    path = r'C:\yolov5-master'
    model = torch.hub.load(path, 'yolov5s',source='local', pretrained=True)

    def score_frame(self):
        #device = 'cuda' if torch.cuda.is_available() else 'cpu'
        #model.to(device)
        frame = cv2.imread('smol_Ina.jpg')
        wee = [torch.tensor(frame)]
        results = self.model(wee)
        labels = results.xyxyn[0][:, -1].numpy()
        cord = results.xyxyn[0][:, :-1].numpy()
        return labels, cord

    def plot_boxes(self, results, frame):
        labels, cord = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for i in range(n):
            row = cord[i]
            # If score is less than 0.2 we avoid making a prediction.
            if row[4] < 0.2: 
                continue
            x1 = int(row[0]*x_shape)
            y1 = int(row[1]*y_shape)
            x2 = int(row[2]*x_shape)
            y2 = int(row[3]*y_shape)
            bgr = (0, 255, 0) # color of the box
            classes = self.model.names # Get the name of label index
            label_font = cv2.FONT_HERSHEY_SIMPLEX #Font for the label.
            cv2.rectangle(frame,(x1, y1), (x2, y2),bgr, 2) #Plot the boxes
            cv2.putText(frame, classes[labels[i]], (x1, y1), label_font, 0.9, bgr, 2) #Put a label over box.
            return frame

    def __init__(self):
        #Below code creates a new video writer object to write our
        #output stream.
        #self.frame = cv2.cvtColor(frame_read.frame,cv2.COLOR_RGB2BGR)
        frame = cv2.imread('smol_Ina.jpg') # Read the first frame.
        x_shape = int(frame.shape[1])
        y_shape = int(frame.shape[0])
        results = self.score_frame() # Score the Frame
        frame = self.plot_boxes(results, frame) # Plot the boxes.
        cv2.imshow('object detection',frame)
        cv2.waitKey(0)


imgdet = VideoStreamWidget()


"""
tello = Tello()
tello.connect(False)
tello.streamon()
print(tello.get_udp_video_address())
print(type(tello.get_udp_video_address()))

bruh = tello.get_frame_read()



    print("while ing")
    while True:
        try:
        img = bruh.frame
        #img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        except KeyboardInterrupt:
            exit(1)
finally:
    print("fin")
"""


