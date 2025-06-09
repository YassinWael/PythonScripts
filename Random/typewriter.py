from pyautogui import typewrite
from time import sleep
from random import uniform
text = input("Text you would like to type: ")
sleep(2)
print(f"Writing {text}...")
# typewrite(text.strip(),interval=0.0925)
typewrite(text.strip())
print("Finished writing successfully")

