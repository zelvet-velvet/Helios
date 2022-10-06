import io
import numpy as np
import PIL
from PIL import Image
import requests
import torch
import openpifpaf
import cv2
import json


image_response = requests.get('https://raw.githubusercontent.com/openpifpaf/openpifpaf/main/docs/coco/000000081988.jpg')
pil_im = PIL.Image.open(io.BytesIO(image_response.content)).convert('RGB')
im = np.asarray(pil_im)
ok=cv2.imread('000000081988.jpg')

predictor = openpifpaf.Predictor(checkpoint='shufflenetv2k16')
predictions, gt_anns, image_meta = predictor.pil_image(pil_im)

annotation_painter = openpifpaf.show.AnnotationPainter()
print(predictions[0].data)
print(predictions[0].data[0][0])

cv2.circle(ok,(int(predictions[0].data[0][0]), int(predictions[0].data[0][1])), 3, (0, 0, 255), -1)

cv2.imshow("ewe",ok)
cv2.waitKey(0)
with openpifpaf.show.image_canvas(im) as ax:
    annotation_painter.annotations(ax, predictions)


