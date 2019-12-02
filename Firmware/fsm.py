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

SHUTDOWN_THRESH_S = 5

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
    #disp.set_backlight(False)
    return disp

def initCamera():
    camera = PiCamera()
    camera.resolution = (WIDTH, HEIGHT)
    camera.framerate = FRAMERATE
    return camera




if __name__ == "__main__":

    # initialize lcd, camera, buttons
    disp = initLCD()
    cameraButton = Button(cameraButtonPin)
    powerButton = Button(powerButtonPin)
    camera = initCamera()
    rawCapture = PiRGBArray(camera, size=(WIDTH, HEIGHT))

    #start state machine
    state = WELCOME
    powerButtonHoldTime_s = 0
    backlight = False
    img = Image.new('RGB', (WIDTH,HEIGHT))

    while(True):
        if (state == WELCOME):
            print("WELCOME")
            #TODO: create welcome screen
            state = SCREEN_ON

        elif (state == LOW_POWER):
            print("LOW_POWER")
            #state = LOW_POWER
            #turn screen on
            disp.set_backlight(False)
            if (powerButton.is_pressed):
                state = SCREEN_ON

        elif(state == SCREEN_ON):
            print("SCREEN_ON")
            disp.set_backlight(True)
            for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
                img = Image.fromarray(frame.array, "RGB")
                disp.display(img)
                #state = SCREEN_ON
                rawCapture.truncate(0)

                #capture image
                if cameraButton.is_pressed:
                    state = CAPTURE_IMAGE
                #shutdown or turn screen on
                if powerButton.is_pressed:
                    if((time.time() - powerButtonHoldTime_s) > SHUTDOWN_THRESH_S) and (powerButtonHoldTime_s > 0):
                        state = SHUTDOWN
                    elif (powerButtonHoldTime_s == 0):  #change screen
                        powerButtonHoldTime_s = time.time()
                        state = LOW_POWER
                else:
                    powerButtonHoldTime_s = 0



        elif(state == CAPTURE_IMAGE):
            print("CAPTURE_IMAGE")
            camera.capture("/home/pi/OCRosettaStone/Firmware/image.jpg")
            disp.display(img)
            time.sleep(5)
            state = SCREEN_ON

        #elif(state == RUN_OBJ_DET):

        #elif(state == SHOW_DET_TEXT):

        #elif(state == RUN_TRANSLATION):

        #elif(state == SHOW_TRANSLATION):

        elif(state == SHUTDOWN):
            print("SHUTDOWN")
            #TODO: create shutdown sequence
            #NOTE: stutdown logic doesnt work rn so we never get here

#finally:
#    camera.close()





