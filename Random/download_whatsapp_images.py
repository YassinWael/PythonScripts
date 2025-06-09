from pyautogui import leftClick,position,moveTo
from time import sleep
from os import startfile
from pyautogui import locateCenterOnScreen



image_count = int(input("How many images are you downloading?"))
sleep(3)
image_button = locateCenterOnScreen("Random\download_button.png", confidence=0.9,grayscale=True)
#microsoft edge 
for _ in range(image_count):
    leftClick(image_button[0], image_button[1])
    sleep(1.2)
    leftClick(x=1800, y=557)
    sleep(1.2)

