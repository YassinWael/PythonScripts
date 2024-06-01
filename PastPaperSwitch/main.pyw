from pyautogui import leftClick, hotkey
from pyperclip import copy, paste
from keyboard import on_press, wait
from time import sleep


def switch_to_ms():
    leftClick(x=644, y=66)
    sleep(0.15)

    hotkey('ctrl', 'c')
    sleep(0.15)

    mainLink = paste()

    if 'QP' in mainLink:
        mainLink = mainLink.replace('QP', 'MS')
    else:
        mainLink = mainLink.replace('qp', 'ms')

    copy(mainLink)
    sleep(0.15)

    hotkey('ctrl', 'v')
    hotkey('enter')


def on_key_press(event):
    if event.name == 'clear':
        switch_to_ms()


on_press(on_key_press)

wait()