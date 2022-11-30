import multiprocessing.pool
import os.path
import shutil
import sys
import time

import pyautogui
import selenium.webdriver
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor
import requests

import MyUtils


def Cache():
    MyUtils.CreatePath(f'{path}/clip')
    f = MyUtils.txt('D:/Kaleidoscope/影视/cache.txt')
    l = f.l
    global HostUrl, CurrentEP
    HostUrl = l[0].strip('\n')
    CurrentEP = int(l[1].strip('\n'))
    global step
    step = int(l[2])


def GetM3U8andInfo():
    global name, CurrentEP, TotalEP, HostUrl
    pageo = MyUtils.Chrome(HostUrl, mine=1)
    pageo.maximize()
    page = pageo.driver
    time.sleep(1)
    name = MyUtils.Element([page, By.XPATH, '/html/body/div[2]/div[1]/header/img']).get_attribute('alt')
    name = name.replace(' ', '')
    TotalEP = len(MyUtils.Elements([page, By.XPATH, '/html/body/div[2]/div[1]/div[2]/div/div/div[2]/ul[1]/li']))
    MyUtils.delog(f'获取参数{name},{CurrentEP}/{TotalEP}')
    # 如果已存在路径，直接检索，并把CurrentEP==1更新为CurrentEP
    # if os.path.exists(baijiahao'../影视/{name}'):
    #     for root, dirs, files in os.walk(baijiahao'../影视/{name}'):
    #         CurrentEP = len(files) + 1
    #         if CurrentEP > TotalEP:
    #             sys.exit()
    #         break
    MyUtils.CreatePath(f'./影视/{name}')
    # 如果存在m3u8直接退出
    if os.path.exists(f'C:/Users/{MyUtils.user}/Downloads/m3u8.txt'):
        return
    # 点击当前EP按钮，多点几次
    MyUtils.clickelement([page, By.XPATH, f'/html/body/div[2]/div[1]/div[2]/div/div/div[2]/ul/li[{CurrentEP}]'])
    pageo.switchto(0)
    time.sleep(1)
    MyUtils.clickelement([page, By.XPATH, f'/html/body/div[2]/div[1]/div[2]/div/div/div[2]/ul/li[{CurrentEP}]'])

    if MyUtils.Element([page, By.XPATH, '/html/body/div/div/div/img'], depth=9):
        MyUtils.clickelement([page, By.XPATH, '/html/body/div/div/div/img'])
    # 再检查一次m3u8，如果此时手动下载了，直接退出
    time.sleep(5)
    if os.path.exists(f'C:/Users/{MyUtils.user}/Downloads/m3u8.txt'):
        return
    time.sleep(0)
    pyautogui.hotkey('alt', 'g')
    time.sleep(2)
    # 如果存在m3u8直接退出
    if os.path.exists(f'C:/Users/{MyUtils.user}/Downloads/m3u8.txt'):
        return
    # 判断，多集需要点下一个m3u8
    global step
    if TotalEP == CurrentEP:
        pyautogui.click(1726, 99)
        time.sleep(3)
        pyautogui.click(1690, 99)
    else:
        pyautogui.click(1726, 99 + (step - 1) * 50)
        time.sleep(3)
        pyautogui.click(1690, 99 + (step - 1) * 50)
    time.sleep(2)
    page.switch_to.window(page.window_handles[-1])
    # 可能出现子集链接m3u8
    PossibleElement = MyUtils.Element([page, By.XPATH, '/html/body/div/table/tbody/tr[2]/td/div[3]/p/a'], depth=8)
    if not PossibleElement == None:
        PossibleElement.clickelement()
    time.sleep(1)
    MyUtils.delog('开始点击m3u8下载按钮')
    MyUtils.clickelement([page, By.XPATH, '/html/body/div/button[1]'])
    time.sleep(5)
    time.sleep(3)
    if os.path.exists(f'C:/Users/{MyUtils.user}/Downloads/m3u8.txt'):
        return
    page.quit()
    GetM3U8andInfo()


