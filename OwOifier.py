from yaml import safe_load
from random import choice, randint


class owoifier:
    def __init__(self) -> None:
        with open('settings.yml', 'r') as data: settings: dict = safe_load(data)
        
        self.inputText: str = settings["defaults"]["inputText"]
        self.LW: bool = settings["defaults"]["LW"]
        self.YN: bool = settings["defaults"]["YN"]
        self.repeat: bool = settings["defaults"]["repeat"]
        self.replace: bool = settings["defaults"]["replace"]
        self.stutter: int = settings["defaults"]["stutter"]
        self.prefix: int = settings["defaults"]["prefix"]
        self.suffix: int = settings["defaults"]["suffix"]

        self.replacements: dict[str, str] = settings["replacements"]
        self.prefixes: list[str] = settings["prefixes"]
        self.suffixes: list[str] = settings["suffixes"]
        self.noTranslations: list[str] = settings["noTranslations"]

    def owoify(self) -> str:
        self.text = [line.split() for line in self.inputText.splitlines()]
        for self.line in range(len(self.text)):
            self.word = 0
            while self.word < len(self.text[self.line]):
                alpha = {int(alpha.isalpha()) for alpha in self.text[self.line][self.word]}
                if 1 not in alpha: self.word += 1; continue
                if self.replace: self.replaceWord()
                self.dontTranslate()
                self.escape = False
                self.removeEscape()
                if self.escape: self.word += 1; continue
                if self.LW: self.LRToW()
                if self.YN: self.YAfterN()
                if self.repeat: self.repeatAfterY()
                if 0 != self.stutter and 0 not in alpha: self.addStutter()
                if 0 != self.prefix: self.addPrefix()
                if 0 != self.suffix: self.addSuffix()
                self.word += 1
        return '\n'.join([' '.join(line) for line in self.text])

    def replaceWord(self) -> None:
        word = self.text[self.line][self.word]
        if word.lower() in self.replacements: 
            if word.istitle(): 
                self.text[self.line][self.word] = f'${self.replacements[word.lower()].title()}$'
            elif word.isupper(): 
                self.text[self.line][self.word] = f'${self.replacements[word.lower()].upper()}$'
            else: 
                self.text[self.line][self.word] = f'${self.replacements[word]}$'

    def dontTranslate(self) -> None:
        word = self.text[self.line][self.word]
        if word in self.noTranslations: 
            self.text[self.line][self.word] = f'${word}$'

    def removeEscape(self) -> None:
        word = self.text[self.line][self.word]
        escape: bool = word.startswith('$') and word.endswith('$')
        if escape: self.text[self.line][self.word] = word.replace('$', '')
        self.escape = escape

    def LRToW(self) -> None:
        self.text[self.line][self.word] = self.text[self.line][self.word].replace('l', 'w').replace('r', 'w')

    def YAfterN(self) -> None:
        word = self.text[self.line][self.word]
        for char in range(len(word)-2):
            if word[char].lower() == 'n' and word[char+1].lower() in ['a', 'e', 'i', 'o', 'u']:
                word = word[:char+1] + word[char+2].replace(word[char+2], 'y') + word[char+1:]
        self.text[self.line][self.word] = word

    def repeatAfterY(self) -> None:
        line, word = self.text[self.line], self.word
        if len(line[word]) > 3:
            if line[word][-1].lower() == 'y':
                line.insert(word+1, 'w' + line[word][1:])
                word += 1
        self.text[self.line], self.word = line, word

    def addStutter(self) -> None:
        word = self.text[self.line][self.word]
        stutter = []
        step, increaseChance = 1, 0
        while randint(1, 100) < self.stutter:
            if randint(1, 10) <= increaseChance: step += 1; increaseChance = 0
            if step > len(word): break
            stutter.append(word[:step])
            increaseChance += 1
        stutter.append(word)
        self.text[self.line][self.word] = '-'.join(stutter)

    def addPrefix(self) -> None:
        word = self.text[self.line][self.word]
        if randint(1, 100) < self.prefix:
            word = f"{choice(self.prefixes)} {word}"
        self.text[self.line][self.word] = word

    def addSuffix(self) -> None:
        word = self.text[self.line][self.word]
        if randint(1, 100) < self.suffix:
            word = f"{word} {choice(self.suffixes)}"
        self.text[self.line][self.word] = word


