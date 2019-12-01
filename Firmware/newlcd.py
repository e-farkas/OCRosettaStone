from picamera.array import PiRGBArray
from picamera import PiCamera
#import time
import numpy as np

from PIL import Image
import sys
import ST7735 as ST7735

disp = ST7735.ST7735(
    port = 0,
    cs = 1,
    dc = 26,
    rst = 19,
    backlight=21,
    rotation=270,
    spi_speed_hz=24000000,
    width=128,
    height=128,
    offset_left=2,
    offset_top=3,
    invert=False
)

disp.begin()

camera = PiCamera()
camera.resolution = (128, 128)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size(128, 128))

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    img = Image.fromArray(image, "RGB")

    disp.display(img)

    rawCapture.truncate(0)
