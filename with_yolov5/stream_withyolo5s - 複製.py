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


path = r'C:\yolov5-master'
model = torch.hub.load(path, 'yolov5s',source='local', pretrained=True)
tello = Tello()
tello.connect()
tello.streamon()

frame_read = tello.get_frame_read()
    
class VideoStreamWidget(object):
    """

    def __init__(self):
        # Start the thread to read frames from the video stream
        print("Initialized")
        self.thread = Thread(target=self.update, args=())######
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        # Read the next frame from the stream
        global frame
        print("processing update")
        while True:
            self.frame = cv2.cvtColor(frame_read.frame,cv2.COLOR_RGB2BGR)
            print("meow")
            time.sleep(.01)

    def show_frame(self): 
        # Display frames in main program
        wee = model(self.frame)

    
        arr = wee.datah().cpu().numpy()
        print("arr:")
        print(type(arr))
        
        img = Image.fromarray.fromarray(arr, 'RGB')
        print("img:")
        print(type(img))
        result = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
    
        cv2.imshow(  wee.permute(1, 2, 0)  )
        # cv2.imshow('frame', result)
        # F.to_pil_image(wee)
        key = cv2.waitKey(1)

    """
#################################################################


    def __init__(self):
        player = cv2.cvtColor(frame_read.frame,cv2.COLOR_RGB2BGR) #Get your video stream.
        #assert player.isOpened() # Make sure that their is a stream. 
        #Below code creates a new video writer object to write our
        #output stream.
        x_shape = int(player.shape[1])
        y_shape = int(player.shape[0]) 
        four_cc = cv2.VideoWriter_fourcc(*"MJPG") #Using MJPEG codex
        #out = cv2.VideoWriter('out_file', four_cc, 20, (x_shape, y_shape)) 
        frame = cv2.cvtColor(frame_read.frame,cv2.COLOR_RGB2BGR) # Read the first frame.
        while True: # Run until stream is out of frames
            start_time = time.time() # We would like to measure the FPS.
            results = self.score_frame(frame) # Score the Frame
            frame = self.plot_boxes(results, frame) # Plot the boxes.
            end_time = time.time()
            fps = 1/np.round(end_time - start_time, 3) #Measure the FPS.
            print(f"Frames Per Second : {fps}")
            cv2.imshow('frame', frame)# Write the frame onto the output.
            frame = cv2.cvtColor(frame_read.frame,cv2.COLOR_RGB2BGR) # Read next frame.

    def score_frame(frame,self):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        model.to(device)
        frame = [torch.tensor(frame)]
        results = model(frame)
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
            classes = self.model.names  # Get the name of label index
            label_font = cv2.FONT_HERSHEY_SIMPLEX #Font for the label.
            cv2.putText(frame, classes[labels[i]],  (x1, y1),  label_font, 0.9, bgr, 2) #Put a label over box.
            cv2.rectangle(frame,  (x1, y1), (x2, y2), bgr, 2)   #Plot the boxes
            return frame



#################################################################

if __name__ == '__main__':
    video_stream_widget = VideoStreamWidget()
    """
    while True:
        try:
            video_stream_widget.show_frame()
        except AttributeError:
            pass
    """
    time.sleep(1)

    
