from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
from gpiozero import Button     # for readding button pins

from PIL import Image
import sys
import ST7735                   # for lcd display
import subprocess

# CONSTANTS

#lcd/camera
WIDTH = 128
HEIGHT = 128
BAUDRATE = 24000000
FRAMERATE = 32

# PIN DEFINITIONS
# buttons
cameraButtonPin = 13
powerButtonPin = 6
#lcd
csPin = 1
dcPin = 26
rstPin = 19
backlightPin = 21

#STATES
WELCOME = 0
LOW_POWER = 1
SCREEN_ON = 2
CAPTURE_IMAGE = 3
RUN_OBJ_DET = 4
SHOW_DET_TEXT = 5
RUN_TRANSLATION = 6
SHOW_TRANSLATION = 7
SHUTDOWN = 8


#############################


# initialize LCD screen
def initLCD():
    disp = ST7735.ST7735(
        port = 0,
        cs = csPin,
        dc = dcPin,
        rst = rstPin,
        backlight=backlightPin,
        rotation=270,
        spi_speed_hz=BAUDRATE,
        width=WIDTH,
        height=HEIGHT,
        offset_left=2,
        offset_top=3,
        invert=False
    )
    disp.begin()
    return disp

def initCamera():
    camera = PiCamera()
    camera.resolution = (WIDTH, HEIGHT)
    camera.framerate = FRAMERATE
    return camera


try:

    rawCapture = PiRGBArray(camera, size=(128, 128))

    for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
        image = frame.array
        img = Image.fromarray(image, "RGB")

        disp.display(img)

        # check if button is pressed
        if cameraButton.is_pressed:
            camera.capture("/home/pi/OCRosettaStone/Firmware/image.jpg")
            disp.display(img)
            time.sleep(5)
            print("camera button pin 16")
            #buttonPressed = True
        if powerButton.is_pressed:
            print("power button pin 6")
            #buttonPressed = True

        rawCapture.truncate(0)

finally:
    camera.close()






if __name__ = "__main__":

    # initialize lcd, camera, buttons
    lcd = initLCD()
    cameraButton = Button(cameraButtonPin)
    powerButton = Button(powerButtonPin)
    camera = initCamera()

    #start state machine
    state = WELCOME

    while(true):
        if (state == WELCOME):

        elif (state == LOW_POWER):

        elif(state == SCREEN_ON):

        elif(state == CAPTURE_IMAGE):

        elif(state == RUN_OBJ_DET):

        elif(state == SHOW_DET_TEXT):

        elif(state == RUN_TRANSLATION):

        elif(state == SHOW_TRANSLATION):

        elif(state == SHUTDOWN):






