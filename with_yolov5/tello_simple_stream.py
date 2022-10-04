import asyncio
from threading import Thread
import cv2  
from tello_asyncio import Tello, VIDEO_URL
#from djitellopy import Tello
import asyncio





def fly():
    async def main():
        drone = Tello()
        try:
            await drone.connect()
            await drone.start_video()
        except KeyboardInterrupt:
            pass
        finally:
            await drone.stop_video()
            await drone.disconnect()

    asyncio.run(main())

fly_thread = Thread(target=fly, daemon=True)
fly_thread.start()


capture = cv2.VideoCapture(VIDEO_URL)
capture.open(VIDEO_URL)

while True:
    grabbed, frame = capture.read()
    if grabbed:
        cv2.imshow('tello-asyncio', frame)
    if cv2.waitKey(1) != -1:
        break

capture.release()
cv2.destroyAllWindows()


##################################################

"""
#variables setting
global axis_spd 
global yaw_spd

axis_spd = 100
yaw_spd = 80
hieght_spd = 100


def takeoff():
    tello.takeoff()
    pass
def land():
    tello.land()
    pass
def move_forward():
    tello.send_rc_control(0,axis_spd,0,0)
    pass
def move_back():
    tello.send_rc_control(0,-axis_spd,0,0)
    pass
def move_left():
    tello.send_rc_control(axis_spd*-1,0,0,0)
    pass
def move_right():
    tello.send_rc_control(axis_spd,0,0,0)
    pass
def rotate_clockwise():
    tello.send_rc_control(0,0,0,-yaw_spd)
    pass
def rotate_counter_clockwise():
    tello.send_rc_control(0,0,0,yaw_spd)
    pass
def move_up():
    tello.send_rc_control(0,0,hieght_spd,0)
    pass
def move_down():
    tello.send_rc_control(0,0,hieght_spd*-1,0)
    pass


def ctrl():
    second = 0.001 # wait second to listen key
    bruh = int(second*1000) # init bruh  unit exchange
    print("ctrl's processing")
    while True:
        try:
            key = cv2.waitKey(bruh) & 0xff
            bruh = int(second*1000)
            if key == ord('x'):
                #self.capture.release()
                Thread(target=land, args=()).start()
                capture.release()
                cv2.destroyAllWindows()
                exit(1)
            
            elif key == ord('w'):
               Thread(target=move_forward, args=()).start()
            
            elif key == ord('s'):
                Thread(target=move_back, args=()).start()
            
            elif key == ord('a'):
                Thread(target=move_left, args=()).start()
            
            elif key == ord('d'):
                Thread(target=move_right, args=()).start()     

            elif key == ord('r'):
                Thread(target=move_up, args=()).start()
            
            elif key == ord('f'):
                Thread(target=move_down, args=()).start()

            elif key == ord('q'):
                Thread(target=rotate_clockwise, args=()).start()
                bruh = int(60)

            elif key == ord('e'):
                Thread(target=rotate_counter_clockwise, args=()).start()
                bruh = int(60)            
            elif key == ord('t'):
                Thread(target=takeoff, args=()).start()
            
            elif key == ord('l'):
                Thread(target=land, args=()).start()

            if key == 255 :
               tello.send_rc_control(0,0,0,0)

        except AttributeError:
            pass
"""

