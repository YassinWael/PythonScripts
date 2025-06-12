from pyautogui import screenshot
from time import sleep
from pynput import keyboard
from os import path, listdir
import winsound
english_path = r'C:\Users\yassi\Downloads\PythonScripts - Copy\Random\screenshots\english'



def on_press(key):
    print(key)
    try:
        if key.char == "-":
            
                file_prefix = len(listdir(english_path)) + 1
                file_name = f"{english_path}/screenshot_{file_prefix}.png"
                print("Taking screenshot for English subject...")
                screenshot(file_name)
                print(f"Screenshot saved as {file_name}")
                winsound.PlaySound("click.wav", winsound.SND_ALIAS)
           
    except AttributeError:
        pass
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()