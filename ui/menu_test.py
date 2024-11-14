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


# define menu
topMenuHeading = "Top Level Menu"
topMenuOptions = ["  Option 1", "  Option 2", "  Option 3"]
topMenuOptionsLocations = [16, 32, 48]

# Create blank image for drawing.
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Load a font in 2 different sizes.
headerFont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 12)
menuFont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 10)

def renderMenu(headerText, optionsText, optionsPos):
    # Draw the menu header
    draw.text((0, 0), headerText, font=headerFount, fill=255)
    # draw the menu options
    for index in range(len(optionsText)):
        draw.text((0, optionsPos[index]), optionsText[index], font=menuFont, fill=255)
    oled.image(image)
    oled.show()
    return

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
    
renderMenu(topMenuHeading, topMenuOptions, topMenuOptionsLocations)

currentPick = 0
renderCarrot(topMenuOptionsLocations, currentPick)
while True:
    if button_D.value:  # button is released
        pass
    else:
        currentPick = currentPick + 1
        currentPick = currentPick % len(topMenuOptions)
        renderCarrot(topMenuOptionsLocations, currentPick)
        time.sleep(0.2)
        

    if button_U.value:  # button is released
        pass
    else:
        currentPick = currentPick - 1
        currentPick = currentPick % len(topMenuOptions)
        renderCarrot(topMenuOptionsLocations, currentPick)
        time.sleep(0.2)


