import time

import pyautogui
import pyperclip

import MyUtils





if __name__ == '__main__':
    pyautogui.hotkey('alt','tab')
    time.sleep(0.2)
    for i in range(1):
        MyUtils.click(524,59)
        pyautogui.hotkey('ctrl','c')
        MyUtils.provisionalout(pyperclip.paste())
        pyautogui.hotkey('ctrl','w')
        time.sleep(1)
    pyautogui.hotkey('alt','tab')


