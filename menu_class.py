# import tools for OLED display
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import time

# import tools for the buttons
from digitalio import DigitalInOut, Direction, Pull

# other tools
import json
import random

# import BIP39 vocab and vocab tree 
with open('bip39VocabTree.json') as f:
    bip39VocabTree = json.load(f)

with open('bip39Vocab.json') as f:
    bip39Vocab = json.load(f)

OLED_WIDTH = 128
OLED_HEIGHT = 64

class menu:
    def __init__(self):
        # initialize display
        self.i2c = board.I2C()  # uses board.SCL and board.SDA
        # Create the SSD1306 OLED class.
        self.oled = adafruit_ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, self.i2c)
        # Create blank image for drawing.
        self.image = Image.new("1", (self.oled.width, self.oled.height))
        self.draw = ImageDraw.Draw(self.image)
        self.title = ''
        self.header = ''
        self.choices = ['', '', '']
        # Load a font in 2 different sizes.
        self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 11)
        return
    
    def display(self):
        optionsPos = [31, 42, 53]
        # clear display
        self.draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)
        # draw header and sub header
        self.draw.text((0, 0), self.title, font=self.font, fill=255)
        self.draw.text((0,11), self.header, font=self.font, fill=255)
        # draw the menu options
        for index in range(len(self.choices)):
            self.draw.text((0, optionsPos[index]), self.choices[index], font=self.font, fill=255)
        self.oled.image(self.image)
        self.oled.show()
        return

class selectMnemonicLength(menu): # child of menu
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
        self.allChoices = None
        return
    
    def updateChoice(self):
        nChoices = len(self.allChoices)
        print(nChoices, self.selection)
        if nChoices <= 3:
            idxi = 0
            idxf = nChoices - 1
            for ii, option in enumerate(self.allChoices[idxi:idxf+1]):
                if ii == self.selection - idxi:
                    self.choices[ii] = '>' + self.allChoices[idxi+ii]
                else:
                    self.choices[ii] = ' ' + self.allChoices[idxi+ii] 
        else:
            if self.selection < 2:
                idxi = 0
                idxf = 1
                self.choices[2] = ' down'
                for ii, option in enumerate(self.allChoices[idxi:idxf+1]):
                    if ii == self.selection - idxi:
                        self.choices[ii] = '>' + self.allChoices[idxi+ii]
                    else:
                        self.choices[ii] = ' ' + self.allChoices[idxi+ii] 
            elif (self.selection >= 2) and (self.selection <= (nChoices - 1 - 2)):
                self.choices[0] = ' up'
                self.choices[2] = ' down'
                self.choices[1] = '>' + self.allChoices[self.selection]
            else: # self.selection > nChoices - 1 - 2
                idxi = nChoices - 1 - 1
                idxf = nChoices - 1
                self.choices[0] = ' up'
                for ii, option in enumerate(self.allChoices[idxi:idxf+1]):
                    if ii == self.selection - idxi:
                        self.choices[ii+1] = '>' + self.allChoices[idxi+ii]
                    else:
                        self.choices[ii+1] = ' ' + self.allChoices[idxi+ii] 
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
                self.selection = self.selection % len(self.allChoices)
                self.updateChoice()
                time.sleep(0.2)
        
            if self.button_U.value:  # button is released
                pass
            else:
                self.selection-=1
                self.selection = self.selection % len(self.allChoices)
                self.updateChoice()
                time.sleep(0.2)

            if self.button_C.value:  # button is released
                pass
            else:
                waiting = False
            
        return self.selection
                
