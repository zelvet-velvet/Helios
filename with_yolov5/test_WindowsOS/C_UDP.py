#importing libraries
import socket
import cv2
import pickle
import struct
import imutils
import numpy as np
import base64
import sys
import time

try:
	local_ip = sys.argv[1]
	server_ip = sys.argv[2]
	if local_ip == "--help":
		print("usage: python3 C_UDP.py [self_IP_addr]")
		exit()
except:
	print("error : missing local IP parameter")
	print("usage: python3 C_UDP.py [self_IP_addr] [server_IP_addr]")
	exit()

# Client socket
# create an INET, STREAMing socket : 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

port = 60050 # Port to listen on (non-privileged ports are > 1023)
print('HOST IP:', local_ip )
socket_address = (local_ip, port)
client_socket.bind(socket_address)
print('Socket bind complete')

data = b""
# Q: unsigned long long integer(8 bytes)
payload_size = struct.calcsize("Q")
ip=(server_ip,port)
client_socket.sendto(b"ewe",ip)
while True:
	start_time = time.time()
	packet,_ = client_socket.recvfrom(65536)
	data = base64.b64decode(packet,' /')
	npdata = np.fromstring(data,dtype=np.uint8)
	frame = cv2.imdecode(npdata,1)
	cv2.imshow("Receiving...",frame)
	key = cv2.waitKey(1)
	print("FPS: ", 1.0 / (time.time() - start_time)) # FPS = 1 / time to process loop
"""
	st = time.time()
	et = time.time()
	elapsed_time = et - st
	print('Execution time:', elapsed_time, 'seconds')
"""

