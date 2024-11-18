# import tools for OLED display
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import time

# import tools for the buttons
# import digitalio
from digitalio import DigitalInOut, Direction, Pull

# other tools
import json
import random

with open('bip39VocabTree.json') as f:
    bip39VocabTree = json.load(f)


class menu:
    def __init__(self):
        # initialize display
        self.i2c = board.I2C()  # uses board.SCL and board.SDA
        # Create the SSD1306 OLED class.
        self.oled = adafruit_ssd1306.SSD1306_I2C(128, 64, self.i2c)
        # Create blank image for drawing.
        self.image = Image.new("1", (self.oled.width, self.oled.height))
        self.draw = ImageDraw.Draw(self.image)
        self.header = ''
        self.subHeader = ''
        self.options = ['', '', '']
        # Load a font in 2 different sizes.
        self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 11)
        return
    
    def display(self):
        optionsPos = [31, 42, 53]
        # clear display
        self.draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)
        # draw header and sub header
        self.draw.text((0, 0), self.header, font=self.font, fill=255)
        self.draw.text((0,11), self.subHeader, font=self.font, fill=255)
        # draw the menu options
        for index in range(len(self.options)):
            self.draw.text((0, optionsPos[index]), self.options[index], font=self.font, fill=255)
        self.oled.image(self.image)
        self.oled.show()
        return

class verticalMenu(menu): # child of menu
    def __init__(self):
        menu.__init__(self) # inherit __init__ of parent
        self.selection = 0
        self.button_U = DigitalInOut(board.D17)
        self.button_U.direction = Direction.INPUT
        self.button_U.pull = Pull.UP

        self.button_D = DigitalInOut(board.D22)
        self.button_D.direction = Direction.INPUT
        self.button_D.pull = Pull.UP

        self.button_C = DigitalInOut(board.D4)
        self.button_C.direction = Direction.INPUT
        self.button_C.pull = Pull.UP
        self.allOptions = None
        return
    
    def updateChoice(self):
        lenAllOptions = len(self.allOptions)
        if len(self.allOptions) <= 3:
            startingIdx = 0
            endingIdx = len(self.allOptions)-1
        else:
            if self.selection < 3:
                startingIdx = 0
                endingIdx = 2
            else:
                startingIdx = self.selection - 2
                endingIdx = self.selection
        for ii, option in enumerate(self.allOptions[startingIdx:endingIdx+1]):
            if ii == self.selection - startingIdx:
                self.options[ii] = '>' + self.allOptions[startingIdx+ii]
            else:
                self.options[ii] = ' ' + self.allOptions[startingIdx+ii]
        self.display()
        return
    
    def waitForSelection(self):
        self.updateChoice()
        waiting = True
        while waiting:
            if self.button_D.value:  # button is released
                pass
            else:
                self.selection+=1
                self.selection = self.selection % len(self.allOptions)
                self.updateChoice()
                time.sleep(0.2)
        
            if self.button_U.value:  # button is released
                pass
            else:
                self.selection-=1
                self.selection = self.selection % len(self.allOptions)
                self.updateChoice()
                time.sleep(0.2)

            if self.button_C.value:  # button is released
                pass
            else:
                waiting = False
            
        return self.selection
                
class enterWordMenu(menu):         
    def __init__(self, vocabTree):
        menu.__init__(self) # inherit __init__ of parent
        self.choiceIdx = 0
        self.choices = None
        self.vocabTree = vocabTree
        self.selections = ''
        self.subTree = None

        self.button_U = DigitalInOut(board.D17)
        self.button_U.direction = Direction.INPUT
        self.button_U.pull = Pull.UP

        self.button_D = DigitalInOut(board.D22)
        self.button_D.direction = Direction.INPUT
        self.button_D.pull = Pull.UP

        self.button_L = DigitalInOut(board.D27)
        self.button_L.direction = Direction.INPUT
        self.button_L.pull = Pull.UP

        self.button_R = DigitalInOut(board.D23)
        self.button_R.direction = Direction.INPUT
        self.button_R.pull = Pull.UP
        return
    def getSubTree(self):
        self.subTree = self.vocabTree
        for letter in self.selections:
            self.subTree = self.subTree[letter]
        return
    def getLetterOptions(self):
        if isinstance(self.subTree, dict):
            self.choices = list(self.subTree.keys())
            return True
        else:
            return False
    def updateOptionsMenu(self):
        if isinstance(self.subTree[self.choices[self.choiceIdx]], dict):
            self.options[0] = self.selections + self.choices[self.choiceIdx] 
        else:
            self.options[0] = self.selections + self.choices[self.choiceIdx] + ' ' + self.subTree[self.choices[self.choiceIdx]][0]    
        self.display()

    
    def getChoicesAndNextChoice(self):
        # update subtree
        self.getSubTree()
        # determine valid letter options
        if self.getLetterOptions(): # there are more letters to choose
            if '*' in self.choices:
                self.choiceIdx = self.options.index('*')
            else:
                self.choiceIdx = random.randrange(len(self.choices))
            return True
        else:
            return False
            

    def makingSelections(self):
        self.getChoicesAndNextChoice()
        self.updateOptionsMenu()
        waiting = True
        while waiting:
            if self.button_D.value:  # button is released
                pass
            else:
                self.choiceIdx+=1
                self.choiceIdx = self.choiceIdx % len(self.choices)
                self.updateOptionsMenu()
                time.sleep(0.4)
        

            if self.button_U.value:  # button is released
                pass
            else:
                self.choiceIdx-=1
                self.choiceIdx = self.choiceIdx % len(self.choices)
                self.updateOptionsMenu()
                time.sleep(0.4)

            if self.button_R.value:  # button is released
                pass
            else:
                time.sleep(0.4)
                self.selections = self.selections + self.choices[self.choiceIdx]
                if self.getChoicesAndNextChoice():
                    self.updateOptionsMenu()
                else:
                    waiting = False
            
        return self.getSubTree()


level1 = menu()
level1.header = 'BIP39 Mnemonic'
level1.subHeader = 'Phrase Input'
level1.display()
time.sleep(2)

level2 = verticalMenu()
level2.header = 'Mnemonic Phrase'
level2.subHeader = 'Length'
level2.allOptions = ['12', '15', '18', '21', '24']
nWords = level2.waitForSelection()
print(nWords)

mnemonicPhrase = []
mnemonicIdx = []
while len(mnemonicPhrase) < nWords:
    level3 = enterWordMenu(bip39VocabTree)
    level3.header = 'Enter Mnemonic'
    level3.subHeader = 'Enter Word #1'
    level3.options = ['', '', '']
    choice = level3.makingSelections()
    menmonicPhrase = mnemonicPhrase + [choice[0]]
    mnemonicIdx = mnemonicIdx + [choice[1]]

print(choice)


