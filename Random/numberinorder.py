from pyautogui import typewrite,press
from time import sleep

i = 2
sleep(2)

while True:
    typewrite(str(i))
    i+=1
    press("Enter")
    sleep(1.5)