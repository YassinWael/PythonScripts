from pyautogui import screenshot
from time import sleep
from pynput import keyboard
from os import path, listdir
import winsound
english_path = 'Random/screenshots/english'



def on_press(key,subject="English"):
    print(key)
    if key.char == "p":
        if subject == "English":
            file_prefix = len(listdir(english_path)) + 1
            file_name = f"{english_path}/screenshot_{file_prefix}.png"
            screenshot(file_name)
            winsound.PlaySound("click.wav", winsound.SND_ALIAS)

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()