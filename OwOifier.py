from random import random, choice
from pyperclip import copy
from lorem import sentence
from customtkinter import *


class OwOifier:
	def __init__(self, inputText='', LRToWs=True, YAfterNs=True, repeatAfterYs=True, replaceWords=True, stutterChance=0.15, prefixChance=0.15, suffixChance=0.15) -> None:
		self.inputText = inputText
		self.LRToWs = LRToWs
		self.YAfterNs = YAfterNs
		self.repeatAfterYs = repeatAfterYs
		self.replaceWords = replaceWords
		self.stutterChance = stutterChance
		self.prefixChance = prefixChance
		self.suffixChance = suffixChance
		self.replacements = {
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
		self.prefixes = [
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
		self.suffixes = [
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
		self.noTranslations = [
			'lol',
			'lmao',
			'lmfao',
		]

	def owoify(self) -> str:
		text = self.inputText.splitlines()
		text = [line.split() for line in text]
		for line in range(len(text)):
			word = 0
			while word < len(text[line]):
				alpha = self.findAlpha(text[line][word])
				if 1 not in alpha:
					word += 1
					continue
				if self.replaceWords:
					text[line][word] = self.replaceWord(text[line][word])
				text[line][word] = self.dontTranslate(text[line][word])
				text[line][word], word, escape = self.removeEscape(text[line][word], word)
				if escape:
					word += 1
					continue
				if self.LRToWs:
					text[line][word] = self.LRToW(text[line][word])
				if self.YAfterNs:
					text[line][word] = self.YAfterN(text[line][word])
				if self.repeatAfterYs:
					text[line], word = self.repeatAfterY(text[line], word)
				if 0 not in alpha:
					if 0 < self.stutterChance < 1:
						text[line][word] = self.addStutter(text[line][word])
				if 0 < self.prefixChance < 1:
					text[line], word = self.addPrefix(text[line], word)
				if 0 < self.suffixChance < 1:
					text[line], word = self.addSuffix(text[line], word)
				word += 1
		text = [' '.join(line) for line in text]
		text = '\n'.join(text)
		return text

	def findAlpha(self, word: str) -> set[int]:
		return {int(alpha.isalpha()) for alpha in word}

	def replaceWord(self, word: str) -> str:
		if word.lower() in self.replacements:
			word = self.replacements[word.lower()].upper() if word.isupper() else self.replacements[word.lower()]
			word = f'${word}$'
		return word

	def dontTranslate(self, word: str) -> str:
		if word in self.noTranslations:
			word = f'${word}$'
		return word

	def removeEscape(self, word: str, index: int) -> tuple[str, int, bool]:
		escape = word.startswith('$') and word.endswith('$')
		if escape:
			word = word.replace('$', '')
		return word, index, escape

	def LRToW(self, word: str) -> str:
		word = word.replace('l', 'w')
		word = word.replace('r', 'w')
		return word

	def YAfterN(self, word: str) -> str:
		for char in range(len(word) - 2):
			if word[char].lower() == 'n':
				if word[char+1].lower() in ['a', 'e', 'i', 'o', 'u']:
					word = word[:char+1] + word[char+2].replace(word[char+2], 'y') + word[char+1:]
		return word

	def repeatAfterY(self, line: list[str], index: int) -> tuple[list[str], int]:
		if len(line[index]) > 3:
			if line[index][-1].lower() == 'y':
				line.insert(index+1, 'w' + line[index][1:])
				index += 1
		return line, index

	def addStutter(self, word: str) -> str:
		stutter = []
		count, countChance = 1, 0
		while True:
			if random() < self.stutterChance:
				if random() < countChance:
					count += 1
					countChance = 0.10
				if count < len(word):
					stutter.append(word[:count])
					countChance += 0.10
				else:
					break
			else:
				break
		stutter.append(word)
		word = '-'.join(stutter)
		return word

	def addPrefix(self, line: list[str], index: int) -> tuple[list[str], int]:
		if random() < self.prefixChance:
			line.insert(index - 1, choice(self.prefixes))
		return line, index + 1

	def addSuffix(self, line: list[str], index: int) -> tuple[list[str], int]:
		if random() < self.suffixChance:
			line.insert(index+1, choice(self.suffixes))
		return line, index + 2


class App(CTk):
	def __init__(self) -> None:
		super().__init__()

		self.owo = OwOifier()

		self.title("OwOifier")
		self.geometry(f'{440}x{720}')

		set_appearance_mode("system")
		set_default_color_theme("blue")
		self.configure(fg_color=("#ddb6dc", "#1f1f1f"))

		# create widgets
		# text
		self.textFrame = CTkFrame(self)
		self.inputBox = CTkTextbox(self.textFrame, wrap=WORD)
		self.output = CTkTextbox(self.textFrame, wrap=WORD, state=DISABLED)
		self.copyButton = CTkButton(self.textFrame, text="Copy Output", command=self.copyText)
		self.loremIpsumButton = CTkButton(self.textFrame, text="Lorem Ipsum", command=self.loremIpsum)
		# menu
		self.menuFrame = CTkFrame(self)
		# slider
		self.sliderFrame = CTkFrame(self.menuFrame)
		self.stutterSlider = CTkSlider(self.sliderFrame, from_=0, to=99, number_of_steps=99, command=self.updateStutter)
		self.prefixSlider = CTkSlider(self.sliderFrame, from_=0, to=100, number_of_steps=100, command=self.updatePrefix)
		self.suffixSlider = CTkSlider(self.sliderFrame, from_=0, to=100, number_of_steps=100, command=self.updateSuffix)
		self.stutterLabel = CTkLabel(self.sliderFrame)
		self.prefixLabel = CTkLabel(self.sliderFrame)
		self.suffixLabel = CTkLabel(self.sliderFrame)
		# checkbox
		self.checkboxFrame = CTkFrame(self.menuFrame)
		self.LRToWCheck = CTkCheckBox(self.checkboxFrame, text="L's and R's Converted to W's", command=self.updateLRToW)
		self.YAfterNCheck = CTkCheckBox(self.checkboxFrame, text="Vowels After N's Become Y's", command=self.updateYAfterN)
		self.repeatAfterYCheck = CTkCheckBox(self.checkboxFrame, text="Repeat Words Ending with Y", command=self.updateRepeatAfterY)
		self.replaceWordsCheck = CTkCheckBox(self.checkboxFrame, text="Replace Words", command=self.updateReplaceWords)
		# input button
		self.inputButton = CTkButton(self.menuFrame, text="OwOify!!", command=self.updateText)

		# set defaults
		# set slider defaults
		self.stutterSlider.set(15)
		self.prefixSlider.set(15)
		self.suffixSlider.set(15)
		self.updateStutter(self.stutterSlider.get())
		self.updateSuffix(self.prefixSlider.get())
		self.updatePrefix(self.suffixSlider.get())
		# checkboxes are checked by default
		self.LRToWCheck.select()
		self.YAfterNCheck.select()
		self.repeatAfterYCheck.select()
		self.replaceWordsCheck.select()

		# setting colors
		self.menuFrame.configure(fg_color=("#ddb6dc", "#1f1f1f"))
		self.textFrame.configure(fg_color="transparent")
		self.sliderFrame.configure(fg_color="transparent")
		self.checkboxFrame.configure(fg_color="transparent")
		self.inputButton.configure(fg_color="#9e2e96", hover_color="#7f2478")
		self.copyButton.configure(fg_color="#9e2e96", hover_color="#7f2478")
		self.loremIpsumButton.configure(fg_color="#9e2e96", hover_color="#7f2478")
		self.stutterSlider.configure(button_color="#9e2e96", progress_color="#9e2e96", button_hover_color="#7f2478")
		self.prefixSlider.configure(button_color="#9e2e96", progress_color="#9e2e96", button_hover_color="#7f2478")
		self.suffixSlider.configure(button_color="#9e2e96", progress_color="#9e2e96", button_hover_color="#7f2478")
		self.LRToWCheck.configure(fg_color="#9e2e96", hover_color="#7f2478")
		self.YAfterNCheck.configure(fg_color="#9e2e96", hover_color="#7f2478")
		self.repeatAfterYCheck.configure(fg_color="#9e2e96", hover_color="#7f2478")
		self.replaceWordsCheck.configure(fg_color="#9e2e96", hover_color="#7f2478")

		# placing widgets in grid layout
		# text
		self.textFrame.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky=NSEW)
		self.inputBox.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky=NSEW)
		self.output.grid(row=1, column=0, columnspan=2, sticky=NSEW)
		self.loremIpsumButton.grid(row=2, column=0, sticky=W)
		self.copyButton.grid(row=2, column=1, padx=20, sticky=E)
		# menu
		self.menuFrame.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20))
		# slider
		self.sliderFrame.grid(row=0, column=0, columnspan=2)
		self.stutterLabel.grid(row=0, column=0, sticky=NSEW)
		self.prefixLabel.grid(row=0, column=1, sticky=NSEW)
		self.suffixLabel.grid(row=0, column=2, sticky=NSEW)
		self.stutterSlider.grid(row=1, column=0, sticky=NSEW)
		self.prefixSlider.grid(row=1, column=1, sticky=NSEW)
		self.suffixSlider.grid(row=1, column=2, sticky=NSEW)
		# checkbox
		self.checkboxFrame.grid(row=1, column=0, pady=(10, 0), sticky=W)
		self.LRToWCheck.grid(row=0, column=0, padx=(0, 10), pady=(20, 10), sticky=W)
		self.YAfterNCheck.grid(row=1, column=0, padx=(0, 10), pady=(0, 10), sticky=W)
		self.repeatAfterYCheck.grid(row=2, column=0, padx=(0, 10), pady=(0, 10), sticky=W)
		self.replaceWordsCheck.grid(row=3, column=0, padx=(0, 10), sticky=W)
		self.inputButton.grid(row=1, column=1, padx=(10, 0), pady=(10, 0), sticky=NSEW)

		# allow for resizable widgets
		# root
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		# textFrame
		self.textFrame.rowconfigure(0, weight=1)
		self.textFrame.rowconfigure(1, weight=1)
		self.textFrame.columnconfigure(0, weight=1)
		# menuFrame
		self.menuFrame.rowconfigure(1, weight=1)
		self.menuFrame.columnconfigure(1, weight=1)
		# sliderFrame is scalable horizontally only
		self.sliderFrame.columnconfigure(0, weight=1)
		self.sliderFrame.columnconfigure(1, weight=1)
		self.sliderFrame.columnconfigure(2, weight=1)

	# textbox functions
	def updateText(self) -> None:
		self.owo.inputText = self.inputBox.get('0.0', END)
		self.output.configure(state=NORMAL)
		self.output.delete('0.0', END)
		self.output.insert(INSERT, self.owo.owoify())
		self.output.configure(state=DISABLED)

	def copyText(self) -> None:
		copy(self.output.get('0.0', END))

	def loremIpsum(self) -> None:
		self.inputBox.delete('0.0', END)
		self.inputBox.insert('0.0', '\n'.join([sentence() for i in range(10)]))
		self.updateText()

	# slider functions
	def updateStutter(self, val) -> None:
		self.owo.stutterChance = val / 100
		self.stutterLabel.configure(text=f'Stutter Chance: {val:.0f}%')

	def updatePrefix(self, val) -> None:
		self.owo.prefixChance = val / 100
		self.prefixLabel.configure(text=f'Prefix Chance: {val:.0f}%')

	def updateSuffix(self, val) -> None:
		self.owo.suffixChance = val / 100
		self.suffixLabel.configure(text=f'Suffix Chance: {val:.0f}%')

	# checkbox functions
	def updateLRToW(self) -> None:
		self.owo.LRToWs = bool(self.LRToWCheck.get())

	def updateYAfterN(self) -> None:
		self.owo.YAfterNs = bool(self.YAfterNCheck.get())

	def updateRepeatAfterY(self) -> None:
		self.owo.repeatAfterYs = bool(self.repeatAfterYCheck.get())

	def updateReplaceWords(self) -> None:
		self.owo.replaceWords = bool(self.replaceWordsCheck.get())


if __name__ in "__main__":
	app = App()
	app.mainloop()
