# OwOifier
OwO What's this? An app that converts text to OwO speak ?? Woah !!

## How to Use
**OwOifier.exe and settings.yml must be in the same folder.**

1. Enter text in the left box.
2. Change the settings in the middle.
3. Hit the "OwOify!!" button to genenerate the text.
You can hit the "Copy Output" button to copy the generated text to your clipboard.
The "Random Copypasta" button can be hit to add a copypasta to the input box.

The settings file, using [YAML](https://quickref.me/yaml), can be used to 
- Set defaults for the app upon launch.
- Add prefixes, suffixes, and copypastas.
- Set word replacements. Such as, `thanks` -> `thx`.
- Mark words to not be translated.
  
Use `$` around **words*** to mark them to not translate. For example, 
```
>>> "$Discord$ $Kitten$: Thanks mister"
... "Discord Kitten: Thx mister"
```
* The limitation of only being able to mark individual words will be fixed in a later version.
