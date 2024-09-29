from time import sleep

from win10toast import ToastNotifier
from os import getenv,startfile
from webbrowser import open
from keyboard import press_and_release, block_key, unblock_key
from dotenv import load_dotenv
from threading import Thread
from pyautogui import moveTo,FAILSAFE
from sys import exit
import pyautogui
pyautogui.FAILSAFE = False
from requests import Session
from random import randint

load_dotenv(r"C:\Users\yassi\Downloads\PythonScripts\Focus\Focus\settings.env")
token = getenv('token')
id_ = getenv('id')
toaster = ToastNotifier()

session = Session()

mouse_move = True

def move_mouse():
    while True:
       moveTo(800, 600)

def send_message(message):
    print(f"Sending....{message}")
    url = f"https://api.telegram.org/bot{token}"
    params = {"chat_id": id_, "text": message}
    session.get(url + "/sendMessage", params=params)


def focus():
    print("Focus Initiated!")
    send_message("Laptop Locked!")
    toaster.show_toast("Warning", "App closing...", duration=2)
    press_and_release("win+d")
 
    try:
        for i in range(200):
            block_key(i)
    except Exception as e:
        print(e)
        send_message(str(e))
    toaster.show_toast("Go Do Something", "App Closed!", duration=2)
    sleep(randint(300,400))
    try:
        for i in range(200):
            unblock_key(i)
    except Exception as e:
        print(e)
    toaster.show_toast("Hello There!", "Welcome Back", duration=2)
    send_message("Laptop Unlocked!")

focus()

if __name__ == "__main__":
    move_mouse_thread = Thread(target=move_mouse, daemon=True)
    

    while True:
        sleep(3600) #45 minutes 
        toaster.show_toast("Warning", "5 Minutes Left To Lock", duration=2)
        sleep(240)
        toaster.show_toast("Warning", "1 Minute Left To Lock", duration=3)
        send_message("Laptop Locking In One Minute")
        sleep(60)
        move_mouse_thread.start()
        focus_thread = Thread(target=focus)
        focus_thread.start()
        focus_thread.join()
        startfile(r'C:\Users\yassi\Downloads\PythonScripts\Focus\Focus\main.pyw')
        sleep(2.5)
        exit()
        

        
