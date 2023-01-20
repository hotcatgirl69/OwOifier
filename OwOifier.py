from random import random, choice
from pyperclip import copy
from customtkinter import *


class OwOifier:
	replacements = {
		"love": "wuv", 
		"mr.": "mistuh", 
		"dog": "doggo", 
		"cat": "kitteh", 
		"hello": "henwo", 
		"hell": "heck", 
		"fuck": "fwick", 
		"baby": "bae", 
		"shit": "shoot", 
		"friend": "fren", 
		"stop": "stawp", 
		"god": "gosh", 
		"dick": "pp", 
		"penis": "pp", 
		"cock": "pp", 
		"damn": "darn", 
		"you": "u", 
		"your": "ur",
		"please": "pls",
		"for": "4",
		"how": "meow",
		"feeling": "feline",
		"are": "r",
		"thanks": "thx",
	}

	prefixes = [
		"OwO", 
		"hehe", 
		"*nuzzles*", 
		"*blushes*", 
		"*giggles*", 
		"*waises paw*", 
		"whats this", 
		"*notices bulge*", 
		"*unbuttons shirt*",
	]

	suffixes = [
		":3", 
		">:3", 
		"xox", 
		">~<", 
		">3<", 
		"=3=", 
		"UwU", 
		"hehe", 
		"murr~", 
		"*gwomps*",
	]

	def __init__(self, text='', LRToW=True, YAfterN=True, repeatAfterY=True, replaceWords=True, stutterChance=0.15, prefixChance=0.15, suffixChance=0.15) -> None:
		self.text = text
		self.LRToW = LRToW
		self.YAfterN = YAfterN
		self.repeatAfterY = repeatAfterY
		self.replaceWords = replaceWords
		self.stutterChance = stutterChance
		self.prefixChance = prefixChance
		self.suffixChance = suffixChance

	def owoify(self) -> str:
		text = self.text.split('\n')[:-1]
		for line in range(len(text) - 1):
			text[line] = text[line].split()
			skip = False
			word = 0
			while word < len(text[line]):
				if skip:
					skip = False
					word += 1
					continue
				
				if self.replaceWords:
					if text[line][word].lower() in self.replacements:
						text[line][word] = self.replacements[text[line][word].lower()].upper() if text[line][word].isupper() else self.replacements[text[line][word].lower()]
						text[line][word] = f'${text[line][word]}$'

				if text[line][word][0] == '$' and text[line][word][-1] == '$':
					text[line][word] = text[line][word].replace('$', '')
					word += 1
					continue

				if self.LRToW:
					text[line][word] = text[line][word].replace('l', 'w')
					text[line][word] = text[line][word].replace('r', 'w')

				if self.YAfterN:
					for char in range(len(text[line][word])):
						if char > 0:
							if text[line][word][char-1].lower() == 'n':
								if text[line][word][char].lower() in ['a', 'e', 'i', 'o', 'u']:
									text[line][word] = text[line][word][:char] + text[line][word][char].replace(text[line][word][char], 'y') + text[line][word][char:]

				if self.repeatAfterY:
					if text[line][word].len() > 3:
						if text[line][word][-1].lower() == 'y':
							text[line].insert(word + 1, 'w' + text[line][word][1:])
							skip = True

				if self.stutterChance > 0 and self.stutterChance < 1:
					#find the first character that is a letter
					letter = -1
					for char in range(len(text[line][word])):
						if text[line][word][char].isalpha(): 
							letter = char 
							break
					#recursively add stutter to word
					if letter > 0:
						while True:
							if random() < self.stutterChance:
								text[line][word] = text[line][word][:letter+1] + '-' + text[line][word][letter:] 
							else:
								break

				if self.prefixChance > 0 and self.prefixChance < 1:
					if random() < self.prefixChance:
						text[line].insert(word-1, choice(self.prefixes))
						word += 1

				if self.suffixChance > 0 and self.suffixChance < 1:
					if random() < self.suffixChance:
						text[line].insert(word+1, choice(self.suffixes))
						word += 1
						skip = True

				word += 1 #iterate

			text[line] = ' '.join(text[line])

		text = '\n'.join(text)
		return text