class wordEntry(menu):         
    def __init__(self, vocabTree):
        menu.__init__(self) # inherit __init__ of parent
        self.choiceIdx = 0
        self.options = None
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
            self.options = list(self.subTree.keys())
            return True
        else:
            return False
    def updateOptionsMenu(self):
        if isinstance(self.subTree[self.options[self.choiceIdx]], dict):
            self.choices[0] = self.selections + self.options[self.choiceIdx] 
        else:
            self.choices[0] = self.selections + self.options[self.choiceIdx] + ' ' + self.subTree[self.options[self.choiceIdx]][0]    
        self.display()

    
    def getChoicesAndNextChoice(self):
        # update subtree
        self.getSubTree()
        # determine valid letter options
        if self.getLetterOptions(): # there are more letters to choose
            if '*' in self.options:
                self.choiceIdx = self.options.index('*')
            else:
                self.choiceIdx = random.randrange(len(self.options))
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
                self.choiceIdx = self.choiceIdx % len(self.options)
                self.updateOptionsMenu()
                time.sleep(0.4)
        

            if self.button_U.value:  # button is released
                pass
            else:
                self.choiceIdx-=1
                self.choiceIdx = self.choiceIdx % len(self.options)
                self.updateOptionsMenu()
                time.sleep(0.4)

            if self.button_R.value:  # button is released
                pass
            else:
                time.sleep(0.4)
                self.selections = self.selections + self.options[self.choiceIdx]
                if self.getChoicesAndNextChoice():
                    self.updateOptionsMenu()
                else:
                    waiting = False
            
        return True
    

class mnemonicVerify(menu):
    def __init__(self, vocab, mnemonic):
        menu.__init__(self) # inherit __init__ of parent
        self.vocab = vocab
        self.mnemonic = mnemonic
        self.currentWord = ''
        self.randomWord = ''
        self.choiceTxt = ''
        self.button_L = DigitalInOut(board.D27)
        self.button_L.direction = Direction.INPUT
        self.button_L.pull = Pull.UP
        self.button_R = DigitalInOut(board.D23)
        self.button_R.direction = Direction.INPUT
        self.button_R.pull = Pull.UP
        return
    def getRandomWord(self):
        searching = True
        while searching:
            self.randomWord = random.choice(self.vocab)
            if self.randomWord == self.currentWord:
                pass # continue the search 
            else:
                searching = False
        return
    def getWordChoice(self):
        self.getRandomWord()
        self.choiceTxt = random.choice([['left', self.currentWord + ' ' + self.randomWord], ['right', self.randomWord + ' ' + self.currentWord]])
        return
    def confirmPhrase(self):
        self.title = 'Confirm Mnemonic'
        self.header = 'Choose < or >'
        for idx, word in enumerate(self.mnemonic):
            self.currentWord = word
            self.getWordChoice()
            correctWord = self.choiceTxt[0]
            self.choices[0] = self.choiceTxt[1]
            self.display()
            waiting = True
            while waiting:
                if self.button_R.value:  # button is released
                    pass
                else:
                    if correctWord == 'right':
                        print('YES')
                    else:
                        print('NO')
                    waiting = False
                    time.sleep(0.4)

                if self.button_L.value:  # button is released
                    pass
                else:
                    if correctWord == 'left':
                        print('YES')
                    else:
                        print('NO')
                    waiting = False
                    time.sleep(0.4)



level1 = menu()
level1.title = 'BIP39 Mnemonic'
level1.header = 'Phrase Input'
level1.display()
time.sleep(2)

level2 = selectMnemonicLength()
level2.title = 'Mnemonic Phrase'
level2.header = 'Length'
level2.allChoices = ['12', '15', '18', '21', '24']
leterIdx = level2.waitForSelection()
nWords = int(level2.allChoices[leterIdx])

print(nWords)

mnemonicPhrase = []
mnemonicIdx = []
while len(mnemonicPhrase) < nWords:
    level3 = wordEntry(bip39VocabTree)
    level3.title = 'Enter Mnemonic'
    level3.header = 'Enter Word #' + str(len(mnemonicPhrase)+1)
    level3.choices = ['', '', '']
    level3.makingSelections()
    mnemonicPhrase = mnemonicPhrase + [level3.subTree[0]]
    mnemonicIdx = mnemonicIdx + [level3.subTree[1]]

print(mnemonicPhrase)
print(mnemonicIdx)

confirmMenu = mnemonicVerify(bip39Vocab,mnemonicPhrase)
confirmMenu.confirmPhrase()


