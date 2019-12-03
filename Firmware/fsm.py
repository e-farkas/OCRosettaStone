from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
from gpiozero import Button     # for readding button pins
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import sys
import ST7735                   # for lcd display
import subprocess

# CONSTANTS

#lcd/camera
WIDTH = 1024
HEIGHT = 1024
BAUDRATE = 24000000
FRAMERATE = 32
LCD_WIDTH = 128
LCD_HEIGHT = 128

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
RUN_OCR = 4
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
        width=LCD_WIDTH,
        height=LCD_HEIGHT,
        offset_left=2,
        offset_top=3,
        invert=False
    )
    disp.begin()
    img = Image.new('RGB', (LCD_WIDTH, LCD_HEIGHT), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    disp.display(img)

    return disp

def initCamera():
    camera = PiCamera()
    camera.resolution = (WIDTH, HEIGHT)
    camera.framerate = FRAMERATE
    return camera

def textWrap(disp, txt_file):

    #The text to be displayed from
    textFile = open(txt_file, "r")
    text_to_display = textFile.read()
    #print("letters in string: " + str(len(text_to_display)))

    words = text_to_display.split("\n")

    img = Image.new('RGB', (LCD_WIDTH, LCD_HEIGHT), color=(0, 0, 0))

    draw = ImageDraw.Draw(img)

    fontSize = 14 # font size also sets pixel distance for new line
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", fontSize)

    size_x, size_y = draw.textsize(text_to_display, font)
    #print("text size: " + str(size_x) + ", " + str(size_y))

    charScreenWidth = 10 # maximum number of chars that fit horizontally
    left = 5 # buffer on left
    top = 10 # buffer on top
    draw.rectangle((0, 0, 128, 128), (0, 0, 0))
    ySpace = 0

    for word in words:
        wordIter = 0
        while len(word[wordIter:]) > charScreenWidth:
            draw.text((left,top + ySpace), word[wordIter:(wordIter + charScreenWidth)] + "-", font=font, fill=(255,0,0))
            ySpace += fontSize
            wordIter = wordIter + charScreenWidth
        draw.text((left,top + ySpace), word[wordIter:], font=font, fill=(255,0,0))
        ySpace += fontSize

    disp.display(img)
    time.sleep(0.1)


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
    img = Image.new('RGB', (WIDTH,HEIGHT))

    while(True):
        if (state == WELCOME):
            print("WELCOME")
            disp.set_backlight(True)
            textWrap(disp, "welcome.txt")
            time.sleep(10)
            state = SCREEN_ON

        elif (state == LOW_POWER):
            print("LOW_POWER")
            #turn screen on
            disp.set_backlight(False)
            time.sleep(0.3)  # need a little delay to remove finger from button
            if (powerButton.is_pressed):
                state = SCREEN_ON

        elif(state == SCREEN_ON):
            print("SCREEN_ON")
            disp.set_backlight(True)
            for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
                img = Image.fromarray(frame.array, "RGB")
                img = img.resize((LCD_WIDTH, LCD_HEIGHT))
                disp.display(img)
                rawCapture.truncate(0)

                #capture image
                if cameraButton.is_pressed:
                    state = CAPTURE_IMAGE
                    break
                #shutdown or turn screen on
                if powerButton.is_pressed:
                    if((time.time() - powerButtonHoldTime_s) > SHUTDOWN_THRESH_S) and (powerButtonHoldTime_s > 0):
                        state = SHUTDOWN
                    elif (powerButtonHoldTime_s == 0):  #change screen
                        powerButtonHoldTime_s = time.time()
                        state = LOW_POWER
                    break
                else:
                    powerButtonHoldTime_s = 0



        elif(state == CAPTURE_IMAGE):
            print("CAPTURE_IMAGE")
            camera.capture("/home/pi/OCRosettaStone/Firmware/image.jpg")
            disp.display(img)
            state = RUN_OCR

        elif(state == RUN_OCR):
            print("RUN_OCR")
            subprocess.call(["tesseract", "image.jpg", "out"])
            subprocess.call(["python", "../OCR/text_process.py", "out.txt"])
            state = SHOW_DET_TEXT

        elif(state == SHOW_DET_TEXT):
            print("SHOW_DET_TEXT")
            subprocess.call(["cat", "out.txt"])
            textWrap(disp, "out.txt")
            time.sleep(10)
            state = SCREEN_ON
        #elif(state == RUN_TRANSLATION):

        #elif(state == SHOW_TRANSLATION):

        elif(state == SHUTDOWN):
            print("SHUTDOWN")
            disp.set_backlight(False)
            camera.close()
            subprocess.call(["sudo", "shutdown", "now"])
            #TODO: shutdown from python

#finally:
#    camera.close()