def Download():
    Sections = MyUtils.txt('r', f'C:/Users/{MyUtils.user}/Downloads/m3u8.txt').l
    MyUtils.delog('开始下载')
    inc = 0
    e = MyUtils.pool(30)
    for url in Sections:
        inc += 1
        if os.path.exists(path + f'/{inc}.mp4'):
            MyUtils.log(f'{name}：EP{CurrentEP}:{inc}/{len(Sections)}  Path:{os.path.abspath(path)}')
            continue
        # MyUtils.MyPageDownload(url,path + baijiahao'/{inc}.mp4')
        e.doorwait(MyUtils.requestdownload, path + f'/{inc}.mp4', 'wb', url)
        # print(baijiahao'{name}：EP{CurrentEP}:{inc}/{len(Sections)}  Path:{os.path.abspath(path)}下载中')
    MyUtils.log(f'等待下载完成（剩余working: ）')
    # while not os.path.exists(os.path.abspath(path+baijiahao'/{inc}.mp4')):
    #     # print(baijiahao'等待{path+baijiahao"/{inc}.mp4"}下载完成中')
    #     time.sleep(5)

    MyUtils.delog('下载完毕，开始重写和组合')


def Combine():
    L = []
    count = 0
    clipcount = 0
    str = ''
    for root, dirs, files in os.walk(path):
        # 不执行条件
        if os.path.exists(f'{path}/output.mp4'):
            break

        files.sort(key=lambda x: int(x.replace('.mp4', '')))
        for file in files:
            count += 1
            # 去掉虚假图片头
            l = MyUtils.file('rb', path + '/' + file)
            # 无关字节数组长度统计
            sum = 0
            index = MyUtils.MyBiFind(path + '/' + file)
            try:
                while len(l[0]) < index:
                    sum += len(l[0])
                    l.pop(0)
                l[0] = l[0][index - sum:]
                MyUtils.file('wb', path + '/' + file, l)
                print(f'{file}/{len(files)}已重写')
                str += path + '/' + file + '|'
            except:
                print(f'Error when recomposing file: {file}')
                os.remove(path + '/' + file)
                sys.exit()
            # 每200个合并一个clip.mp4
            if count >= 200:
                count = 0
                clipcount += 1
                if not os.path.exists(f'{path}/clip/{clipcount}.mp4'):
                    os.system(f'ffmpeg -i "concat:{str}" -acodec copy -vcodec copy -absf aac_adtstoasc {path}/clip/{clipcount}.mp4')
                str = ''
        break
    if not os.path.exists(f'{path}/clip/{clipcount + 1}.mp4'):
        os.system(f'ffmpeg -i "concat:{str}" -acodec copy -vcodec copy -absf aac_adtstoasc {path}/clip/{clipcount + 1}.mp4')
    str = ''

    # 合成ts
    for root, dirs, files in os.walk(f'{path}/clip'):
        for file in files:
            if not os.path.exists(f'{path}/clip/{file.replace("mp4", "ts")}'):
                os.system(f'ffmpeg -i {path}/clip/{file} -vcodec copy -acodec copy -vbsf h264_mp4toannexb {path}/clip/{file.replace("mp4", "ts")}')
                str += path + '/clip/' + file.replace("mp4", "ts") + '|'

    # 合并到机械硬盘
    os.system(f'ffmpeg -i "concat:{str}" -acodec copy -vcodec copy -absf aac_adtstoasc ' + f'../影视/{name}/EP{CurrentEP}.mp4')


def Remove():
    global path
    # 去除m3u8
    os.remove(f'C:/Users/{MyUtils.user}/Downloads/m3u8.txt')
    # 去除clip里的
    for root, dirs, files in os.walk(f'{path}/clip'):
        for file in files:
            os.remove(f'{path}/clip/{file}')
    # 去除所有小视频
    for root, dirs, files in os.walk(path):
        for file in files:
            os.remove(f'{path}/{file}')
    # 重置HostUrl
    HostUrl = ''


def main():
    # 初始化
    global HostUrl, path, CurrentEP, TotalEP
    HostUrl = ''
    path = 'D:/standardizedPF/Spectrum'
    while True:
        CurrentEP = 1
        if HostUrl == '':
            # 获取HostUrl,CurrentEP
            Cache()
        TotalEP = 99
        while CurrentEP <= TotalEP:
            MyUtils.CreatePath(path)
            GetM3U8andInfo()  # 获取TotalUrl,M3U8,名字
            while not os.path.exists(f'C:/Users/{MyUtils.user}/Downloads/m3u8.txt'):
                GetM3U8andInfo()  # 获取TotalUrl,M3U8,名字
            Download()
            MyUtils.delog(-1)
            Combine()
            # 1EP结束
            CurrentEP += 1
            Remove()
            MyUtils.file('w', f'../影视/cache.txt', [str(HostUrl) + '\n', str(CurrentEP) + '\n', str(step) + '\n'])
        HostUrl = input('输入新的蛋蛋赞电影网址：')
        MyUtils.file('w', f'../影视/cache.txt', [str(HostUrl) + '\n', str(CurrentEP) + '\n', str(step) + '\n'])


if __name__ == '__main__':
    main()
