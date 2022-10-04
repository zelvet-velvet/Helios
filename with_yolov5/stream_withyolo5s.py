from threading import Thread
from djitellopy import Tello
import cv2, math, time
import torch
import os
path = r'C:\yolov5-master'
model = torch.hub.load(path, 'yolov5s',source='local', pretrained=True)
tello = Tello()
tello.connect(False)
#tello.takeoff()

#Tello.set_video_fps('FPS_30')
tello.streamon()
frame_read = tello.get_frame_read()


def move_forward():
    tello.move_forward(30)
def move_back():
    tello.move_back(30)
def move_left():
    tello.move_left(30)
def move_right():
    tello.move_right(30)
def rotate_clockwise():
    tello.rotate_clockwise(30)
def rotate_counter_clockwise():
    tello.rotate_counter_clockwise(30)
def move_up():
    tello.move_up(30)
def move_down():
    tello.move_down(30)
def takeoff():
    tello.takeoff()
def land():
    tello.land() 
    
class VideoStreamWidget(object):
    def __init__(self, src=0):
        #self.capture = cv2.VideoCapture(src)
        #self.capture = cv2.VideoCapture(tello.get_frame_read())
        
        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())######
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        # Read the next frame from the stream in a different thread
        global frame
        while True:
            #if self.capture.isOpened():
                #frame_read.frame
            #self.frame =  frame_read.frame

            self.frame = cv2.cvtColor(frame_read.frame,cv2.COLOR_RGB2BGR)

            #results = model(self.frame)
            #results.save()
            #(self.status, self.frame) = self.capture.read()
            time.sleep(.01)

    def show_frame(self):
        # Display frames in main program
        #fr=self.frame
        #img_bgr = cv2.cvtColor(self.frame,cv2.COLOR_RGB2BGR)
        #cv2.imshow('frame', self.frame)
        results = model(self.frame)
        results.save()
        i=os.listdir(r'C:\Python\Graduate_project\Tello\stream\with_yolov5\runs\detect')
        if len(i)==0:
            path2=r"C:\Python\Graduate_project\Tello\stream\with_yolov5\runs\detect\exp\image0.jpg"
        elif len(i)==1:
            path2=r"C:\Python\Graduate_project\Tello\stream\with_yolov5\runs\detect\exp\image0.jpg"
        else:
            path2=r"C:\Python\Graduate_project\Tello\stream\with_yolov5\runs\detect\exp"+str(len(i))+"\image0.jpg"
            
        #print(i,path2)
        img=cv2.imread(path2)

        cv2.imshow('frame', img)
        

if __name__ == '__main__':
    video_stream_widget = VideoStreamWidget()
    while True:
        try:
            video_stream_widget.show_frame()
            key = cv2.waitKey(1) & 0xff
            if key == ord('q'):
                #self.capture.release()
                Thread(target=land, args=()).start()
                cv2.destroyAllWindows()
                exit(1)
            elif key == ord('w'):
                Thread(target=move_forward, args=()).start()
            elif key == ord('s'):
                move_back(30)
                Thread(target=move_forward, args=()).start()
            elif key == ord('a'):
                move_left(30)
                Thread(target=move_forward, args=()).start()
            elif key == ord('d'):
                move_right(30)
                Thread(target=move_forward, args=()).start()
            elif key == ord('e'):
                Thread(target=rotate_clockwise, args=()).start()
            elif key == ord('q'):
                Thread(target=rotate_counter_clockwise, args=()).start()
            elif key == ord('r'):
                Thread(target=move_up, args=()).start()
            elif key == ord('f'):
                Thread(target=move_down, args=()).start()
            elif key == ord('t'):
                Thread(target=takeoff, args=()).start()
            elif key == ord('l'):
                Thread(target=land, args=()).start()
        except AttributeError:
            pass