class App(CTk):
	def __init__(self) -> None:
		super().__init__()

		self.owo = OwOifier()

		self.title("OwOifier")
		self.geometry(f'{440}x{720}')

		set_appearance_mode("system")
		set_default_color_theme("blue")
		self.configure(fg_color=("#ddb6dc", "#1f1f1f"))

		#create widgets
		#text
		self.textFrame = CTkFrame(self)
		self.inputBox = CTkTextbox(self.textFrame, wrap=WORD)
		self.output = CTkTextbox(self.textFrame, wrap=WORD, state=DISABLED)
		self.copyButton = CTkButton(self.textFrame, text="Copy Output", command=self.copyText)
		#menu
		self.menuFrame = CTkFrame(self)
		#slider
		self.sliderFrame = CTkFrame(self.menuFrame)
		self.stutterSlider = CTkSlider(self.sliderFrame, from_=0, to=99, number_of_steps=99, command=self.updateStutter)
		self.prefixSlider = CTkSlider(self.sliderFrame, from_=0, to=99, number_of_steps=99, command=self.updatePrefix)
		self.suffixSlider = CTkSlider(self.sliderFrame, from_=0, to=99, number_of_steps=99, command=self.updateSuffix)
		self.stutterLabel = CTkLabel(self.sliderFrame)
		self.prefixLabel = CTkLabel(self.sliderFrame)
		self.suffixLabel = CTkLabel(self.sliderFrame)
		#checkbox
		self.checkboxFrame = CTkFrame(self.menuFrame)
		self.LRToWCheck = CTkCheckBox(self.checkboxFrame, text="L's and R's Converted to W's", command=self.updateLRToW)
		self.YAfterNCheck = CTkCheckBox(self.checkboxFrame, text="Vowels After N's Become Y's", command=self.updateYAfterN)
		self.repeatAfterYCheck = CTkCheckBox(self.checkboxFrame, text="Repeat Words Ending with Y", command=self.updateRepeatAfterY)
		self.replaceWordsCheck = CTkCheckBox(self.checkboxFrame, text="Replace Words", command=self.updateReplaceWords)
		#input button
		self.inputButton = CTkButton(self.menuFrame, text="OwOify!!", command=self.updateText)

		#set defaults
		#set slider defaults
		self.stutterSlider.set(15)
		self.prefixSlider.set(15)
		self.suffixSlider.set(15)
		self.updateStutter(self.stutterSlider.get())
		self.updateSuffix(self.prefixSlider.get())
		self.updatePrefix(self.suffixSlider.get())
		#checkboxes are checked by default
		self.LRToWCheck.select()
		self.YAfterNCheck.select()
		self.repeatAfterYCheck.select()
		self.replaceWordsCheck.select()

		#setting colors
		self.menuFrame.configure(fg_color=("#ddb6dc", "#1f1f1f"))
		self.textFrame.configure(fg_color="transparent")
		self.sliderFrame.configure(fg_color="transparent")
		self.checkboxFrame.configure(fg_color="transparent")
		self.inputButton.configure(fg_color="#9e2e96", hover_color="#7f2478")
		self.copyButton.configure(fg_color="#9e2e96", hover_color="#7f2478")
		self.stutterSlider.configure(button_color="#9e2e96", progress_color="#9e2e96", button_hover_color="#7f2478")
		self.prefixSlider.configure(button_color="#9e2e96", progress_color="#9e2e96", button_hover_color="#7f2478")
		self.suffixSlider.configure(button_color="#9e2e96", progress_color="#9e2e96", button_hover_color="#7f2478")
		self.LRToWCheck.configure(fg_color="#9e2e96", hover_color="#7f2478")
		self.YAfterNCheck.configure(fg_color="#9e2e96", hover_color="#7f2478")
		self.repeatAfterYCheck.configure(fg_color="#9e2e96", hover_color="#7f2478")
		self.replaceWordsCheck.configure(fg_color="#9e2e96", hover_color="#7f2478")

		#placing widgets in grid layout
		#text
		self.textFrame.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky=NSEW)
		self.inputBox.grid(row=0, column=0, pady=(0, 20), sticky=NSEW)
		self.output.grid(row=1, column=0, sticky=NSEW)
		self.copyButton.grid(row=2, column=0, padx=20, sticky=E)
		#menu
		self.menuFrame.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20))
		#slider
		self.sliderFrame.grid(row=0, column=0, columnspan=2)
		self.stutterLabel.grid(row=0, column=0, sticky=NSEW)
		self.prefixLabel.grid(row=0, column=1, sticky=NSEW)
		self.suffixLabel.grid(row=0, column=2, sticky=NSEW)
		self.stutterSlider.grid(row=1, column=0, sticky=NSEW)
		self.prefixSlider.grid(row=1, column=1, sticky=NSEW)
		self.suffixSlider.grid(row=1, column=2, sticky=NSEW)
		#checkbox
		self.checkboxFrame.grid(row=1, column=0, pady=(10, 0), sticky=W)
		self.LRToWCheck.grid(row=0, column=0, padx=(0, 10), pady=(20, 10), sticky=W)
		self.YAfterNCheck.grid(row=1, column=0, padx=(0, 10), pady=(0, 10), sticky=W)
		self.repeatAfterYCheck.grid(row=2, column=0, padx=(0, 10), pady=(0, 10), sticky=W)
		self.replaceWordsCheck.grid(row=3, column=0, padx=(0, 10), sticky=W)
		self.inputButton.grid(row=1, column=1, padx=(10, 0), pady=(10, 0), sticky=NSEW)

		#allow for resizable widgets
		#root
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		#textFrame
		self.textFrame.rowconfigure(0, weight=1)
		self.textFrame.rowconfigure(1, weight=1)
		self.textFrame.columnconfigure(0, weight=1)
		#menuFrame
		self.menuFrame.rowconfigure(1, weight=1)
		self.menuFrame.columnconfigure(1, weight=1)
		#sliderFrame is scalable horizontally only
		self.sliderFrame.columnconfigure(0, weight=1)
		self.sliderFrame.columnconfigure(1, weight=1)
		self.sliderFrame.columnconfigure(2, weight=1)

	#textbox functions
	def updateText(self) -> None:
		self.owo.text = self.inputBox.get('0.0', END)
		self.output.configure(state=NORMAL)
		self.output.delete('0.0', END)
		self.output.insert(INSERT, self.owo.owoify())
		self.output.configure(state=DISABLED)

	def copyText(self) -> None:
		copy(self.output.get('0.0', END))

	#slider functions
	def updateStutter(self, val) -> None:
		self.owo.stutterChance = val / 100
		self.stutterLabel.configure(text=f'Stutter Chance: {val:.0f}%')

	def updatePrefix(self, val) -> None:
		self.owo.prefixChance = val / 100
		self.prefixLabel.configure(text=f'Prefix Chance: {val:.0f}%')

	def updateSuffix(self, val) -> None:
		self.owo.suffixChance = val / 100
		self.suffixLabel.configure(text=f'Suffix Chance: {val:.0f}%')

	#checkbox functions
	def updateLRToW(self) -> None:
		self.owo.LRToW = bool(self.LRToWCheck.get())

	def updateYAfterN(self) -> None:
		self.owo.YAfterN = bool(self.YAfterNCheck.get())

	def updateRepeatAfterY(self) -> None:
		self.owo.repeatAfterY = bool(self.repeatAfterYCheck.get())

	def updateReplaceWords(self) -> None:
		self.owo.replaceWords = bool(self.replaceWordsCheck.get())


if __name__ in "__main__":
	app = App()
	app.mainloop()
