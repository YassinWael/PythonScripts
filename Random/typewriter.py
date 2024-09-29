from pyautogui import typewrite
from time import sleep
text = input("Text you would like to type: ")
sleep(3)
print(f"Writing {text}...")
typewrite(text.strip())
print("Finished writing successfully")