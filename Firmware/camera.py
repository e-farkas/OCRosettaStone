from picamera import PiCamera
import time

previewTime = 10

camera=PiCamera()

camera.start_preview()
#camera.startPreview(alpha=180)
time.sleep(previewTime)
camera.capture("/home/pi/Desktop/camCapture.jpg")
camera.stop_preview()
