from pyautogui import locateCenterOnScreen
from time import sleep
from os import system
from webbrowser import open
while True:
    sleep(0.15)
    loc = (locateCenterOnScreen(r'C:\Users\yassi\Downloads\PythonScripts\Focus\Focus\Untitled.png', confidence=0.85))
    loc2 = (locateCenterOnScreen(r'C:\Users\yassi\Downloads\PythonScripts\Focus\Focus\Untitled2.png', confidence=0.85))
    loc3 = (locateCenterOnScreen(r'C:\Users\yassi\Downloads\PythonScripts\Focus\Focus\Untitled3.png', confidence=0.85))
    if loc or loc2 or loc3:
        system("shutdown -s -t 0")
        print(loc,loc2)
        
    else:
        print(loc,loc2)