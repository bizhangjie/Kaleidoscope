import time
# 留姜来
import pyautogui

import MyUtils

if __name__ == '__main__':
    for i in range(2):
        duration=0
        pyautogui.keyDown('ctrl')
        MyUtils.click(1644,199)
        time.sleep(duration)
        MyUtils.click(1644,399)
        time.sleep(duration)
        MyUtils.click(1644,599)
        time.sleep(duration)
        MyUtils.click(1644,799)
        time.sleep(duration)
        pyautogui.keyUp('ctrl')
        MyUtils.scroll(1500, x=1800, y=200)
        MyUtils.scroll(-400,x=1800,y=200)
        time.sleep(2)
