from gpiozero import Button

cButtonPin = 13
pButtonPin = 6

cameraButton = Button(cButtonPin)
powerButton = Button(pButtonPin)

buttonPressed = False

while buttonPressed == False:
    if cameraButton.is_pressed:
        print("camera button pin 16")
        buttonPressed = True
    if powerButton.is_pressed:
        print("power button pin 6")
        buttonPressed = True

