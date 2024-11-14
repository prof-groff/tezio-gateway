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


button_U = DigitalInOut(board.D17)
button_U.direction = Direction.INPUT
button_U.pull = Pull.UP


button_D = DigitalInOut(board.D22)
button_D.direction = Direction.INPUT
button_D.pull = Pull.UP

# Clear display.
oled.fill(0)
oled.show()

def drawMenu(menuHeader, menuSubheader, menuOptions, oled, image, draw):
    optionsPos = [29, 39, 49]
    # clear display
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    # draw header and sub header
    draw.text((0, 0), menuHeader, font=headerFont, fill=255)
    draw.text((0,12), menuSubheader, font=headerFont, fill=255)
    # draw the menu options
    for index in range(len(menuOptions)):
        draw.text((0, optionsPos[index]), menuOptions[index], font=menuFont, fill=255)
    oled.image(image)
    oled.show()
    return

# menu contents
menuHeader = "Menu Header"
menuSubheader = "Menu Subheader"
menuOptions = ["  Option 1", "  Option 2", "  Option 3"]
topMenuOptionsLocations = [29, 39, 49]



# Create blank image for drawing.
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Load a font in 2 different sizes.
headerFont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 12)
menuFont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 10)


def renderCarrot(optionsPos, pick):
    # Draw the carrots
    for index in range(len(optionsPos)):
        if index == pick:
            fill = 255
        else:
            fill = 0
        draw.text((0, optionsPos[index]), ">", font=menuFont,fill=fill)
    oled.image(image)
    oled.show()
    
drawMenu(menuHeader, menuSubheader, menuOptions, oled, image, draw)

currentPick = 0
renderCarrot(topMenuOptionsLocations, currentPick)
while True:
    if button_D.value:  # button is released
        pass
    else:
        currentPick = currentPick + 1
        currentPick = currentPick % len(menuOptions)
        renderCarrot(topMenuOptionsLocations, currentPick)
        time.sleep(0.2)
        

    if button_U.value:  # button is released
        pass
    else:
        currentPick = currentPick - 1
        currentPick = currentPick % len(menuOptions)
        renderCarrot(topMenuOptionsLocations, currentPick)
        time.sleep(0.2)


