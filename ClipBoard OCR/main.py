from PIL import ImageGrab, Image
import os
import pytesseract as tess
from pynput import keyboard
from time import sleep

cmb = [{keyboard.Key.shift, keyboard.KeyCode(char='r')}, {
    keyboard.Key.shift, keyboard.KeyCode(char='R')}]
current = set()
dir = os.getcwd()

print("Press Shift + R to Perform OCR on clipboard Image.\nResults Will be copied to clipboard.\n")


def execute():
    try:
        tess.pytesseract.tesseract_cmd = r'C:\Users\RISHABH SHAH\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
        im = ImageGrab.grabclipboard()
        im.save(dir+'\image.png', 'PNG')
        im = Image.open(dir+'\image.png')
        text = tess.image_to_string(im)
        text = text[:-1].replace('\n', " ").replace('  ', '')
        print('Results:', text, '\n')
        copyToClipBoard(text)
        os.remove(dir+'\image.png')
    except Exception as e:
        print('First Item on Clipboard is not an Image.')
        sleep(5)


def copyToClipBoard(text):
    command = 'echo ' + text + '| clip'
    os.system(command)


def onPress(key):
    if any([key in z for z in cmb]):
        current.add(key)
        if any(all(k in current for k in z) for z in cmb):
            print('Performing OCR.Please Wait...\n')
            execute()


def onRelease(key):
    if any([key in z for z in cmb]):
        current.remove(key)


with keyboard.Listener(on_press=onPress, on_release=onRelease) as listener:
    listener.join()
