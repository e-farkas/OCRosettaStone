from gpiozero import Button

cButtonPin = 16
pButtonPin = 6

cameraButton = Button(cButtonPin)
powerButton = Button(pButtonPin)

buttonPressed = false

while !buttonPressed:
    if cameraButton.is_pressed:
        print("camera button pin 16")
        buttonPressed = true
    if powerButton.is_pressed:
        print("power button pin 6")
        buttonPressed = true

