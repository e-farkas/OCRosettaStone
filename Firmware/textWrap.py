from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time
import sys
import ST7735

#MESSAGE = "Hello World! How are you today?"

#The text to be displayed from 
textFile = open(sys.argv[1], "r")
text_to_display = textFile.read()

#text_to_display = sys.argv[1]  
#MESSAGE2 = "how many chars"
  # Create ST7735 LCD display class.
disp = ST7735.ST7735(
    port = 0,
    cs = 1,
    dc = 26,
    rst = 19,
    backlight=21,               # 18 for back BG slot, 19 for front BG slot.
    rotation=90,
    spi_speed_hz=24000000,
    width=128,
    height=128,
    offset_left=2,
    offset_top=3,
    invert=False
)

# Initialize display.
disp.begin()

print("letters in string" + len(text_to_display))

words = text_to_display.split("\n")

WIDTH = disp.width
HEIGHT = disp.height
 
img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
textImg = ImageDraw.multiline_text()
  
draw = ImageDraw.Draw(img)
  
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
  
size_x, size_y = draw.textsize(text_to_display, font)
print("text size: " + size_x + size_y)

#while True:
draw.rectangle((0, 0, 128, 128), (0, 0, 0))
ySpace = 0;
for word in words:
  if len(word) > 8:
    draw.text((10,20 + ySpace), word[], font=font, fill=(255,0,0))
  else:
    draw.text((10,20 + ySpace), word, font=font, fill=(255,0,0))
    ySpace += 20
    #draw.text((10,20), MESSAGE2, font=font, fill=(255,0,0))
disp.display(img)
time.sleep(0.1)
