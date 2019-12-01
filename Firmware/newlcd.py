from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
from gpiozero import Button

from PIL import Image
import sys
import ST7735


cButtonPin = 13
pButtonPin = 6

cameraButton = Button(cButtonPin)
powerButton = Button(pButtonPin)

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

backlight = False
backlight_count = 0
disp.set_backlight(0)
camera = PiCamera()
try:
    disp.begin()

    camera.resolution = (128, 128)
    camera.framerate = 32
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
            print(time.time()-backlight_count)
            print(backlight_count)
            if ((time.time() - backlight_count) > 5) and (backlight_count > 0):
                print("SHUTDOWN")
            if backlight_count == 0: #if button is held, dont change screen
                backlight_count = time.time()
                disp.set_backlight(backlight)
                backlight = not backlight
        else:
            backlight_count = 0

        rawCapture.truncate(0)

finally:
    camera.close()
    disp.set_backlight(0)
