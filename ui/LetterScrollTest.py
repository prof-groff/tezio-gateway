# Imports the necessary libraries...
import board
import digitalio
from digitalio import DigitalInOut, Direction, Pull
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import time
# Setting some variables for our reset pin etc.
RESET_PIN = digitalio.DigitalInOut(board.D4)
# Very important... This lets py-gaugette 'know' what pins to use in order to reset the display

i2c = board.I2C()  # uses board.SCL and board.SDA

# Create the SSD1306 OLED class.
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

oled.fill(0)
oled.show()

letterOptions = [" a ", " b "," c ", " d ", " e ", " f ", " g ", " h ", " i ", " j ", " k ", " l ", " m ", " n ", " o ", " p ", " q ", " r ", " s ", " t ", " u ", " v ", " w ", " y ", " z "]

# Create blank image for drawing.
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Load a font in 2 different sizes.
# font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 20)

draw.text((20, 18), " a _ _ ", font=font, fill=255)

oled.image(image)
oled.show()