from customtkinter import *
from pyperclip import copy


class App(CTk):
    def __init__(self) -> None:
        super().__init__()
        
        # app settings
        self.title("OwOifier")
        self.minsize(700, 350)
        set_appearance_mode("system")
        self.configure(fg_color=("#ddb6dc", "#333333"))
        
        # widgets
        self.owo = owoifier()
        self.widgetsInit()
        self.setDefaults()
        self.setColors()
        self.setGrid()
        self.placeWidgets()
    
    # widget functions
    def widgetsInit(self) -> None:
        self.inputButton = CTkButton(self, text="OwOify!!", command=self.updateText)
        # input
        self.inputBox = CTkTextbox(self, wrap=WORD)
        self.pastaButton = CTkButton(self, text="Random Copypasta", command=self.pasta)
        # output
        self.outputBox = CTkTextbox(self, wrap=WORD, state=DISABLED)
        self.copyButton = CTkButton(self, text="Copy Output", command=self.copyText)
        # slider
        self.sliderFrame = CTkFrame(self)
        self.stutterLabel = CTkLabel(self.sliderFrame)
        self.stutterSlider = CTkSlider(self.sliderFrame, from_=0, to=100, number_of_steps=100, command=self.updateStutter)
        self.prefixLabel = CTkLabel(self.sliderFrame)
        self.prefixSlider = CTkSlider(self.sliderFrame, from_=0, to=100, number_of_steps=100, command=self.updatePrefix)
        self.suffixLabel = CTkLabel(self.sliderFrame)
        self.suffixSlider = CTkSlider(self.sliderFrame, from_=0, to=100, number_of_steps=100, command=self.updateSuffix)
        # checkbox
        self.checkboxFrame = CTkFrame(self)
        self.LWCheck = CTkCheckBox(self.checkboxFrame, text="L's and R's Converted to W's", command=self.updateLW)
        self.YNCheck = CTkCheckBox(self.checkboxFrame, text="Vowels After N's Become Y's", command=self.updateYN)
        self.repeatCheck = CTkCheckBox(self.checkboxFrame, text="Repeat Words Ending with Y", command=self.updateRepeat)
        self.replaceCheck = CTkCheckBox(self.checkboxFrame, text="Replace Words", command=self.updateReplace)

    def setDefaults(self) -> None:
        self.stutterSlider.set(self.owo.stutter); self.prefixSlider.set(self.owo.prefix); self.suffixSlider.set(self.owo.suffix)
        self.updateStutter(self.stutterSlider.get()); self.updateSuffix(self.prefixSlider.get()); self.updatePrefix(self.suffixSlider.get())
        self.LWCheck.select(self.owo.LW); self.YNCheck.select(self.owo.YN); self.repeatCheck.select(self.owo.repeat); self.replaceCheck.select(self.owo.replace)

    def setColors(self) -> None:
        self.sliderFrame.configure(fg_color="transparent")
        self.checkboxFrame.configure(fg_color="transparent")
        self.inputBox.configure(fg_color="#4D4D4D")
        self.outputBox.configure(fg_color="#4D4D4D")
        self.inputButton.configure(fg_color="#9e2e96", hover_color="#7f2478")
        self.copyButton.configure(fg_color="#9e2e96", hover_color="#7f2478")
        self.pastaButton.configure(fg_color="#9e2e96", hover_color="#7f2478")
        self.LWCheck.configure(fg_color="#9e2e96", hover_color="#7f2478")
        self.YNCheck.configure(fg_color="#9e2e96", hover_color="#7f2478")
        self.repeatCheck.configure(fg_color="#9e2e96", hover_color="#7f2478")
        self.replaceCheck.configure(fg_color="#9e2e96", hover_color="#7f2478")
        self.stutterSlider.configure(button_color="#9e2e96", progress_color="#9e2e96", button_hover_color="#7f2478")
        self.prefixSlider.configure(button_color="#9e2e96", progress_color="#9e2e96", button_hover_color="#7f2478")
        self.suffixSlider.configure(button_color="#9e2e96", progress_color="#9e2e96", button_hover_color="#7f2478")

    def setGrid(self) -> None:
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)

    def placeWidgets(self) -> None:
        self.configure(padx=15, pady=15)
        self.inputBox.grid(     row=0, column=0, rowspan=2,                            sticky=NSEW)
        self.pastaButton.grid(  row=2, column=0,            pady=(10, 0),              sticky=W)
        self.checkboxFrame.grid(row=0, column=1,            padx=10,      pady=(5, 0), sticky=NSEW)
        self.sliderFrame.grid(  row=1, column=1,            padx=10)
        self.inputButton.grid(  row=2, column=1,            pady=(10, 0))
        self.outputBox.grid(    row=0, column=2, rowspan=2,                            sticky=NSEW)
        self.copyButton.grid(   row=2, column=2,            pady=(10, 0),              sticky=E)
        # > checkbox
        self.LWCheck.grid(      row=0,                      pady=(0, 10),              sticky=W)
        self.YNCheck.grid(      row=1,                      pady=(0, 10),              sticky=W)
        self.repeatCheck.grid(  row=2,                      pady=(0, 10),              sticky=W)
        self.replaceCheck.grid( row=3,                      pady=(0, 10),              sticky=W)
        # > slider
        self.stutterLabel.grid( row=0)
        self.stutterSlider.grid(row=1,                      pady=(0, 10))
        self.prefixLabel.grid(  row=2)
        self.prefixSlider.grid( row=3,                      pady=(0, 10))
        self.suffixLabel.grid(  row=4)
        self.suffixSlider.grid( row=5,                      pady=(0, 10))

    # textbox functions
    def updateText(self) -> None:
        self.owo.inputText = self.inputBox.get('0.0', END)
        self.outputBox.configure(state=NORMAL)
        self.outputBox.delete('0.0', END)
        self.outputBox.insert(INSERT, self.owo.owoify())
        self.outputBox.configure(state=DISABLED)

    def copyText(self) -> None:
        copy(self.outputBox.get('0.0', END))

    def pasta(self) -> None:
        self.inputBox.delete('0.0', END)
        with open("settings.yml") as data: settings: dict = safe_load(data)
        self.inputBox.insert('0.0', choice(settings["pasta"]))
        self.updateText()

    # slider functions
    def updateStutter(self, val) -> None:
        self.owo.stutter = val
        self.stutterLabel.configure(text=f'Stutter Chance: {val:.0f}%')

    def updatePrefix(self, val) -> None:
        self.owo.prefix = val
        self.prefixLabel.configure(text=f'Prefix Chance: {val:.0f}%')

    def updateSuffix(self, val) -> None:
        self.owo.suffix = val
        self.suffixLabel.configure(text=f'Suffix Chance: {val:.0f}%')

    # checkbox functions
    def updateLW(self) -> None:
        self.owo.LW = bool(self.LWCheck.get())

    def updateYN(self) -> None:
        self.owo.YN = bool(self.YNCheck.get())

    def updateRepeat(self) -> None:
        self.owo.repeat = bool(self.repeatCheck.get())

    def updateReplace(self) -> None:
        self.owo.replace = bool(self.replaceCheck.get())


if __name__ in "__main__":
    app = App()
    app.mainloop()
