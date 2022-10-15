import io
import numpy as np
import PIL
from PIL import Image
import torch
import openpifpaf
import cv2
import random
import time 


st = time.time()
player = cv2.VideoCapture('000000081988.jpg')
_, ok = player.read()
pil_ok = cv2.cvtColor(ok, cv2.COLOR_BGR2RGB)

predictor = openpifpaf.Predictor(checkpoint='resnet50', json_data=True )
predictions, gt_anns, image_meta = predictor.numpy_image(pil_ok)

print(predictions)
"""
print(predictions[0]["keypoints"])
print(len(predictions[0]["keypoints"])/3)
"""
box_filter = ok.copy()
for l in range(len(predictions)):
	fall = False 
	# the color of each person's body dot
	b, g, r = 255, 255, 255
	# list title 
	kp = predictions[l]["keypoints"] 
	bbox = predictions[l]["bbox"]
	# body line's width and color
	body_trunk = 4
	bgr_body = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

	face_bgr = (0, 0, 255)		#	
	neck_bgr = (255, 255, 255)	#
	body_bgr = (100, 255, 77)	#

	leftHand_bgr = (245, 0, 231)	#
	leftLeg_bgr = (194, 102, 255)	#
	rightHand_bgr = (149, 94, 255)	#
	rightLeg_bgr = (237, 101, 23)	#

# --------------- Face ------------------	
	if kp[0] and kp[3]: # nose to left eye
		cv2.line(box_filter, (int(kp[0]),int(kp[1])), (int(kp[3]),int(kp[4])), face_bgr, body_trunk)	
	if kp[0] and kp[6]: # nose to right eye
		cv2.line(box_filter, (int(kp[0]),int(kp[1])), (int(kp[6]),int(kp[7])), face_bgr, body_trunk)	
	if kp[6] and kp[12]:# right eye to ear
		cv2.line(box_filter, (int(kp[6]),int(kp[7])), (int(kp[12]),int(kp[13])), face_bgr, body_trunk)	
	if kp[3] and kp[9]: # left eye to ear
		cv2.line(box_filter, (int(kp[3]),int(kp[4])), (int(kp[9]),int(kp[10])), face_bgr, body_trunk)	
	if kp[0] and kp[15]: # nose to left shoulder
		cv2.line(box_filter, (int(kp[0]),int(kp[1])), (int(kp[15]),int(kp[16])), neck_bgr, body_trunk)	
	if kp[0] and kp[18]: # nose to right shoulder 
		cv2.line(box_filter, (int(kp[0]),int(kp[1])), (int(kp[18]),int(kp[19])), neck_bgr, body_trunk)	
# --------------- Face ------------------

# --------------- Hands ------------------
	if kp[24] and kp[18]: # right elbow to shoulder
		cv2.line(box_filter, (int(kp[24]),int(kp[25])), (int(kp[18]),int(kp[19])), rightHand_bgr, body_trunk)	
	if kp[21] and kp[15]: # left elbow to shoulder 
		cv2.line(box_filter, (int(kp[21]),int(kp[22])), (int(kp[15]),int(kp[16])), leftHand_bgr, body_trunk)	
	if kp[24] and kp[30]: # right elbow to wrist
		cv2.line(box_filter, (int(kp[24]),int(kp[25])), (int(kp[30]),int(kp[31])), rightHand_bgr, body_trunk)	
	if kp[21] and kp[27]: # left elbow to wrist
		cv2.line(box_filter, (int(kp[21]),int(kp[22])), (int(kp[27]),int(kp[28])), leftHand_bgr, body_trunk)	
# ---------------- Hands ------------------

# ---------------- Body ------------------
	if kp[15] and kp[18]: # left shoulder to right shoulder 
		cv2.line(box_filter, (int(kp[15]),int(kp[16])), (int(kp[18]),int(kp[19])), body_bgr, body_trunk)
	if kp[18] and kp[36]: # right shoulder to hip 
		cv2.line(box_filter, (int(kp[36]),int(kp[37])), (int(kp[18]),int(kp[19])), body_bgr, body_trunk)	
	if kp[15] and kp[33]: # left shoulder to hip
		cv2.line(box_filter, (int(kp[15]),int(kp[16])), (int(kp[33]),int(kp[34])), body_bgr, body_trunk)	
	if kp[33] and kp[36]: # right hip to left hip 
		cv2.line(box_filter, (int(kp[33]),int(kp[34])), (int(kp[36]),int(kp[37])), body_bgr, body_trunk)	
# ---------------- Body ------------------

# ---------------- Legs ------------------
	if kp[36] and kp[42]: # right hip to knee 
		cv2.line(box_filter, (int(kp[36]),int(kp[37])), (int(kp[42]),int(kp[43])), rightLeg_bgr, body_trunk)	
	if kp[33] and kp[39]: # left hip to knee
		cv2.line(box_filter, (int(kp[33]),int(kp[34])), (int(kp[39]),int(kp[40])), leftLeg_bgr, body_trunk)	
	if kp[42] and kp[48]: # right knee to right ankle  
		cv2.line(box_filter, (int(kp[42]),int(kp[43])), (int(kp[48]),int(kp[49])), rightLeg_bgr, body_trunk)	
	if kp[39] and kp[45]: # left knee to ankle  
		cv2.line(box_filter, (int(kp[39]),int(kp[40])), (int(kp[45]),int(kp[46])), leftLeg_bgr, body_trunk)
# ---------------- Legs ------------------

	# plot the body parts' dot 
	i=0
	while i<(len(kp)):
		cv2.circle(box_filter,(int(kp[i]), int(kp[i+1])), 2, (b, g, r), -1)
		i=i+3

	# detect if someone gonna fall down
	print(f"{l} head y: {int(kp[1])} hip y : {( int(kp[34]) + int(kp[37]) )/2}\n{abs(int(kp[1]) - ( int(kp[34]) + int(kp[37]) )/2)}")
	if abs( int(kp[1]) - ( int(kp[34]) + int(kp[37]) )/2 ) < 20:
		# plot the frame of this person
		upl = int(bbox[0]), int(bbox[1])
		buttomr = int(bbox[0]+bbox[2]), int(bbox[1]+bbox[3])
		cv2.rectangle(box_filter, upl, buttomr, (0,0,255) , 1)		
		cv2.putText(box_filter,"!!!Fall detected!!!", (int(bbox[0]),int(bbox[1])-5), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,0,255), 1)	

Transparency = 0.7
ok = cv2.addWeighted(box_filter, Transparency, ok, 1 - Transparency, 0)

cv2.imshow("ewe",ok)

# calculate the executed time
et = time.time()
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')

cv2.waitKey(0)


