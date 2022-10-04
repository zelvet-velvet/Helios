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


tello = Tello()
tello.connect()
tello.streamon()

frame_read = tello.get_frame_read()

class VideoStreamWidget(object):
    path = r'C:\yolov5-master'
    model = torch.hub.load(path, 'yolov5s',source='local', pretrained=True)
    def update(self):
        global frame
        while True:
            self.frame = cv2.cvtColor(frame_read.frame,cv2.COLOR_RGB2BGR)
            print("meow")
            time.sleep(.01)

    def score_frame(frame, model):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        model.to(device)
        frame = [torch.tensor(frame)]
        results = self.model(frame)
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
        self.thread = Thread(target=self.update, args=())######
        self.thread.daemon = True
        self.thread.start()
        player = cv2.cvtColor(frame_read.frame,cv2.COLOR_RGB2BGR)
        #Below code creates a new video writer object to write our
        #output stream.
        x_shape = int(player.get(cv2.CAP_PROP_FRAME_WIDTH))
        y_shape = int(player.get(cv2.CAP_PROP_FRAME_HEIGHT))
        #four_cc = cv2.VideoWriter_fourcc(*"MJPG") #Using MJPEG codex
        #out = cv2.VideoWriter(out_file, four_cc, 20, (x_shape, y_shape)) 
        frame = frame_read.frame # Read the first frame.
        while True: 
            start_time = time() # We would like to measure the FPS.
            results = self.score_frame(frame) # Score the Frame
            frame = self.plot_boxes(results, frame) # Plot the boxes.
            end_time = time()
            fps = 1/np.round(end_time - start_time, 3) #Measure the FPS.
            print(f"Frames Per Second : {fps}")
            #out.write(frame) # Write the frame onto the output.
            cv2.imshow('object detection',frame)
            frame = frame_read.frame # Read next frame.

if __name__ == '__main__':
    video_stream_widget = VideoStreamWidget()
    time.sleep(1)
