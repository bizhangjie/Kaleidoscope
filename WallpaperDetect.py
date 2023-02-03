import time

import pyautogui
import pyperclip

import WallpaperUtils

readytodownload = WallpaperUtils.readytodownload
repeat=2

def fun():
    pass


# 对wallpaper网站进行最大化后自动化，alt+tab，点击复制网址，关闭网页，依次加入到txt
def main():
    fun()
    for i in range(repeat):
        # 复制网址并关闭网页
        pyautogui.click(1075, 72)
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'w')
        time.sleep(0.2)
        readytodownload.add({''
                             : [pyperclip.paste()]})


pyautogui.hotkey('alt', 'tab')

if __name__ == '__main__':
    main()
