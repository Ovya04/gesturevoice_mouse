import pyautogui
import os
import time

def left_click():
    pyautogui.click()

def right_click():
    pyautogui.rightClick()

def scroll_up():
    pyautogui.scroll(300)

def scroll_down():
    pyautogui.scroll(-300)

def double_click():
    pyautogui.doubleClick()

def open_notepad():
    os.system("notepad")

def open_browser():
    os.system("start chrome")

def type_text(text):
    pyautogui.write(text, interval=0.05)
