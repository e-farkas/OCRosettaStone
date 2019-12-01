from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np



camera = PiCamera()
camera.resolution = (128, 128)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size(128, 128))

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    img = Image.show(image)

    disp.display(img)

    rawCapture.truncate(0)
