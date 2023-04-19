import concurrent.futures
import csv
import datetime
import inspect
import json
import multiprocessing
import os
import random
import re
import shutil
import subprocess
import sys
import time
import zipfile
from glob import glob
import winshell
from win32com.client import Dispatch

import PIL
import PySimpleGUI
import cv2
import moviepy
import numpy
import openpyxl
import pyautogui
import pyperclip
import requests
import selenium
import urllib3
import win32api
import win32con
from PIL import ImageGrab
from moviepy.editor import VideoFileClip
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from functools import wraps

# 初始化1
# region
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

Logcount = 0
global debug
debug = sys.gettrace()
MyError = selenium.common.exceptions.TimeoutException
# 不包括 SystemExit，因为默认通过这个来强行中止严重错误
retrylist = [
    MyError, selenium.common.exceptions.ElementClickInterceptedException,
    Exception, ConnectionRefusedError,
    urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError,
    selenium.common.exceptions.TimeoutException,
    selenium.common.exceptions.NoSuchWindowException, pyautogui.FailSafeException,
]
headers = {
    # 'user-agent': txt(projectpath('user-agent.txt')).l[0],
    'user-agent': '',
    'cookie': ''
}


# endregion


# 参考代码
# region
# 列表传参法是可行的，只不过最好不要传不是自定义的类
# 如果传参已经是列表就不要再列表传参。直接在函数内使用index。不要在函数内声明，这样会直接创建新的局部变量
# 不建议传递列表进行写。列表本身的大小不能在函数内再改变。字典应该也是同理。
# '//div[starts-with(@style,"transform:")]'
# './div[starts-with(@style,"transform:")]'
#
# endregion

# 注解
# region
# 使用json保存配置文件，进行关键字参数覆盖
def useState(fn):
    @wraps(fn)
    def wrapper(*args, config=True, **kwargs):

        if config:
            config = jsondata(jsonpath(fn.__name__))

            # 获取函数定义时关键字参数默认值
            defaults = fn.__defaults__ or ()
            default_values = dict(
                zip(fn.__code__.co_varnames[:fn.__code__.co_argcount][-len(defaults):], defaults))

            # jsondata config 覆盖
            for k, v in config.data.items():
                if k in default_values:
                    default_values[k] = v

            # 调用处代码覆盖
            default_values.update(kwargs)

            # 构造新的参数列表
            new_args = []
            for arg in args:
                if arg in default_values:
                    new_args.append(default_values[arg])
                    del default_values[arg]
                else:
                    new_args.append(arg)

            # 将剩余的默认值添加到kwargs中
            kwargs.update(default_values)

            # 调用原始函数
            return fn(*new_args, **kwargs)
        else:
            return fn(*args, **kwargs)

    return wrapper


# 多名函数
def newname(func):
    @wraps(func)
    def wrapper(originalfunc, *a, **b):
        return originalfunc(*a, **b)

    return wrapper


# 只有一个参数，如果有多个，则重复执行函数，或者空参数
def multisingleargs(func):
    @wraps(func)
    def wrapper(*a):
        res = []
        if a in [None, (), []]:
            return func()
        for i in a:
            res.append(func(i))
        return res

    return wrapper



def listed(func):
    """
    最后一个参数可以是列表以重复执行
    @param func:
    @return:
    """
    @wraps(func)
    def wrapper(*a, **c):
        res = []
        if a in [None, (), []]:
            return func()
        if type(a[-1]) == list:
            b = a[:-1]
            for i in a[-1]:
                ret = (func(*b, i, **c))
                if not type(ret) == list:
                    res.append(ret)
                else:
                    res += ret
            return res
        else:
            return func(*a, **c)

    return wrapper


# 计算调试时函数的消耗时间
def DebugConsume(func):
    def wrapper(*a, **b):
        def inner1(f, *a, **b):
            ret = f(*a, **b)
            stole = nowstr()
            filename1 = filename(inspect.getframeinfo(inspect.currentframe().f_back.f_back)[0])
            filename1 = rmtail(filename1, '.py')
            funcname1 = inspect.getframeinfo(inspect.currentframe().f_back.f_back)[2]
            funcname2 = None
            try:
                funcname2 = inspect.getframeinfo(inspect.currentframe().f_back.f_back)[3]
                funcname2 = (funcname2[0])
                funcname2 = funcname2[funcname2.find('.') + 1:funcname2.find('(')]
            except:
                pass
            if counttime(stole) > 1:
                delog(f'函数{filename1}.{funcname1}/.{funcname2} 所消耗的时间：{int(counttime(stole))} s')
            return ret

        return inner1(func, *a, **b)

    return wrapper


# 计算运行时函数的消耗时间
def RuntimeConsume(func):
    @wraps(func)
    def wrapper(*a, **b):
        def inner1(f, *a, **b):
            if not debug:
                stole = nowstr()
            ret = f(*a, **b)
            if debug:
                return ret
            funcname1 = inspect.getframeinfo(inspect.currentframe().f_back.f_back)[2]
            funcname2 = None
            try:
                funcname2 = inspect.getframeinfo(inspect.currentframe().f_back.f_back)[3]
                funcname2 = (funcname2[0])
                funcname2 = funcname2[funcname2.find('.') + 1:funcname2.find('(')]
            except:
                pass
            if counttime(stole) > 1:
                delog(f'函数{funcname1}/{funcname2} 所消耗的时间：{int(counttime(stole))} s')
            return ret

        return inner1(func, *a, **b)

    return wrapper


# 计算函数的消耗时间
def consume(func):
    @wraps(func)
    def wrapper(*a, **b):
        def inner1(f, *a, **b):
            stole = nowstr()
            ret = f(*a, **b)
            funcname1 = inspect.getframeinfo(inspect.currentframe().f_back.f_back)[2]
            try:
                funcname2 = inspect.getframeinfo(inspect.currentframe().f_back)[2]
                # funcname2 = inspect.getframeinfo(inspect.currentframe().f_back.f_back)[3]
                # funcname2 = (funcname2[0])
                # funcname2 = funcname2[funcname2.find('.') + 1:funcname2.find('(')]
            except:
                pass
            if counttime(stole) > 1:
                log(f'函数{funcname1}/{funcname2} 所消耗的时间：{int(counttime(stole))} s')
            return ret

        return inner1(func, *a, **b)

    return wrapper


# endregion

# 时间
# region
# 对外只提供类的字符串、类的时间数组、字符串
# timestamp只对内使用

# 字符串
def research(*a):
    return re.search(*a)


def rematch(*a):
    return re.match(*a)


def nowstr(mic=True):
    ret = str(datetime.datetime.now())
    if mic:
        return ret
    return ret[:ret.find('.')]


def today():
    return str(f'{now().year}-{now().month}-{now().day}')


def yesterday():
    return str(f'{Time.year}')


def realtime():
    return f'{str(now().hour).zfill(2)}:{str(now().minute).zfill(2)}:{str(now().second).zfill(2)}'


def now():
    return datetime.datetime.now()


def Now():
    return Time()


# 根据字符串，返回到现在的时间差
def counttime(*args):
    a = []
    for i in args:
        if not type(i) == Time:
            a.append(Time(i))
        else:
            a.append(i)
    if len(a) == 1:
        return a[0].counttime()
    else:
        return a[0].counttime(a[1])

    # if s.find('hms') >= 0:
    #     return time.strftime("%H:%M:%S", time.localtime())
    # if s.find('ms') >= 0:
    #     return time.strftime("%M:%S", time.localtime())
    # if s.find('hm') >= 0:
    #     return time.strftime("%H:%M", time.localtime())
    # if s.find('h') >= 0:
    #     return time.strftime("%H", time.localtime())
    # if s.find('m') >= 0:
    #     return time.strftime("%M", time.localtime())
    # if s.find('s') >= 0:
    #     return time.strftime("%S", time.localtime())
    # if s=='all':
    #     return str(datetime.datetime.nowstr())


# 底层维护一个时间类，再由这个时间类导出字符串，进行操作
class Time():
    def __init__(self, *a, **b):
        # 默认是现在
        # 可以用字典传入
        # 如果是一个变量，就是timestamp或者字符串
        # 如果是三个数字，时分秒或者年月日，其它定为0或现在
        # 如果是六七个数字就默认是年月日，时分秒
        # 如果是字符串就转换

        def reset(self, year=now().year, month=now().month, day=now().day, hour=now().hour,
                  min=now().minute, sec=now().second, mic=now().microsecond):
            self[0].t = datetime.datetime(int(year), int(month), int(day), int(hour), int(min),
                                          int(sec), int(mic))

        # 默认设置为现在时间
        reset([self])
        year, month, day, hour, min, sec, mic = now().year, now().month, now().day, now().hour, now().minute, now().second, now().microsecond
        if b == {}:
            if len(a) in [1]:
                i = a[0]
                if type(i) in [Time]:
                    self.t = i.t
                    return
                if type(i) in [datetime.datetime]:
                    self.t = i
                    return
                if type(i) in [float]:
                    struct = time.localtime(i)
                    year, month, day, hour, min, sec, mic = struct.tm_year, struct.tm_mon, struct.tm_mday, struct.tm_hour, struct.tm_min, struct.tm_sec, int(
                        1000000 * (i - int(i)))
                if type(i) in [str]:
                    newself = Time.strtotime(i)
                    self.t = newself.t
                    return
            if len(a) in [3]:
                if a[0] < 30:
                    hour, min, sec = a
                    reset([self], hour=hour, min=min, sec=sec)
                else:
                    year, month, hour = a
                    reset([self], year=year, month=month, hour=hour)
            if len(a) in [6, 7]:
                reset([self], *a)
        # 是通过*b传参，则忽略所有的*a
        else:
            reset([self], **b)
            # year, month, day, hour, min, sec, mic = b['year'], b['month'], b['day'], b['hour'], b['min'], b['sec'], b['mic']
        # timestamp = datetime.datetime(year, month, day, hour, min, sec, mic).timestamp()
        # self.t = datetime.datetime.fromtimestamp(timestamp)

    def strtotime(s):
        """
        字符串返回时间类
        @return:
        """
        return strtotime(s)

    def istime(*a):
        try:
            return strtotime(a[-1])
        except:
            return False

    def __call__(self, *args, **kwargs):
        self.__init__()

    def today(self):
        return str(f'{self.year()}-{self.month()}-{self.day()}')

    def yesterday(self):
        t = Time()
        t.add(-24 * 3600)
        return t.today()

    def year(self):
        return str(self.t.year)

    def month(self):
        return str(self.t.month)

    def day(self):
        return str(self.t.day)

    def weekday(self):
        return str(self.t.weekday())

    def second(self):
        return str(self.t.second)

    def min(self):
        return str(self.t.minute)

    def hour(self):
        return str(self.t.hour)

    def mic(self):
        return str(self.t.microsecond)

    def date(self):
        return self.s()[:10]

    def time(self):
        return self.s()[11:19]

    def __sub__(self, other):
        if type(other) in [int, float]:
            return Time(self.t.__sub__(datetime.timedelta(seconds=other)))
        return Time(self.t.__sub__(other.t))

    # 重写<，>
    def __lt__(self, other):
        return self.t.__lt__(other.t)

    def __gt__(self, other):
        return self.t.__gt__(other.t)

    def __add__(self, other):
        if type(other) in [int, float]:
            return Time(self.t.__add__(datetime.timedelta(seconds=other)))
        return Time(self.t.__add__(other.t))

    def add(self, sec):
        if not type(sec) == int:
            warn(sec)
            sys.exit(-1)
        self.t = datetime.datetime.fromtimestamp(self.t.timestamp() + sec)
        return self.s()

    def s(self, mic=False):
        # return f'{str(self.year).zfill(2)}-{str(self.month).zfill(2)}-{str(self.day).zfill(2)} {str(self.hour).zfill(2)}:{str(self.min).zfill(2)}:{str(self.sec).zfill(2)}.{str(self.mic).zfill(6)}'
        if not mic:
            return str(self.t)
        else:
            return removetail(str(self.t), '.')

    def __str__(self):
        return self.s()

    # 返回距离现在的时间或者两个时间类的差，返回绝对值（秒）
    def counttime(self, obj=None):
        def do(*a):
            if len(a) == 1:
                s, = a
                return abs(s.t - datetime.datetime.now()).total_seconds()
            if len(a) == 2:
                s1, s2 = a
                return abs(s1.t - s2.t).total_seconds()

        if obj == None:
            return do(self)
        return do(self, obj)

    def stamp(self):
        return self.timestamp()

    def timestamp(self):
        return self.t.timestamp()


# 字符串返回Time
def strtotime(s=nowstr()):
    if not type(s) == str:
        warn(f'用法错误。s不是字符串而是{info(s)}')
        return
    s = s.replace('：', ':')
    s = s.replace('年', '-').replace('月', '-').replace('日', '')
    s = s.replace('时', ':').replace('分', ':').replace('秒', '')

    # 星期（返回的是今日所在这周的）
    if '星期' in s:
        # 0-6
        today = int(now().weekday())
        t = Time()
        if s == '星期一':
            t.add((0 - today) * 24 * 3600)
            s = s.replace('星期一', '')
        if s == '星期二':
            t.add((1 - today) * 24 * 3600)
            s = s.replace('星期二', '')
        if s == '星期三':
            t.add((2 - today) * 24 * 3600)
            s = s.replace('星期三', '')
        if s == '星期四':
            t.add((3 - today) * 24 * 3600)
            s = s.replace('星期四', '')
        if s == '星期五':
            t.add((4 - today) * 24 * 3600)
            s = s.replace('星期五', '')
        if s == '星期六':
            t.add((5 - today) * 24 * 3600)
            s = s.replace('星期六', '')
        if s == '星期日' or s == '星期天':
            t.add((6 - today) * 24 * 3600)
            s = s.replace('星期日', '')
        return t

    # 先处理毫秒
    if '.' in s:
        s, mic = splittail(s, '.')
        mic = int(mic)
    else:
        mic = 0

    # 没有年或者没有时间
    t = rematch(r"(\d{4})?-?(\d{1,2})-(\d{1,2})\s?(\d{1,2})?:?(\d{1,2})?:?(\d{1,2})?", s)
    if t:
        year, month, day, hour, min, sec = t.groups()
        if year == None:
            year = now().year
        if hour == None:
            hour = 0
        if min == None:
            min = 0
        if sec == None:
            sec = 0
        return Time(year=year, month=month, day=day, hour=hour, min=min, sec=sec, mic=mic)
    else:
        #     没有日期信息，可以没有秒（那就是时+分）
        t = rematch(r"(\d{1,2}):(\d{1,2}):?(\d{1,2})?", s)
        hour, min, sec = t.groups()
        if sec == None:
            sec = 0
        return Time(hour=hour, min=min, sec=sec, mic=mic)

    # 至少五项的字符串
    # if ':'in s and '-'in s:
    #     (year, month, day, hour, min) = (
    #         int(s[0:4]), int(s[s.find('-') + 1:s.rfind('-')]),
    #         int(s[s.rfind('-') + 1:s.find(' ')]), int(s[s.rfind(' ') + 1:s.find(':')]),
    #         int(s[s.find(':') + 1:s.rfind(':')]))
    #     try:
    #         mic = int(s[s.find('.') + 1:])
    #         sec = int(s[s.rfind(':') + 1:s.find('.')])
    #     except:
    #         sec = int(s[s.rfind(':') + 1:])
    #         mic = 0
    # else:
    #     # 只有日期字符串
    #     if '-'in s:
    #         lis=s.split('-')
    #         year,month,day=lis[0].strip(' '),lis[1].strip(' '),lis[2].strip(' ')
    #         hour,min,sec,mic=0,0,0,0
    #     else:
    # #         只有时间字符串
    #         year,month,day=today().split('-')
    #         if len(s)<7:
    # #             只有hour, min
    #             hour,min=s.split(':')
    #             sec,mic=0,0
    #         elif len(s)<10:
    # #             没有mic
    #             hour,min,sec=s.split(':')
    #             mic=0
    #         else:
    #             hour,min,res=s.split(':')
    #             sec,mic=res.split('.')


# timestamp构造Time
def timestamptotime(s):
    return datetime.datetime.fromtimestamp(eval(s) / 1000).strftime("%Y-%m-%a %H:%M:%S.%f")


# 工具
# 转换为timestamp
def timestamp(s=None):
    if type(s) == str:
        return time.mktime(time.strptime(s, "%Y-%m-%a %H:%M:%S.%f"))
    if type(s) == Time:
        return Time.timestamp()
    if s == None:
        return time.time()


# 转换为数组（未写完）
def timearr(s=nowstr()):
    # return time.strftime("%Y-%m-%a %H:%M:%S", time.localtime())

    if len(s) > 10:
        (year, month, day, hour, min) = (
            int(s[0:4]), int(s[s.find('-') + 1:s.rfind('-')]), int(s[s.rfind('-') + 1:s.find(' ')]),
            int(s[s.rfind(' ') + 1:s.find(':')]),
            int(s[s.find(':') + 1:s.rfind(':')]))
        try:
            mic = int(s[s.find('.') + 1:])
            sec = int(s[s.rfind(':') + 1:s.find('.')])
        except:
            sec = int(s[s.rfind(':') + 1:])
            mic = 0
        return (year, month, day, hour, min, sec, mic)


# endregion

# 调试模式
# region
def Exit(*a):
    """
    直接结束或者无限挂起，不再让程序运行
    @param a:
    @return:
    """
    try:
        warn(*a)
        exit()
    except Exception as e:
        warn('程序不能正常停止。请手动终止。')
        log(f'错误类型为 {type(e)}')
        warn(e)
        context(2)
        sleep(9999)


def Debug():
    """
    转到调试模式
    @return:
    """
    global debug
    debug = True


def Run():
    global debug
    debug = False


def retry(e):
    """
    确定是否应该进行重试
    @param e:
    @return:
    """
    log(f'{type(e)} 错误')
    if type(e) in retrylist:
        log('重建中 ...')
        return True
    log('不重建。')
    return False


# endregion

# 特殊功能函数
# region

def info(s):
    # 如果是类，列举属性和方法
    if not type(s) in [int, str, list, dict, float, tuple, ]:
        att = []
        for i in dir(s):
            if not i in dir(object):
                att.append(i)
        log(f'属性和方法：{att}')
        return att

    if type(s) in [str]:
        # 磁盘
        if len(s) == 1:
            gb = 1024 ** 3  # GB == gigabyte
            try:
                total_b, used_b, free_b = shutil.disk_usage(s.strip('\n') + ':')  # 查看磁盘的使用情况
            except Exception as e:
                Exit(e)
            # log(f'{s.upper()}' + '盘总空间: {:6.2f} GB '.format(total_b / gb))
            # log('\t已使用 : {:6.2f} GB '.format(used_b / gb))
            # log('\t\t空余 : {:6.2f} GB '.format(free_b / gb))
            return (free_b / gb)

        #     文件（夹）
        if isfile(s) or isdir(s):
            s = standarlizedPath(s)
            sss = ''
            if isdir(s):
                sss = '夹'
            log(f'路径：{s}（文件{sss}）')
            log(f'创建日期：{createtime(s)}')
            log(f'修改日期：{modifytime(s)}')
            log(f'访问日期：{accesstime(s)}')
            log(f'大小：{size(s)}MB')

            # 是视频
            if tail(s, '.') in ['wmv', 'mp4']:
                t = videolength(s)
                log(f'{filename(s)} 时长{int(t / 60)}:{t - int(t / 60)}')
            return size(s)
    # 其它类型
    elif type(s) in [list, tuple, dict]:
        if len(s) > 3:
            tip(f'{s[0:2]}...{s[-1]}')
        else:
            tip(s)
        tip(f'类型：{type(s)} 大小：{int(int(sys.getsizeof(s) / 1024 / 1024 * 100) / 100.0)}MB 内存地址：{id(s)} 长度{len(list(s))}')
    elif type(s) in [int, str, float, ]:
        tip(f'类型：{type(s)} 大小：{int(sys.getsizeof(s))}Byte 内存地址：{id(s)}')


# 获取锁
def getlock(name, content=None):
    f = txt(projectpath(f'{name}lock.txt'))
    if f.l == []:
        f.l.append(f'1')
        f.save()
        return True
    else:
        sleep(10)
        warn(f'awaitingLOCK {name}')
        return getlock(name)


# 释放锁
def releaselock(name):
    f = txt(projectpath(f'{name}lock.txt'))
    f.l = []
    f.save()


# 获取屏幕锁
def getscreenlock():
    return getlock('screen')


def releasescreenlock():
    return releaselock('screen')


# 获取剪贴板锁
def getcopylock():
    return getlock('copy')


# 释放剪贴板锁
def releasecopylock():
    return releaselock('copy')


# 翻译
def translate(s, limit=3):
    if len(s) < limit:
        return ''
    hotkey('alt', 'tab')
    getscreenlock()
    getcopylock()
    click(846, 520)
    hotkey('ctrl', 'a')
    copyto(s)
    hotkey('ctrl', 'v')
    hotkey('enter')
    sleep(len(s) / 1000)
    click(1000, 358)
    sleep(0.5)
    hotkey('ctrl', 'a')
    hotkey('ctrl', 'c')
    hotkey('alt', 'tab')
    releasescreenlock()
    releasecopylock()
    return pastefrom()


# 计数工具语法糖
def count(k=''):
    f = rjson(projectpath('cache/count.txt'), silent=True)
    f.l = []
    f.save()
    if k in keys(f.d):
        v = f.d[k][0]
        f.delete({k: v}, silent=True)
        v += 1
        f.add({k: v})
        delog(v)
    else:
        f.add({k: 1}, silent=True)
        delog(1)
    f.save(silent=True)


# 命令行
# https://blog.csdn.net/weixin_42133116/article/details/114371614
class CMD():
    CSI = '\033['

    # CSI = '\x1b['
    def front(n, s=''):
        return (f'{CMD.CSI}38;5;{n}m{s}')

    def resetfront(s=''):
        return CMD.front(39, s)

    def background(n, s=''):
        return (f'{CMD.CSI}48;5;{n}m{s}')

    def resetbackground(s=''):
        return CMD.background(49, s)

    def font(n, s=''):
        return (f'{CMD.CSI}{n}m{s}')

    def resetall(s=''):
        return CMD.font(0, s)

    def reset(*a, **b):
        return CMD.resetall(*a, **b)

    def showall(self=None):
        for i in range(0, 256):
            print(i, CMD.front(i, f'-------{i}号颜色--------'), CMD.reset(),
                  CMD.background(i, '\t' * 100), CMD.reset())
        for i in range(0, 110):
            print(CMD.font(i), f'这是{i}号示例字体', CMD.reset())

    def listall(*a, **b):
        return CMD.showall(*a, **b)

    def __init__(self, cmds='', coding='utf-8', silent=False):
        cmd = [self._where('PowerShell.exe'),
               "-NoLogo", "-NonInteractive",  # Do not print headers
               "-Command", "-"]  # Listen commands from stdin
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        self.popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                      stderr=subprocess.STDOUT, startupinfo=startupinfo)
        self.coding = coding
        self.run(cmds, silent=silent)

    def __enter__(self):
        return self

    def __exit__(self, a, b, c):
        self.popen.kill()

    def run(self, cmd, silent=False, timeout=15):
        b_cmd = cmd.encode(encoding=self.coding)
        try:
            b_outs, errs = self.popen.communicate(b_cmd, timeout=timeout)
        except subprocess.TimeoutExpired:
            self.popen.kill()
            b_outs, errs = self.popen.communicate()
        outs = b_outs.decode(encoding=self.coding)
        if errs == None:
            out(outs, silent=silent)
            return True
        else:
            return False
            Exit(errs)

    @staticmethod
    def _where(filename, dirs=None, env="PATH"):
        if dirs is None:
            dirs = []
        if not isinstance(dirs, list):
            dirs = [dirs]
        if glob(filename):
            return filename
        paths = [os.curdir] + os.environ[env].split(os.path.pathsep) + dirs
        try:
            return next(os.path.normpath(match)
                        for path in paths
                        for match in glob(os.path.join(path, filename))
                        if match)
        except (StopIteration, RuntimeError):
            raise IOError("File not found: %s" % filename)


#         endregion

# 键鼠互动
# region
def get_screen(path):
    """
    保存当前屏幕截图
    @param path:
    @return:
    """
    path=standarlizedPath(path)
    createpath(path)
    if isdir(path):
        path+=f'{Now().s()}.png'
        path=standarlizedFileName(path)
    ImageGrab.grab().save(path)

# 打开一系列的edge
def openedge(l):
    hotkey('win')
    typein('edge')
    hotkey('shift')
    hotkey('enter')
    sleep(2)
    if type(l) == str:
        l = [l]
    for url in l:
        hotkey('alt', 'd')
        copyto(url)
        hotkey('ctrl', 'v')
        hotkey('enter')
        if not url == l[-1]:
            hotkey('ctrl', 't')


# 键盘输入
def typein(s, strict=False):
    if strict:
        for i in str(s):
            hotkey(i)
    else:
        copyto(s)
        hotkey('ctrl', 'v')
        sleep(0.5)


# pyperclip
def copyto(s):
    pyperclip.copy(s)
    sleep(0.1)


def pastefrom():
    return pyperclip.paste()


# 键盘
def hotkey(*a):
    pyautogui.hotkey(*a)
    sleep(0.2)


def size(a, sum=0, bit=True):
    """

    @param a:
    @param sum:
    @param bit:
    @return:
    """
    if type(a) in [str]:
        s = a
        # 磁盘
        if len(s) == 1:
            gb = 1024 ** 3  # GB == gigabyte
            try:
                total_b, used_b, free_b = shutil.disk_usage(s.strip('\n') + ':')  # 查看磁盘的使用情况
            except Exception as e:
                Exit(e)
            return (free_b / gb)
        #     文件
        if isfile(s):
            if bit:
                return os.stat(s).st_size
            return os.stat(s).st_size / 1024 / 1024

        #     文件夹
        if isdir(s):
            sum = 0
            for i in listfile(s):
                sum += size(i, bit=bit)
            for i in listdir(s):
                sum += size(i, bit=bit)
            return sum

    #     其它类型

    elif type(a) in [list, tuple]:
        for i in a:
            sum = size(i, sum, bit=bit)
        return sum
    elif type(a) in [dict]:
        sum = size(keys(a), sum, bit=bit)
        for k in keys(a):
            sum = size(a[k], sum, bit == bit)
        return sum
    return sum + sys.getsizeof(a)


# 在屏幕指定位置进行剪贴板复制粘贴并按下回车
def Input(x, y, s):
    pyperclip.copy(s)
    pyautogui.click(x, y)
    sleep(1)
    pyautogui.hotkey('ctrl' + 'v')
    sleep(0.5)
    pyautogui.hotkey('Enter')
    sleep(1)


# endregion

# 音视频、图片
# region


#     拼接图片
def combineimages(inputpath=None, outputpath=None, outputname=None, mode='vertical', reverse=None,
                  filelist=None,
                  cuttop=0, cutbottom=0, cutleft=0, cutright=20):
    """

    @param inputpath:
    @param outputpath:
    @param outputname:
    @param mode:
    @param reverse:
    @param filelist:
    @param cutbottom:
    @param cuttop:
    @param cutleft:
    @param cutright: 总有些傻哔情况有点右侧进度条
    @param cuttop:顶部裁剪
    @return:
    """

    def do(img1, img2, mode='vertical', outputpath=None,
           ratio1=0.3, ratio2=0.3, scale1=70, scale2=70):
        """
        裁剪后自动识别拼接图片
        @param img1:上图片路径(确定？)，是不断扩张的图片。
        @param img2:
        @param mode:
        @param outputpath:
        @param ratio1:
        @param ratio2: 默认地根据图片的长宽比例来设置重合验证长度
        @param scale1: 我也不知道现在有什么用

        @param scale2:与image1的重合验证部分
        @return:
        """
        # 新版 chrome 有进度条，image2 掉顶格2像素变为白色
        image1 = cv2.imread(img1)
        image2 = cv2.imread(img2)[2:,:]

        # 原图去掉拼接方向上衔接须裁剪处
        if mode == 'vertical':
            # 允许中断后继续操作，因此有时候不处理image1
            image1 = image1[:image1.shape[0] - cutbottom, :]
            image2 = image2[cuttop:image2.shape[0]:]

        matchimage1 = image1
        # image1 的忽略历史累积部分
        level1=0
        if mode == 'vertical':
            if image1.shape[0]>3000:
                level1+=image1.shape[0]-2000
                matchimage1=image1[-2000:,:]
        matchimage2 = image2
        scale1, scale2 = min(scale1, int(matchimage1.shape[0] * ratio1)), min(scale2, int(
            matchimage2.shape[0] * ratio2))
        if mode == 'vertical':
            matchimage2 = matchimage2[:scale2, :]

        # 匹配图去掉垂直于拼接方向的部分
        if mode == 'vertical':
            matchimage1 = matchimage1[:, cutleft:image1.shape[1] - cutright]
            matchimage2 = matchimage2[:, cutleft:image2.shape[1] - cutright]


        # 需要从下到上匹配，所以要翻转
        # 1 是template，是被滑动的图像。
        result_filpped = cv2.matchTemplate(cv2.flip(matchimage2, 0), cv2.flip(matchimage1, 0),
                                           cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(cv2.flip(result_filpped, 0))
        if mode == 'vertical':
            max_loc=(max_loc[0],level1+max_loc[1])
        delog('相似匹配位置', max_loc)
        # look(matchimage1)
        # look(matchimage2)

        if mode == 'vertical':
            if max_val < 0.75:
                warn('图片匹配失败，直接拼接')
                max_loc = (0, image1.shape[0])
            cv2.imwrite(img1, image1[:max_loc[1]])
            image3 = cv2.vconcat([image1[:int(max_loc[1]), :], image2])
            cv2.imwrite(img1, image3)

    if outputpath == None:
        if outputname == None:
            outputpath = parentpath(inputpath) + 'combined.jpg'
        else:
            outputpath = parentpath(inputpath) + outputname
    if filelist == None:
        filelist = []
        l1 = SortedName(listfile(inputpath, full=False))
        for i in l1:
            filelist.append(inputpath + '/' + i)
    if reverse:
        filelist.reverse()
    first = filelist.pop(0)
    for i in filelist:
        do(first, i, )
    if outputpath == None:
        if outputname == None:
            outputname = 'basic.png'
        outputpath = parentpath(inputpath) + outputname
    sleep(2)
    move(first, outputpath)


class pic():
    def __init__(self, path):
        path = standarlizedPath(path)
        self.path = path
        try:
            self.img = PIL.Image.open(path)
            self.width, self.height = self.img.size
            self.type = self.img.format
            self.complete_img_suffix()
        except:
            pass

    #         自动补全后缀名
    def complete_img_suffix(self):
        if not '.' in self.path:
            self.img.close()
            newname = self.path + '.' + (self.type.lower())
            rename(self.path, newname)
            self.__init__(newname)

    def __del__(self):
        try:
            self.img.close()
        except:
            pass


class img(pic):
    pass


class video():
    def __init__(self, path):
        self.path = path
        self.cap = cv2.VideoCapture(path)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.framecount = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.duration = self.framecount / self.fps
        self.type = self.path.split('.')[-1]


# 识别图片格式（后缀名）
def imgtype(path):
    img = PIL.Image.open(path)
    return img.format


# 从视频中提取声音
def mp4tomp3(src, tar=None):
    if tar == None:
        tar = f'{removetail(src, "mp4")}mp3'
    src, tar = standarlizedPath(src, strict=True), standarlizedPath(tar, strict=True)
    if isdir(src) and isdir(tar):
        for f in listfiletree(src):
            if '.mp4' in f:
                moviepy.editor.VideoFileClip(f).audio.write_audiofile(f'{tar}\\{filename(f)}.mp3')
        return
    if not isfile(src) and not '.mp4' in src:
        Exit(f'{src}不是mp4文件1')
    moviepy.editor.VideoFileClip(src).audio.write_audiofile(tar)


def videotoaudio(*a, **b):
    return mp4tomp3(*a, **b)


# 使用ffmpeg剪切视频
def cutvideo(inputpath, start, end, outputpath=None):
    if outputpath == None:
        outputpath = removetail(inputpath, '.mp4') + '-cut.mp4'
    sourcepath = os.path.abspath(inputpath)
    outputpath = os.path.abspath(outputpath)
    command = f'ffmpeg  -i {standarlizedPath(sourcepath)} -vcodec copy -acodec copy -ss {start} -to {end} {outputpath} -y'
    print(command)
    os.system('"%s"' % command)


# 使用ffmpeg提取音频
# def extractaudio(inputpath, outputpath):
#     sourcepath = os.path.abspath(standarlizedPath(inputpath))
#     command = f'ffmpeg -i {inputpath} -vn -codec copy {outputpath}'
#     print(command)
#     os.system('"%s"' % command)


# 返回音频的秒数
def videolength(s):
    if not isfile(s):
        Exit(s)
    return VideoFileClip(s).duration


# endregion


# endregion

# 进程池与线程池
# region
def sleep(t=9999):
    if t > 10:
        delog(f'睡眠 {t} 秒')
    time.sleep(t)


class pool():
    def __init__(self, maxworker=10):
        self.e = concurrent.futures.ThreadPoolExecutor(max_workers=maxworker)

    def doorwait(self, fn, *a):
        # self.e.map(fn,[[*a],])
        self.f = fn
        # print(a)
        self._do(a)
        print(a)

    def _do(self, a):
        self.e.submit(self.f, *a)

    def execute(self, fun, *a):
        self.doorwait(fun, *a)

    def rest(self):
        return len(self.e.as_conpleted())

    def rest(self):
        ()


# endregion

# 文件系统读写
# region
def similar(s1, s2):
    """
    计算两个字符串的相似度
    @param s1:
    @param s2:
    @return:
    """
    if not type(s1)in [str] or not type(s2) in [str]:
        warn('similar 输入的不是字符串')
        return False

    m, n = len(s1), len(s2)
    dp = [[0] * (n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        dp[i][0] = i
    for j in range(1, n+1):
        dp[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[m][n]


def delete_similar(path,new=False):
    """
    删除目录下名称相似的同大小文件和文件夹。保留创建时间更早的。一次只会二选一。
    @param path:
    @param new:是否保留创建时间更晚的
    @return:
    """
    files=listfile(path)
    dirs=listdir(path)
    delete=[]
    retain=[]
    def func(l):
        for i in l:
            for j in l[l.index(i)+1:]:
                if i in delete or j in delete:
                    continue
                if size(i)==size(j) and similar(i,j)/max(len(filename(i)),len(filename(j)))<0.1:
                    if createtime(i)<createtime(j) and new or createtime(i)>createtime(j) and not new:
                        ii=i
                        jj=j
                    else:
                        ii=j
                        jj=i
                    delete.append(ii)
                    retain.append(jj)
                    break
    func(files)
    func(dirs)
    out([f'以下是要删除的文件 {len(delete)}\n']+delete+[f'\n以下是被保留的文件 {len(retain)}\n']+retain)
    deletedirandfile(delete)


def create_shortcut(source, target=None):
    """

    @param source: 源文件/文件夹
    @param target: 快捷方式位置。默认为在桌面的同名。
    @return:
    """
    if not source[1]==':':
        source=projectpath(source)
    source=standarlizedPath(source)
    if target==None:
        target=f'C:/Users/username/Desktop/{extentionandname(source)[0]}.lnk'
    if isdir(source):
        folder_shortcut = winshell.shortcut(target)
        folder_shortcut.path = source
        folder_shortcut.write()
    if isfile(source):
        file_shortcut = winshell.shortcut(target)
        file_shortcut.path = source
        # shell = Dispatch('WScript.Shell')
        # file_shortcut.working_directory = shell.SpecialFolders('Desktop')
        file_shortcut.write()


def cleardir(path):
    path = standarlizedPath(path)
    deletedirandfile(path)
    createpath(path + '/')


# 判断路径存在
def exists(path):
    return os.path.exists(path)


# 解压zip文件
def unzip(zippath, targetpath=None):
    zfile = zipfile.ZipFile(zippath)
    if targetpath == None:
        targetpath = zippath.replace('.zip', '')
    if isdir(targetpath):
        pass
    else:
        createpath(targetpath)
    for f in zfile.namelist():
        zfile.extract(f, targetpath)
    zfile.close()


def regeneratename(originalname, targetpath, regenerate=None, issame=None, originalpath=None):
    """
    要新建的文件/文件夹已存在时，新命名，并判断是否覆盖。线程不安全。
    @param originalname:原来的名字。不确定目标路径是否存在同样的
    @param targetpath:目标路径
    @param regenerate: 方法。传入旧名字，返回新名字。默认下划线+数字
    @param issame: 方法。判断内容是否相同
    @param originalpath: 如果不为空，说明原来的文件是存在的。就可以使用比较大小作为默认比较内容方法。
    @return: 存在同样的文件/文件夹 ；新的文件/文件夹名
    """
    newname = originalname
    if regenerate == None:
        # 下划线+数字 自动生成新名字
        def regenerate(oldname):
            oldname, ext = extentionandname(oldname, exist=False)
            if not research(r'_\d$', oldname):
                return oldname + '_1' + ext
            originalname, count = splittail(oldname, '_')
            return f'{originalname}_{int(count) + 1}{ext}'

    # 检查目标位置名称是否被占用
    def havename(newname, targetpath):
        return isfile(f'{targetpath}/{newname}') or isdir(f'{targetpath}/{newname}')

    # 检查是否存在同样的文件/文件夹
    def tellsame(newname, targetpath):
        if havename(newname, targetpath):
            if issame == None:
                # 源文件不存在，无法比较大小。默认相同
                if originalpath == None or not exists(originalpath + '/' + originalname):
                    return True
                #     默认比较大小
                return size(originalpath + '/' + originalname) == size(targetpath + '/' + newname)
            return issame(newname, targetpath)
        return False

    b = tellsame(newname, targetpath)
    while havename(newname, targetpath):
        newname = regenerate(newname)
        b = tellsame(newname, targetpath) or b
    return b, newname


# 获取文件的扩展名（后缀名）
def extention(fname, silent=False):
    if not isfile(fname):
        if not silent:
            warn(f'文件 {fname} 不存在')
        return
    if not '.' in fname:
        if not silent:
            warn(f'文件 {fname} 没有扩展名')
        return
    fname = filename(fname)
    return fname[fname.rfind('.') + 1:]


# 分割带路径的文件名和其.+扩展名
def extentionandname(fname, silent=True, exist=True):
    if not isfile(fname):
        if not silent:
            warn(f'文件 {fname} 不存在')
        if exist:
            return
    if not '.' in fname:
        if not silent:
            warn(f'文件 {fname} 没有扩展名')
        return fname, ''
    fname = filename(fname)
    return fname[0:fname.rfind('.')], fname[fname.rfind('.'):]


def filenameandext(*a, **b):
    ret = extentionandname(*a, **b)
    return ret[0], ret[1]


def splitext(*a, **b):
    return filenameandext(*a, **b)


# 移除空文件夹
def rmempty(root, tree=False, silent=False):
    dlis = []
    if tree == False:
        for i in listdir(root):
            if [] == listdir(i) + listfile(i):
                dlis.append(i)
    if not dlis == []:
        if not silent:
            out(dlis)
            warn('确认删除这些空文件夹，输入任意开始删除，否则请立即停止程序。')
            c = input()
        deletedirandfile(dlis)


def look(path):
    """
    打开文件或者网页
    @param path:
    @return:
    """
    if type(path) in [numpy.ndarray]:
        p = cachepath('cv2/look.png')
        createpath(p)
        deletedirandfile([p])
        cv2.imwrite(p, path)
        # cv2.imwrite(p,numpy.load(path))
        look(p)
        return
    if 'https' in path:
        openedge(path)
    path = standarlizedPath(path)
    if isdir(path):
        os.startfile(path)
        return
    if not isfile(path,notnull=False) and not 'https' in path:
        warn(f'不存在文件或文件夹{path}')
        return
    os.startfile(path)


def Open(path):
    return look(path)


def get_base_path(base_path, s):
    if base_path in s or ':' in s:
        return s
    if './' in s:
        s = s[2:]
    if not s == '':
        s = '/' + s
    return standarlizedPath(f'{base_path}{s}')

# 隐藏目录
def selfpath(s=''):
    return get_base_path(projectpath('self/'), s)

# 收藏目录
def collectionpath(s=''):
    return get_base_path(projectpath('self/MANUAL 文档 收藏 AUTO/网页集锦/'), s)


# 用户目录
def userpath(s=''):
    if 'C:/' in s:
        return
    return get_base_path(f'C:/Users/{user}', s)


# 项目根目录
def projectpath(s=''):
    return get_base_path('D:/Kaleidoscope', s)


# js 脚本目录
def jspath(s=''):
    return get_base_path(projectpath('js'), s)


# 临时文件目录
def cachepath(s=''):
    return get_base_path(projectpath('cache'), s)


# 用户配置文件目录
def settingspath(s=''):
    return get_base_path(projectpath('settings'), s)


def jsonpath(s=''):
    return get_base_path(projectpath('json'), s)


# 下属的文件夹和文件
def listall(path):
    return listfile(path) + listdir(path)


# 判断是否是空的文件夹
def isemptydir(path):
    path = standarlizedPath(path)
    if not isdir(path):
        warn(f'{path}不是文件夹，请检查路径。')
        return False
    if [] == listfile(path) + listdir(path):
        return True
    else:
        return False


# 访问时间
def accesstime(path):
    path = standarlizedPath(path)
    t = os.path.getatime(path)
    return Time(t)


# 创建时间
def createtime(path):
    path = standarlizedPath(path)
    t = os.path.getctime(path)
    return Time(t)


# 修改时间
def modifytime(path):
    path = standarlizedPath(path)
    t = os.path.getmtime(path)
    return Time(t)


# 在项目目录下新建文件以进行覆盖输出
def out(s, silent=False, target='out.txt'):
    f = txt(projectpath(target))
    f.l = []
    f.save()

    def do(s):
        f.add(s, silent=True)

    do(s)
    if silent == False:
        Open(f.path)


# 在固定文件进行持续输出
def pout(*a, **b):
    return provisionalout(*a, **b)


def provisionalout(s, silent=True, path='pout.txt'):
    f = txt(projectpath(path))

    def do(s):
        f.add(s)

    do(s)
    log(f.path)
    if silent == False:
        Open(f.path)


# 在固定文件进行输入
def provisionalin():
    f = txt(desktoppath('pout.txt'))
    return f.l


# 重命名文件或文件夹
def rename(s1, s2, overwrite=True):
    s1 = standarlizedPath(s1)
    s2 = standarlizedPath(s2)
    if overwrite and (isdir(s2) or isfile(s2)):
        if size(s1) >= size(s2):
            deletedirandfile(s2)
        else:
            deletedirandfile(s1)
            return
    os.rename(standarlizedPath(s1), standarlizedPath(s2))


# 判断是否是存在文件
def isfile(s, notnull=True):
    """
    判断是否是存在文件
    @param s:
    @param notnull: 文件不为空
    @return:
    """
    if not type(s) in [str]:
        warn(f'isfile的参数必须是字符串，而不是{type(s)}')
        return False
    if os.path.isfile(s):
        if notnull:
            return not 0 == os.path.getsize(s)
        return True


# 判断是否是存在文件夹
def isdir(s):
    if not type(s) in [str]:
        return False
    return os.path.isdir(s)


# 复制文件夹
def copydir(s1, s2):
    s1, s2 = standarlizedPath(s1), standarlizedPath(s2)
    if isdir(s1):
        shutil.copytree(s1, s2)


# 复制文件
def copyfile(s1, s2):
    s1, s2 = standarlizedPath(s1), standarlizedPath(s2)
    createpath(s2)
    if isfile(s1):
        shutil.copy(s1, s2)


def move(s1, s2, overwrite=False, silent=True, autorename=True, merge=True):
    """
    移动文件或文件夹
    @param s1:
    @param s2:
    @param overwrite: 是否覆盖同名文件。如果autorename，同名内容不同文件会重命名而不是覆盖。
    @param autorename: 是否重命名同名文件。如果overwrite，同名同内容文件会直接覆盖而不是重命名。
    @param merge: 是否合并同名文件夹。如果autorename，同名文件夹会重命名而不是合并。
    @param silent:
    @return:
    """
    if isfile(s1):
        if isdir(s2):
            return move(s1, f'{s2}/{filename(s1)}', overwrite, silent, autorename, merge)
        if isfile(s2):
            b, newname = regeneratename(filename(s1), parentpath(s2), originalpath=parentpath(s1))
            if b and overwrite:
                deletedirandfile(s1)
                delog(f'移动时已有相同文件 {s2}。覆盖。')
                return
            if autorename:
                if b:
                    delog(f'移动时已有相同文件 {s2}。重命名 {newname}。')
                else:
                    delog(f'移动时已有不同内容文件 {s2}。重命名 {newname}。')
            if not autorename and not overwrite:
                Open(parentpath(s1))
                Open(parentpath(s2))
                Exit(f'移动时已有文件。请检查 {s1} {s2}')
            s2 = f'{parentpath(s2)}/{newname}'
        createpath(s2)
        shutil.move(standarlizedPath(s1), standarlizedPath(s2))
        return

    if isdir(s1):
        if isdir(s2):
            if merge:
                for all in listall(s2):
                    move(all, f'{s1}/{filename(all)}', overwrite=overwrite, silent=silent,
                         autorename=autorename, merge=merge)
            else:
                # 思路是直接把文件夹当作文件来判断。因此直接copy上面的逻辑
                b, newname = regeneratename(filename(s1), parentpath(s2),
                                            originalpath=parentpath(s1))
                if b and overwrite:
                    deletedirandfile(s1)
                    delog(f'移动时已有相同文件夹 {s2}。覆盖。')
                    return
                if autorename:
                    if b:
                        delog(f'移动时已有相同文件夹 {s2}。重命名 {newname}。')
                    else:
                        delog(f'移动时已有不同内容文件夹 {s2}。重命名 {newname}。')
                if not autorename and not overwrite:
                    Open(parentpath(s1))
                    Open(parentpath(s2))
                    Exit(f'移动时已有文件夹。请检查 {s1} {s2}')
        if isfile(s2):
            Exit(f'移动文件夹为文件错误。 {s1} {s2}')

    shutil.move(standarlizedPath(s1), standarlizedPath(s2))
    if not silent:
        log(f'移动完成：从 {s1} 到 {s2}')


@listed
def listdir(path, full=True):
    path = standarlizedPath(path)
    for (root, dirs, files) in os.walk(path):
        ret = dirs
        for i in ['$RECYCLE.BIN', 'System Volume Information']:
            try:
                ret.remove(i)
            except:
                pass
        # delog(str(ret))
        if full == False:
            return ret
        ret1 = []
        for i in ret:
            ret1.append(standarlizedPath(root + '/' + i))
        return ret1
    return []


@listed
def listfile(path, full=True):
    path = standarlizedPath(path)
    for (root, dirs, files) in os.walk(path):
        ret = files
        for i in ['DumpStack.log', 'DumpStack.log.tmp', 'pagefile.sys']:
            try:
                ret.remove(i)
            except:
                pass
        if not full:
            return ret
        ret1 = []
        for i in ret:
            ret1.append(standarlizedPath(root + '/' + i))
        # delog(str(ret))
        return ret1
    return []


def listfiletree(path):
    """
    listall
    @param path:
    @return:
    """
    lis = []
    lis += listfile(path)
    for i in listdir(path):
        lis += listfiletree(i)
    return lis


# 直接返回路径的文件夹路径
def pathname(s=None):
    s = standarlizedPath(s)
    return s[:s.rfind('/') + 1]


def parentpath(s):
    while s[-1] in ['\\', '/']:
        s = s[:-1]
    return pathname(s)


# 返回文路径的文件名
def filename(s):
    s = standarlizedPath(s)
    s = s[s.rfind('/') + 1:]
    if s == '':
        warn('空')
        sys.exit(-1)
    return standarlizedFileName(s)


class table():
    def __init__(self, path, title=True):
        """
        一定有表头
        @param path:
        @param title:表头数组
        """
        if not '.csv' in path:
            path += '.csv'
        self.path = standarlizedPath(path)

        if not isfile(self.path):
            if title == False:
                Exit(f'{self.path} 不存在。')
            self.create(*title)

        if not isfile(self.path):
            Exit()
        self.read(title=title)

    # 合并表格，忽略表头，默认表头一致
    def merge(self, t):
        for i in t.l:
            self.l.append(i)
        self.save()

    def create(self, *a):
        copyfile(projectpath('database/sample.csv'), self.path)
        f = open(self.path, 'w')
        writer = csv.writer(f)
        writer.writerow(a)
        f.close()
        # Exit(f'已创建 {self.path} 完毕。强制停止程序以创建成功。似乎存在缓冲区？')

    @consume
    #         去重，去空，集合化
    def set(self):
        p = list(set(self.l))
        p.sort(key=self.l.index)
        self.l = p
        if '' in self.l:
            self.l.pop(self.l.index(''))
        self.save(self)

    def read(self, title=True):
        f = open(self.path, encoding='utf-8-sig', mode='r')
        f1 = open(self.path, encoding='utf-8-sig', mode='r')

        if title:
            self.reader = csv.DictReader(f)
            self.l = []
            self.d = {}
            self.title = []
            for i in next(csv.reader(f1)):
                self.title.append(i)
            for title in self.title:
                self.d.update({title: []})
            for i in self.reader:
                self.l.append(i)
            for d in self.l:
                for k in d:
                    self.d.update({k: self.d[k] + [d[k]]})

    def save(self):
        f = open(self.path, encoding='utf-8-sig', mode='w', newline="")
        writer = self.writer = csv.DictWriter(f, self.title)
        writer.writeheader()
        writer.writerows(self.l)
        log(f'saved {self.path}')

    def add(self, d, withtitle=False, silent=True):
        if type(d) in [dict]:
            self.l.append(d)
            for key in d:
                if key in keys(self.d):
                    self.d[key] += [d[key]]
        if type(d) in [tuple, list]:
            count = 0
            newd = {}
            for i in self.title:
                if count + 1 > len(d):
                    break
                newd.update({i: d[count]})
                count += 1
            self.add(newd)
            return
        f = open(self.path, encoding='utf-8-sig', mode='a', newline="")
        writer = self.writer = csv.DictWriter(f, self.title)
        writer.writerows([self.l[-1]])
        if not silent:
            delog(f'added {self.path} {self.l[-1]}')


def add_extension(path, extension, strict=True):
    """
    给路径文件名加上扩展名
    :param path: 原始路径名
    :param extension: 不带"."的扩展名，可以是字符串或列表
    :param strict: 如果疑似已经有扩展名则强制退出
    :return:
    """
    path = standarlizedPath(path)
    if path.endswith('/'):
        Exit(f'加扩展名时路径不应以/结尾！ {path}')
    if isinstance(extension, str):
        if '.' in path and not path.endswith('.' + extension):
            warn(f'疑似已经有扩展名！ {path}')
            if strict:
                Exit('疑似已经有扩展名！')
        if not f'.{extension}' in path:
            path += f'.{extension}'
            return
    elif isinstance(extension, list):
        if not any(path.endswith(ext) for ext in extension):
            path += '.' + extension[0]
    return path


class excel():
    """
    add，每次访问全部数据内容要内存开销
    save，read要磁盘开销

    """

    def __init__(self, path, title=False):
        """
        当已有文件
        @param path:
        @param title:表头。一般是字符串数组。
        """
        self.path = add_extension(standarlizedPath(path), ['csv', 'xls', 'xlsx'])

        # 处理title
        if type(title) in [str]:
            title = [title]
        if title in [False, None]:
            self.title=False
        if self.title==[]:
            self.title=['']


        self.workbook = openpyxl.Workbook(self.path)
        self.sheet = self.workbook.active
        if not isfile(self.path):
            if self.title:
                self.sheet.append(self.title)
            self.save()

    def save(self):
        self.workbook.save(self.path)


class Csv(table):
    pass


def deletedirandfile(l, silent=None):
    """
    删除文件和文件夹
    @param l: 可以是txt路径
    @param silent:
    @return:
    """
    # 删除txt里的文件
    if isfile(l) and l[-4:] in '.txt':
        f = txt(l)
        dlis = []
        for i in f.l:
            if i in ['\n', '']:
                continue
            dlis.append(i)
        deletedirandfile(dlis)
        return

    # 递归删除dir_path目标文件夹下所有文件，以及各级子文件夹下文件，保留各级空文件夹
    # (支持文件，文件夹不存在不报错)
    def del_files(dir_path):
        if os.path.isfile(dir_path):
            try:
                os.remove(dir_path)  # 这个可以删除单个文件，不能删除文件夹
            except BaseException as e:
                if silent == None:
                    print(e)
        elif os.path.isdir(dir_path):
            file_lis = os.listdir(dir_path)
            for file_name in file_lis:
                # if file_name != 'wibot.log':
                tf = os.path.join(dir_path, file_name)
                del_files(tf)
        if silent == None:
            log(dir_path + '  removed.')

    if not type(l) == list:
        l = [l]
    # e = MThreadPool(1000)
    for file in l:
        # e.excute(del_files,file)
        del_files(file)
    for i in l:
        if os.path.exists(i):
            shutil.rmtree(standarlizedPath(i, strict=True))


def standarlizedPath(s='', strict=False):
    """
    统一路径格式
    @param s:
    @param strict:
    @return:
    """
    b = False
    if s == '':
        s = __file__
    if s[-1] in ['/', '\\']:
        b = True
    try:
        s = os.path.abspath(s)
    except Exception as e:
        print(s)
        warn(e)
        sys.exit(-1)
    if b:
        s += '/'
    #     删去路径里的每一个末尾空格
    s = s.replace('\\', '/')
    while (' /') in s:
        s = s.replace(' /', '/')
    # while (' .')in s[-6:]:
    #     s=s.replace(' .','.')
    # 规范化每一层文件夹名
    ss = s
    s = ss[:2]
    for i in ss.split('/')[1:]:
        s += '/' + standarlizedFileName(i)

    if strict:
        return s.replace('/', '\\')
    return s.replace('\\', '/')


# 合法化文件名
def standarlizedFileName(str):
    '_1_171915336a3bc770~tplv-t2oaga2asx-zoom-in-crop-mark 4536 0 0 0.image.webp'
    str = re.sub('/|\||\?|>|<|:|\n|/|"|\*', ' ', str)
    s = '_'
    str = str.replace('\\', s)
    str = str.replace('\r', s)
    str = str.replace('\t', s)
    str = str.replace('\x08', s)
    str = str.replace('\x1c', s)
    str = str.replace('\x14', s)

    return str[:224]


def CreatePath(path):
    """
    只创建空文件夹
    :param path: ’\‘自动转换为‘/’
    :return:成功或者已存在返回路径字符串，否则返回False
    """
    path = pathname(path)
    # if not path.rfind('.') > 1:
    #     path = path + '/'
    if os.path.exists(path):
        return path
    try:
        # windows创建文件夹自动删去末尾空格，此时再在原来的带空格路径下操作就会报错
        os.makedirs(path)
        return path
    except Exception as e:
        warn(e)
        warn(f'Create {path} Failed.')
        sys.exit(-1)


def createpath(path):
    return CreatePath(path)


def createfile(path, encoding=None):
    # 文件已存在返回False，成功返回True
    path = standarlizedPath(path)
    root = pathname(path)
    createpath(path)
    name = standarlizedFileName(path[path.rfind('/') + 1:])
    if not path == root + name:
        tip(f'文件名{path}不规范，已重命名为{root + name}')
    path = root + name
    if os.path.exists(path):
        warn(f'{path} alreay exists. 文件已存在')
        return False
    # try:
    if not encoding == None:
        with open(path, 'w') as f:
            ()
    else:
        with open(path, 'wb', encoding=encoding) as f:
            ()
    # except Exception:
    #     warn(f'创建文件{path}未知失败。{str(Exception)}')
    #     return False
    return True


def file(mode, path, IOList=None, encoding=None):
    """
    所有文件with open的封装
    @param mode:
    @param path:
    @param IOList:
    @param encoding:
    @return:列表或是open对象
    """
    try:
        path = standarlizedPath(path)
        createpath(path)
        if (IOList == None or IOList == []) and (mode.find('w') > -1 or mode.find('a') > -1):
            warn(f'可能是运行时错误。写未传参。IOList: {info(IOList)} mode: {mode}')
            sys.exit(-1)
        if not os.path.exists(path) and mode.find('r') > -1:
            warn(f'错误。读不存在文件：{path}')
            return False
        # 比特流
        if mode == 'rb':
            with open(path, mode='rb') as file:
                return IOList + file.readlines()
        # 字符流
        elif mode == 'r':
            with open(path, mode='r', encoding=encoding) as file:
                return IOList + file.readlines()
        elif mode == 'w':
            with open(path, mode='w', encoding=encoding) as file:
                file.writelines(IOList)
                return file
        elif mode == 'wb':
            try:
                with open(path, mode='wb') as file:
                    file.write(IOList)
                    return file
            except:
                with open(path, mode='wb') as file:
                    file.writelines(IOList)
                    return file
        elif mode == 'a':
            with open(path, mode='a', encoding=encoding) as file:
                file.writelines(IOList)
                return file
    except Exception as e:
        warn(e, type(e))
        warn(info(IOList))
        sys.exit(-1)


def DesktopPath(s=''):
    if 'esktop' in s:
        return
    if './' in s:
        s = s[2:]
    if not s == '':
        s = '/' + s
    if s == 'new':
        s = random.randint(0, 99999)
        s = str(s)
        log(f'桌面新建：{s}')
        return standarlizedPath(f"C:/Users/{user}/Desktop/{s}.txt")

    return standarlizedPath(f"C:/Users/{user}/Desktop{s}")


def desktoppath(s=''):
    return DesktopPath(s)


def desktop(s=''):
    return DesktopPath(s)


class txt():
    """
    读写txt文件。l，可以不是字符串，自动追加空格。
    """

    @DebugConsume
    def __init__(self, path, encoding='utf-8', silent=None):
        self.silent = silent
        self.mode = 'txt'
        if encoding == None:
            encoding = 'utf-8'
        self.encoding = encoding
        if path == 'new':
            path = desktoppath('new')
        self.path = standarlizedPath(path)
        if not self.path.find('.') > 0:
            self.path += '.txt'
        self.l = []
        if not os.path.exists(self.path):
            createfile(self.path, encoding=encoding)
            return
        delog(f'文件读 {self.path}')
        for i in file('r', self.path, IOList=[], encoding=encoding):
            self.l.append(str(i).strip('\n'))

    def look(self):
        look(self.path)

    @listed
    def delete(self, s):
        """
        删除字符串相等的行。自动保存。
        @param s:
        @return:
        """
        for i in self.l:
            if i == s:
                self.l.remove(s)
                self.save()
                return

    @DebugConsume
    def set(self, silent=None, sort=False):
        """
        去重，排序，去空，集合化
        @param silent:
        @return:
        """
        if '' in self.l:
            self.l.pop(self.l.index(''))
        if len(self.l) > 20000:
            return
        p = Set(self.l)
        if sort:
            p.sort(key=self.l.index)
        self.l = p
        if not silent == None:
            txt.save(self, 'Rtxt set', silent=silent)
        else:
            txt.save(self, 'Rtxt set', silent=self.silent)

    @listed
    def add(self, i, silent=None):
        if silent == None:
            silent = self.silent
        i = str(i)
        for k in i.split('\n'):
            k = str(k)
            # 如果原来是空的，就不另起一行
            if not self.l == []:
                file('a', self.path, ['\n' + k], encoding='utf-8')
            else:
                file('a', self.path, [k], encoding='utf-8')
            self.l.append(str(k))
            if not silent:
                delog(f'txt add {k}')

    def addline(selfself, i):
        txt.add('\n')
        txt.add(i)

    @consume
    def save(self, s='txt saved', silent=None):
        # 强制覆盖写
        if silent == None:
            silent = self.silent
        slist = []
        if self.l == []:
            slist = ['']
        else:
            for i in self.l[:-1]:
                slist.append(str(i) + '\n')
            slist.append(str(self.l[-1]))
        delog(f'文件写 {self.path}')
        file('w', self.path, slist, encoding=self.encoding)
        if not silent and not self.silent:
            warn(f'{rmtail(tail(self.path), ".txt", strict=False)}({(self.mode)}) - {s}')

    def length(self):
        return len(self.l)

    def clear(self):
        self.l = []
        txt.save(self, '清除')


class RefreshTXT(txt):
    # 实现逐行的记录仓库
    # 实现备份
    # 增删都会执行保存操作。
    @DebugConsume
    def __init__(self, path, encoding=None, silent=None):
        txt.__init__(self, path, encoding, silent)
        self.loopcount = 0
        self.mode = 'Rtxt'
        # self.rollback()
        RefreshTXT.backup(self)
        RefreshTXT.set(self, silent=silent)

    def backup(self, strict=False):
        # region
        backupname = self.path.strip('.txt') + '_backup.txt'
        if not os.path.exists(backupname):
            f = txt(backupname, self.encoding)
            f.l = [nowstr()] + self.l
            f.save('create backup')
        else:
            if counttime(txt(backupname).l[0]) <= 3600 * 24 and strict == False:
                return
            RefreshTXT.set(self)
            f = txt(backupname)
            f.l = [nowstr()] + self.l
            f.save('refresh backup')
        # endregion

    # 根据l并行写入
    @DebugConsume
    def save(self, silent=None):
        if silent == None:
            silent = self.silent
        self.l = Set(self.l + rtxt(self.path, silent=silent).l)
        RefreshTXT.set(self, silent=silent)
        txt.save(self, 'Rtxt 合并保存', silent=silent)

    def get(self, silent=None):
        """
        滚动文本，第一行放最后一行
        @param silent:
        @return: 第一行
        """
        # 要实现并发，需要每次get都从本地中读取
        RefreshTXT.__init__(self, self.path, self.encoding, silent=self.silent)
        if silent == None:
            silent = self.silent
        if len(self.l) < 1:
            return None
        self.l = self.l[1:] + [self.l[0]]
        self.loopcount -= 1
        RefreshTXT.save(self, silent=silent)
        return self.l[-1]

    def rollback(self, silent=None):
        if silent == None:
            silent = self.silent
        self.__init__(self.path, self.encoding, silent=self.silent)
        if len(self.l) <= 1:
            return None
        self.l = [self.l[-1]] + self.l[:-1]
        self.loopcount += 1
        self.save(silent=silent)
        return self.l[0]

    @listed
    def delete(self, i, silent=None):
        if silent == None:
            silent = self.silent
        b = False
        j = dicttojson(i)
        while j in self.l:
            self.l.pop(self.l.index(j))
            b = True
        if not b:
            warn(f'尝试删除但是记录{self.path}中没有以下列表中的任何一个元素 {i}.')
        txt.save(self, f'删除{j}', silent=silent)

    @listed
    def add(self, i, silent=None):
        if silent == None:
            silent = self.silent
        i = str(i)
        i.strip('\n')
        if not i in self.l:
            self.l.append(i)
            file('a', self.path, ['\n' + i], encoding='utf-8')


class jsondata:
    def __init__(self, path, autosave=True):
        """

        @param path:
        @param autosave:
        """
        self.path = standarlizedPath(jsonpath(path))
        self.encoding = 'utf-8'
        self.autosave = autosave
        if not '.json' in self.path:
            self.path += '.json'
        if not isfile(self.path):
            json.dump({}, open(mode='w', file=self.path, encoding=self.encoding))

        self.data = json.load(open(mode='r', file=self.path, encoding=self.encoding))

    def remove(self, s):
        if isinstance(s, dict):
            for k in s.keys():
                if k in self.data:
                    del self.data[k]
        elif isinstance(s, str):
            if s in self.data:
                del self.data[s]
        if self.autosave:
            self.save()

    def clear(self):
        self.data = {}
        if self.autosave:
            self.save()

    def delete(self, *a, **b):
        self.remove(*a, **b)

    def save(self):
        json.dump(self.data, open(mode='w', file=self.path, encoding=self.encoding))

    def get(self, s):
        return self.data.get(s)

    def add(self, d):
        for key, value in d.items():
            if key in self.data:
                if type(self.data[key]) == list:
                    self.data[key].append(value)
                else:
                    self.data[key] = [self.data[key], value]
            else:
                self.data[key] = value
        if self.autosave:
            self.save()

    def setdata(self, d):
        self.data = d
        self.save()


class Json(txt):
    """
    txt转json，一行一个json
    """

    def __init__(self, path, encoding=None, silent=None):
        txt.__init__(self, path, encoding)
        self.addtodict()

    def addtodict(self):
        self.d = {}
        for i in self.l:
            if i == '':
                continue
            try:
                self.d.update(jsontodict(i))
            except:
                warn(self.path)
                warn(f'-{i}-')
                print(type(i))
                print(info(i))
                sys.exit(-1)

    def get(self):
        ret = self.l[0]
        if ret == '':
            self.l.pop(0)
            self.save()
            return Json.get(self)
        return jsontodict(ret)

    def add(self, d):
        txt.add(self, dicttojson(d))
        self.d.update(jsontodict(d))


class RefreshJson(Json, RefreshTXT):
    @DebugConsume
    def __init__(self, path, encoding=None, silent=None):
        RefreshTXT.__init__(self, path, encoding=encoding, silent=silent)
        RefreshJson.depart(self)
        Json.addtodict(self)
        RefreshJson.set(self, silent=silent)
        self.mode = 'Rjson'

        #     非列表的安全检查
        if self.length() > 0 and not list == type(value(jsontodict(self.l[0]))):
            Exit(f'{self.path}似乎不是列表。')

    # depatch
    # segment
    # 有时会产生异常，多行没有换行。分开。
    def depart(self, silent=None):
        if silent is None:
            silent = self.silent
        addl = []
        dell = []
        for i in self.l:
            if '}{' in i:
                newl = i.split('}{')
                newl[0] = newl[0][1:]
                newl[-1] = newl[-1][:-1]
                addl += newl
                dell.append(i)
        for j in addl:
            RefreshTXT.add(self, '{' + j + '}', silent=silent)
        for i in dell:
            RefreshTXT.delete(self, i, silent=silent)

    # 返回列表，所有的record，一个value对应一个key
    def all(self):
        ret = []
        for i in range(self.length()):
            ret += self.get()
        return ret

    # 返回值的键
    def find(self, v):
        for i in self.all():
            if v == value(i):
                return key(i)

    @DebugConsume
    def get(self, silent=None):
        """
        本地存储值是列表，返回所有键值对（拆开成列表）
        @return: 第一行放最后一行，并返回这一行

        """
        if silent is None:
            silent = self.silent
        dstr = (RefreshTXT.get(self, silent=silent))
        try:
            d = jsontodict(dstr)
        except Exception as e:
            if type(e) in [ValueError] and '}{' in dstr:
                #         先分割
                RefreshJson.depart(self, silent=silent)
                #         在返回全部的列表
                newl = dstr.split('}{')
                newl[0] = newl[0][1:]
                newl[-1] = newl[-1][:-1]
                ret = []
                for j in newl:
                    j = '{' + j + '}'
                    ret += RefreshJson.get(j)
                return ret
            else:
                Exit(f'{e}')
        ret = []
        if value(d) == []:
            return [{key(d): None}]
        for i in value(d):
            ret.append({key(d): i})
        return ret

    def add(self, d, silent=None):
        if silent == None:
            silent = self.silent
        d = jsontodict(d)

        if list == type(value(d)):
            for i in value(d):
                rjson.add(self, {key(d): i}, silent=silent)
            return

        for i in self.l:
            din = jsontodict(i)
            if key(din) == key(d):
                if value(d) in value(din):
                    return
                RefreshTXT.delete(self, dicttojson(din), silent=silent)
                try:
                    din = {key(d): list(Set([value(d)] + value(din)))}
                except Exception as e:
                    print(din)
                    print(d)
                    Exit(e)
                RefreshTXT.add(self, dicttojson(din), silent=silent)
                self.d.update(din)
                return

        d = {key(d): [value(d)]}
        RefreshTXT.add(self, dicttojson(d), silent=silent)
        self.d.update(d)

    @consume
    # 合并相同的键
    def set(self, silent=None):
        if silent == None:
            silent = self.silent
        allkey = []
        for dstr in self.l:
            d = jsontodict(dstr)
            k = key(d)

            if not k in allkey:
                allkey.append(k)
                continue

            dlis = []
            values = []
            for i in self.l:
                ii = jsontodict(i)
                if not key(ii) == k:
                    continue
                dlis.append(i)
                values += [value(ii)]
                try:
                    values = list(Set(values))
                except:
                    print(values)
                    Exit()
            RefreshTXT.delete(self, dlis, silent=silent)
            RefreshJson.add(self, {k: values}, silent=silent)

    def rollback(self):
        d = jsontodict(RefreshTXT.rollback(self))
        ret = []
        for i in value(d):
            ret.append({key(d): i})
        return ret

    @listed
    @consume
    def delete(self, i, silent=None):
        if silent == None:
            silent = self.silent
        i = jsontodict(i)
        if list == type(value(i)):
            for j in value(i):
                RefreshJson.delete(self, {key(i): j}, silent=silent)
            return

        for j in self.l:
            din = jsontodict(j)
            if not key(din) == key(i):
                continue
            newvalue = value(din)
            if value(i) in newvalue:
                newvalue.remove(value(i))
            newd = {key(din): newvalue}

            RefreshTXT.delete(self, j, silent=silent)
            if not newvalue == []:
                RefreshTXT.add(self, dicttojson(newd), silent=silent)
            else:
                RefreshJson.delete(self, dicttojson({key(din): []}), silent=silent)
            self.d.update(newd)
            break

    def pieceinfo(self, num, author, title, extra=None):
        diskname = getdiskname()
        if extra in ['', None]:
            return json.dumps({str(num): {'disk': diskname, 'author': author, 'title': title}},
                              ensure_ascii=False)
        else:
            # 有额外信息
            if type(extra) in [dict]:
                din = {'disk': diskname, 'author': author, 'title': title}
                for i in extra:
                    din.update({i: extra[i]})
                ret = {str(num): din}
                return json.dumps(ret, ensure_ascii=False)
            elif type(extra) in [str]:
                return json.dumps({str(num): {'disk': diskname, 'author': author, 'title': title}},
                                  ensure_ascii=False)

    def addpiece(self, num, author, title, extra=None):
        """

        @param num: 作品唯一标识符
        @param author: 作者
        @param title: 标题
        @param extra: 附加信息字符串
        @return:
        """
        piece = jsontodict(self.pieceinfo(num, author, title, extra))
        self.add(piece)

    def adduser(self, uid, author):
        self.add({uid: author})


class cache():
    """
    dict
    """

    def __init__(self, path, silent=None, json=True):
        self.silent = silent
        self.path = path
        self.json = json

    def get(self, silent=False):
        """
        删除。如果失误直接删除
        @param silent:
        @return:首条。
        """
        if self.silent:
            silent = True
        while True:
            try:
                f = txt(self.path)
                if f.l == []:
                    return
                if self.json:
                    s = jsontodict(f.l[0])
                    if not s:
                        f.delete(f.l[0])
                        return self.get()
                else:
                    s = f.l[0]
                f.l.pop(0)
                f.save('cache get', silent=silent)
                if s == None:
                    s = self.get()
                return s
            except Exception as e:
                warn(e)
                warn('cache获取失败。正在重试')
                sleep(2)

    def add(self, s, silent=False):
        if self.silent:
            silent = True
        if self.json:
            s = dicttojson(s)
        f = txt(self.path)
        f.add(s, silent=silent)
        f.save(f'cache added{s}', silent=silent)

    def length(self):
        return txt(self.path).length()


def rtxttorjson(path):
    f = txt(path)
    l = f.l
    f.l = []
    f.save()
    for i in l:
        f.l.append(dicttojson({i: []}))
    f.save()


class rtxt(RefreshTXT):
    pass


class rjson(RefreshJson):
    pass


# endregion

#  日志
# region
def context(step=0, show=False):
    """
    返回程序上下文
    @param step:
    @param show:是否通过txt显示
    @return:
    """
    if step < 0:
        return None
    frame = inspect.currentframe()
    ret = []
    # 调试模式pydev和运行是不一样的
    for i in range(step):
        try:
            frame = frame.f_back
            if not frame == None:
                framed = inspect.getframeinfo(frame)
                d = {}
                d.update({'module': framed.function})
                d.update({'function': framed.function})
                d.update({'code': framed.code_context})
                d.update({'code_context': framed.code_context})
                d.update({'file': framed.filename})
                d.update({'filename': framed.filename})
                d.update({'line': framed.lineno})
                d.update({'lineno': framed.lineno})
                ret.append(d)
        except:
            break
    if show:
        f = txt(cachepath('context.txt'))
        f.add(ret)
        f.save()
        look(f.path)
    return ret


def stepback(*a, **b):
    return context(*a, **b)


def traceback(*a, **b):
    return context(*a, **b)


def backtrace(*a, **b):
    return context(*a, **b)


def WARN(s):
    now = Time()
    hotkey('win', 'd')
    win32api.MessageBox(None, s, f'Kaleidoscope{now.time()}', win32con.MB_OK)


def alert(s=''):
    # t=Time()
    p = pool(1)

    def do():
        win32api.MessageBox(0, s, Time.time(Time()), win32con.MB_OK)

    p.execute(do, )


def console(s, duration=999, text_color='#F08080', font=('Hack', 14), size=28):
    #  每当新的控制台启动后，改内容，然后开新进程，将0改为1，1改为0
    # 控制台每隔一段时间刷新，如果变为0则退出。
    # 新的控制台计时结束后，将1改为0
    refreshtime = 0.6
    consoletxt.add({nowstr(): s})
    while 3600 < Now().counttime(Time(key(jsontodict(consoletxt.get())))):
        consoletxt.l.pop(0)
    consoletxt.save()

    # 短暂显示桌面控制台
    def show():
        # 系统默认颜色
        # COLOR_SYSTEM_DEFAULT='1234567890'=='ADD123'
        global win
        outs = ''
        inc = 0
        for i in consoletxt.l:
            outs += f'[{inc}]  {value(i)}\n'
            inc += 1
        layout = [[PySimpleGUI.Text(outs, background_color='#add123', pad=(0, 0),
                                    text_color=text_color, font=font)]]
        win = PySimpleGUI.Window('', layout, no_titlebar=True, keep_on_top=True,
                                 location=(120 * 16 / 3 * 2, 0), auto_close=True,
                                 auto_close_duration=duration,
                                 transparent_color='#add123', margins=(0, 0))
        event, values = win.read(timeout=0)
        sleep(0.3)
        return win

    def func(duration, ):
        delog('1')
        return
        # 更改consolerunning
        if consolerunning.l[0] == '1':
            consolerunning.l[0] == '0'
            consolerunning.save()
        elif consolerunning.l[0] == '0':
            consolerunning.l[0] == '1'
            consolerunning.save()
        while duration > 0:
            sleep(refreshtime)
            duration -= refreshtime
            show()

    process = multiprocessing.Process(target=func, args=(duration,))
    # process.daemon=True
    process.start()


def Log(s, front=242, font=1, background=238):
    global Logcount
    # 最大的每行字符长度
    m = 250
    try:
        s = str(s)
        s.replace(u'\xa0', u'<?>')
        s1 = ''
        if len(s) > m:
            s1 = s[m:]
            s = s[:m]
        s = s.ljust(m, '\t')
        if Logcount >= 100:
            sss = f'[{Logcount}]' + CMD.reset()
        else:
            sss = CMD.reset()
        print(sss,
              CMD.background(background), CMD.front(244), realtime(),
              CMD.front(front), CMD.font(font), s, CMD.resetall(), CMD.background(background),
              CMD.reset())
        Logcount += 1
        if not s1 == '':
            Logcount -= 1
            Log(s1[m:], front, font, background)
    except Exception as e:
        warn(f'这条日志输出失败了。原因{e}')


@listed
def log(*a):
    s = ''
    for i in a:
        s += str(i)
    Log(s, 148)


@listed
def tip(*a):
    s = ''
    for i in a:
        s += str(i)
    Log(s, 248, 9)


@listed
def delog(*a):
    if a in [(), [], None]:
        Log('continuing', 75)
        return
    s = a[0]
    if not s in [0, -1, 'beign', 'end', 'a', 'z']:
        s = ''
        for i in a:
            s += str(i) + ' '
    if not debug:
        return
    if s == 0 and type(s) == int:
        delog('is Processing.')
        return
    if s == -1:
        # 手动打终点断点，所以会退出
        delog('已处理。准备退出。')
        sys.exit(0)
        return
    dic = {
        'begin': 'Announce Begin',
        'end': "Announce End",
        'a': 'Announce Begin',
        'z': "Announce End"
    }
    try:
        if str(s) in dic.keys():
            s = dic.get(s)
    finally:
        Log(s, 75)


def warn(*a):
    """

    @param a:
    @return:
    """
    s = ''
    for i in a:
        s += str(i)
        if issubclass(type(i), Exception):
            s += str(type(i))
    Log(s, 166)


# endregion

# 基础数据结构
# region
def SortedName(l):
    """
    自动排序名字
    @param l:
    @return:
    """
    d = []
    for i in l:
        i, ext = extentionandname(i, exist=False)
        ret = research(r'_\d+$', i)
        if ret:
            d.append((rmtail(i, ret.group()), ret.group(), ext))
            continue
        ret = research(r'\d+$', i)
        if ret:
            d.append((rmtail(i, ret.group()), ret.group(), ext))
            continue
        d.append((i, '', ext))
    d.sort(key=lambda x: (x[0], Int(x[1]), x[2]))
    l = []
    for i in d:
        l.append(i[0] + i[1] + i[2])
    return l


# 实现包括None在内的int转换
def Int(s):
    if s in [None, False, '']:
        return 0
    return int(s)


# 实现包括列表元素为字典在内的集合化，不改变原来的顺序
def Set(l):
    res = []
    if l == None:
        return []
    for i in l:
        if i in res:
            continue
        res.append(i)
    return res


def simplinfo(num, author, title, diskname=None):
    if diskname == None:
        diskname = getdiskname()
    return json.dumps({str(num): {'disk': diskname, 'author': author, 'title': title}},
                      ensure_ascii=False)


class MyError(BaseException):
    pass


def jsontodict(s):
    """

    @param s:
    @return: 如果转换失败返回False
    """
    if type(s) == dict:
        return s
    if s == '' or s == None or s == []:
        warn(f'{s, type(s)}')
        return
    try:
        return json.loads(s)
    except Exception as e1:
        warn(['解析字符为 json 错误\n',s, e1])
        return False


def dicttojson(s):
    if type(s) == str:
        return s
    try:
        return json.dumps(s, ensure_ascii=False)
        # return str(s)
    except Exception as e:
        warn(e)
        return ''


def key(d):
    return keys(d)[0]


def keys(d):
    if not type(d) == dict:
        warn(f'用法错误。d的类型为{type(d)}')
    return list(d.keys())


@listed
def value(d):
    d = jsontodict(d)
    if not type(d) == dict:
        warn(f'用法错误。d的类型为{type(d)}')
    return d[key(d)]


def values(d):
    d = jsontodict(d)
    # ret=[]
    # for i in d:
    #     ret.append(d[i])
    # return ret
    return list(d.values())


# endregion

# 字符串
# region
# 正则


def TellStringSame(s1, s2, ratio=1):
    s1 = str(s1)
    s2 = str(s2)
    if len(s1) > 3 and len(s2) > 3:
        if s1.rfind(s2) >= 0 or s2.rfind(s1) >= 0:
            return True
    if len(s1) / len(s2) < ratio / 2 or len(s2) / len(s1) < ratio / 2:
        return False

    if len(s1) > 5:
        for i in range(max(int(len(s1) * (1 - ratio)), 1)):
            if s1[i:min(len(s1), i + int(len(s1) * ratio))] in s2:
                return True
    if len(s2) > 5:
        for i in range(max(int(len(s1) * (1 - ratio)), 1)):
            if s2[i:min(len(s2), i + int(len(s2) * ratio))] in s1:
                return True
    return False


def tellstringsame(s1, s2):
    # 只对中文开放
    return TellStringSame(s1, s2)


# 去除字符串末尾
def Strip(s, tail, strict=False):
    if not type(s) in [str] and type(tail) in [str]:
        warn(f's tail中有不为字符')
        Exit(s, tail)
    if s[-len(tail):] == tail:
        return s[:-len(tail)]
    else:
        return s


# 正则查找
def refind(s, re):
    return re.findall(s, re)


def cuttail(s, mark='_', strict=False):
    """
    截取字符串末尾
    @param s:
    @param mark:
    @param strict: 不包括mark
    @return:
    """
    if type(s) == list:
        warn('用法错误。')
        sys.exit(-1)
    if mark == None:
        return s
    s, mark = str(s), str(mark)
    t = tail(s, mark, strict=strict)
    s = s[:(s.rfind(mark))]
    return s, t


def splittail(s, mark):
    return cuttail(s, mark)


def removetail(l, mark='.', strict=False):
    return cuttail(l, mark, strict=strict)[0]


def rmtail(*a, **b):
    return removetail(*a, **b)


def strip(s, mark):
    pass


# 截取字符串末尾
def tail(s, mark='/', strict=True):
    return gettail(s, mark, strict=strict)


def gettail(s, mark='/', strict=True):
    """
    找到最右侧匹配
    @param s:
    @param mark:
    @param strict:不包括mrak
    @return:
    """
    s, mark = str(s), str(mark)
    if not mark in s:
        if strict:
            warn(stepback(2))
            Exit(f'tail失败。字符串 {s} 中没有预计存在的子串：  {mark}。', (s, mark))
        else:
            return s
    return s[s.rfind(mark) + len(mark):]


def strre(s, pattern):
    return (re.compile(pattern).findall(s))


# endregion

# 分布式
# region
# 获取用户个性化设置
def getsettings(k=None):
    if not type(k) in [str]:
        Exit(f'键错误。{info(k)}')
    f = Json(settingspath('all.txt'))
    return f.d[k]


# 检查磁盘是否可用（待机）
def checkdiskusable(s):
    s = s[0]
    Open(f'{s}:/diskInfo.txt')


def setRootPath(dname=None, d=None, strict=True):
    """
    动态更改操作盘
    @param d:盘符
    @param dname:False则自动分配；字符串表示操作盘唯一标识符，可以列表
    @param strict:非严格模式下，找不到唯一标识符则开始创建
    @return:唯一标识符，失败为False
    """
    global diskpath, diskname, disknames
    disknames = rjson(projectpath('disknames.txt'), silent=True)
    if d:
        return initdisk(d, strict=strict)
    else:
        # 自动分配
        if dname == False:
            return initdisk('d')
        # 空参
        if dname in [None, []]:
            if strict:
                Exit('传空参，未指定磁盘。')
            else:
                ret = initdisk()
        if type(dname) in [list]:
            for dname in dname:
                ret = setRootPath(dname=dname)
                if ret:
                    return ret
            if strict:
                Exit(f'未找到磁盘{dname}。')
            return False
        if type(dname) in [str, int]:
            for i in ['c', 'd', 'e', 'g', 'f', 'h']:
                if isfile(f'{i}:/diskInfo.txt'):
                    f = rjson(f'{i}:/diskInfo.txt')
                    if f.d['name'][0] == dname:
                        return initdisk(i)
            if strict:
                Exit(f'未找到磁盘{dname}')
            else:
                return False
    return False


def confirmRootPath(name):
    return getdiskname() == name


def setrootpath(*a, **b):
    setRootPath(*a, **b)


def initdisk(d=None, strict=False):
    """
    重设工作根目录
    @param d: 为空则自动顺序查找
    @param strict:严格模式退出。非严格模式返回diskname
    @return:不存在路径返回False
    """
    global diskname, diskpath, disknames
    # 为空
    if d == None:
        for d in getsettings('defaultDisk'):
            if not isdir(f'{d}:/'):
                continue
            else:
                return initdisk(d)
            return False
    else:
        if isdir(f'{d}:/'):
            diskpath = d
            os.chdir(f'{d}:/')
            if isfile(f'./diskInfo.txt'):
                diskname = getdiskname()
            else:
                c = input(f'准备{d.upper()}盘。请输入为磁盘起名（需唯一）')
                while c in disknames.d['name']:
                    c = input(f'已有命名。请重新输入。')
                disknames.add({'name': c})
                disknames.save()
                diskinfo = rjson(f'./diskInfo.txt')
                diskinfo.add({'name': c})
                diskinfo.save()
                diskname = c
            log(f'operating disk {diskpath.upper()}（{diskname}）')
            return diskname


def getdiskname():
    """
    获取当前操作盘的唯一标识符
    @return:解析失败则返回False
    """
    diskinfo = RefreshJson('./diskInfo.txt', silent=True)
    global disknames, diskname
    diskname = diskinfo.d['name'][0]
    disknames.add({'name': diskname})
    return diskname


# endregion

# 爬虫
# region
#  爬取论坛的每一页
def forum(firsturl, titletail, hostname, func1, func2, func3, minsize=(150, 150), t=3, scale=200,
          saveuid=True, look=True, mine=True, silent=False):
    if firsturl == '':
        return
    # uid是否文件夹注入帖子uid前缀
    #     先打开第一页，获取标题，每页数
    page = Chrome(mine=mine, silent=silent)
    page.get(firsturl)
    sleep(t)
    title = page.title()
    if ' ' + titletail in title:
        title = removetail(title, ' ' + titletail)
    if titletail in title:
        title = removetail(title, titletail)
    # func1  返回当前帖子的Uid
    uid = func1(page.url())
    # 把以前的帖子重命名
    pastcount = 0
    if isdir(collectionpath(f'{hostname}/{uid}_{title}')):
        pastcount += 1
        while isdir(collectionpath(f'{hostname}/{uid}_{title}_{pastcount}')):
            pastcount += 1
    if isdir(collectionpath(f'{hostname}/{title}')):
        pastcount += 1
        while isdir(collectionpath(f'{hostname}/{title}_{pastcount}')):
            pastcount += 1
    if pastcount == 0:
        pastcount = ''
    else:
        pastcount = f'_{pastcount}'
    delog(pastcount)

    if saveuid:
        page.save(collectionpath(f'{hostname}/{uid}_{title}{pastcount}/第1页/'), minsize=minsize,
                  direct=True, look=look, scale=scale)
    else:
        page.save(collectionpath(f'{hostname}/{title}{pastcount}/第1页/'), minsize=minsize,
                  direct=True, look=look, scale=scale)
    # func2  根据帖子的uid，返回后面的每页的urllist
    urllist = func2([page, uid])
    page.quit()
    count = 1
    for url in urllist:
        count += 1
        page = Chrome(url, mine=True, silent=True)
        # func3  检查后面的每页是否被反爬了
        func3([page])
        if saveuid:
            page.save(collectionpath(f'{hostname}/{uid}_{title}{pastcount}/第{count}页/'),
                      minsize=minsize, direct=True, look=look, scale=scale)
        else:
            page.save(collectionpath(f'{hostname}/{title}{pastcount}/第{count}页/'), minsize=minsize,
                      direct=True, look=look, scale=scale)
        page.quit()


def linkedspider(*a, **b):
    return forum(a, **b)


# 转到已经打开的edge并保存全部截屏
def getpics(loop, path):
    for i in range(loop):
        hotkey('ctrl', 'shift', 's')
        sleep(1)
        click(1146, 174)
        # 截图生成时间
        sleep(4)
        old = listfile('D:/')
        click(1700, 112)
        # 截图下载时间
        sleep(2)
        new = listfile('D:/')
        for j in new:
            if j in old:
                continue
            else:
                break
        move(j, f'{path}.{gettail(j, ".")}')


def geturls(loop=1, func=None, type='edge'):
    """
    获取已打开浏览器的所有链接
    @param loop:
    @param func:处理每次get到的url
    @param type:浏览器类型
    @return:
    """
    ret = []
    hotkey('alt', 'tab')
    for i in range(loop):
        click(cachepath(type + 'url.png'), xoffset=80)
        hotkey('ctrl', 'c')
        c = pyperclip.paste()
        if func:
            c = func(c)
        ret.append(c)
        hotkey('ctrl', 'w')
    hotkey('alt', 'tab')
    return ret


# 将网页置顶显示
def alertpage(l):
    page = l[0]
    page.switch_to.window(page.window_handles[0])


def Element(l, s, method=By.XPATH, depth=5, silent=debug, strict=True):
    res = Elements(l, s, depth=depth, silent=silent, method=method, strict=strict)
    if res == []:
        return None
    else:
        return res[0]


def Elements(l, s, depth=7, silent=True, method=By.XPATH, strict=True):
    """
    :param l:根元素
    :param s:字符表达式
    :return:元素列表，找不到为[]
    """
    root = l[0]
    s.replace('\'', '\"')
    # 重写xpath语法规则
    s = s.replace('span', '*[name()="span"]')
    s = s.replace('//@', '//*/@')
    s = s.replace('//text()', '//*/text()')
    atr = None
    if '/text()' in s:
        s = Strip(s, '/text()')
        atr = 'text'
    if '/@' in s:
        s, atr = cuttail(s, '/@')
    ret = root.find_elements(method, s)
    if len(ret):
        if atr == None:
            return ret
        if atr not in ['text']:
            return [i.get_attribute(atr) for i in ret]
        else:
            return [i.text if i.text else i.get_attribute('text') for i in ret]
    else:
        sleep(2)
        if depth >= 10:
            message = (f'最终未获取到元素。 method={method},str={s}')
            if strict:
                Exit(message)
            if not silent:
                warn(message)
            return []
        else:
            return Elements(l, s, depth=depth + 1, method=method, strict=strict)


def elements(*a, **b):
    return Elements(*a, **b)


def element(*a, **b):
    return Element(*a, **b)


def skip(l, s, method=By.XPATH, strict=False):
    """
    简单等待，不做操作，等待人工操作
    :param l:页面
    :return:
    """
    page = l[0]
    sleep(1)
    if Element(l, s, depth=8, silent=True, method=method, strict=strict):
        warn(f'{s} detected. 等待其消失中以继续。。。')
        alertpage([page])
        WebDriverWait(page, 99999, 3).until_not(
            expected_conditions.presence_of_element_located(locator=(method, s)))
        sleep(2)


def getscrolltop(l):
    page = l[0]
    return page.execute_script('var q=document.documentElement.scrollTop;return(q)')


def scrollwidth(l):
    page = l[0]
    return page.execute_script('var q=document.documentElement.scrollWidth;return(q)')


# 获取页面最大高度（通过滚动条
def scrollheight(l):
    page = l[0]
    return float(page.execute_script('var q=document.documentElement.scrollHeight;return(q)'))


@consume
def scroll(l, silent=None, x=None, y=None, ratio=1, t=1, ite=None):
    """
    移动到元素、不断下滚
    @param l:
    @param silent:
    @param x:
    @param y:
    @param ratio:
    @param t:下滚刷新间隔
    @param ite:
    @return:
    """
    if not type(l) in [list]:
        if not x == None:
            pyautogui.moveTo(x, y)
            sleep(0.2)
        flag = l / abs(l)
        while abs(l) > 101:
            l = abs(l) - 100
            x = flag * -100
            pyautogui.scroll(int(x))
        return

    # 循环判断下滚
    if silent == None:
        log('滚动中..')
    page = l[0]
    ratio = ratio
    ScrollTop = -1
    while ScrollTop != getscrolltop([page]):
        # 一个下滑到底并且再下滑一下的模仿人的动作，并且更新ScrollTop
        def doubledown(l, ite):
            nonlocal ScrollTop
            page = l[0]
            if ScrollTop == getscrolltop([page]):
                return False
            page.execute_script(
                f'document.documentElement.scrollTop=document.documentElement.scrollHeight*{ratio}')
            page.execute_script(
                f'document.documentElement.scrollTop=document.documentElement.scrollHeight-20')
            ScrollTop = getscrolltop([page])
            sleep(t)
            page.execute_script(
                f'document.documentElement.scrollTop=document.documentElement.scrollHeight*{ratio}')
            sleep(t)

            # 有限下滑次数
            if type(ite) in [int]:
                ite -= 1
                if ite < 0:
                    return False
            return True

        while doubledown([page], ite):
            pass


def requestdownload(path, url, mode='wb'):
    """

    @param path: 目标路径
    @param url: 源 url
    @param mode:
    @return:
    """
    path = standarlizedPath(path)
    CreatePath(path)
    try:
        with open(path, mode) as f:
            f.write(requests.get(url=url, headers=headers).content)
    except(requests.exceptions.SSLError):
        try:
            with open(path, mode) as f:
                f.write(requests.get(url=url, headers=headers, verify=False).content)
        finally:
            input('SSLError')
            requestdownload(path, mode, url)


def chrome(url='', mine=None, silent=None, t=100, mute=True):
    if not url in ['', None] and not 'http' in url:
        url = 'https://' + url
    options = webdriver.ChromeOptions()
    # options.page_load_strategy = 'none'
    op = ''
    if not silent in [None, False]:
        if mine:
            options.add_argument('--headless=new')
        else:
            options.add_argument("--headless")
    if mute:
        options.add_argument('mute-audio')
        delog('浏览器打开静音')
    if mine:
        options.add_argument(
            f"--user-data-dir=C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data")
    # options.add_experimental_option("excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(t)
    driver.set_script_timeout(t)
    try:
        if not url in [None, '']:
            driver.get(url)
        return driver
    except selenium.common.exceptions.InvalidArgumentException as e:
        warn(e, url)
        driver.quit()
        warn(f'旧页面未关闭。请关闭。或者是因为{url}中没有http or https请求')
        c = input()
        return chrome(url=url, mine=mine, silent=silent, t=t)


class Edge():
    def __init__(self, url=None, silent=None, driver=None, mine=False, mute=False):
        if not driver == None:
            self.driver = driver[0]
            return
        else:
            self.driver = edge(url='', silent=silent, mine=mine, mute=mute)
        if not url == None:
            self.get(url)
        self.silent = silent
        self.mine = mine
        self.type = 'edge'
        self.set_window_size(900, 1000)

    @consume
    def download(self, url, path, t=15, silent=True, depth=0, auto=None, redownload=None,
                 overwrite=False):
        """
        浏览器自动重命名 '~' 为 '_'
        @param url:
        @param path: 必须指定文件名，建议指定后缀名。文件名自动重命名"~"为"_"
        @param t:下载和下载后浏览器自动安全检查的时间
        @param silent:
        @param depth:
        @param auto:是否是打开页面即自动下载
        @param overwrite: 覆盖下载或是覆盖移动
        @param redownload: 一定会重新下载。
        @return:True 下载了并且下载成功；False 下载了但是下载失败；字符串 返回检测到的以前的错误命名
        """

        path = standarlizedPath(path)
        defaultpath = userpath('Downloads/')
        previouscontent = listfile(defaultpath)
        if not redownload:
            #     已下载
            if exists(path) and not size(path) == 0:
                if not overwrite:
                    log(f'{path} 已存在，将不下载')
                    return True
                else:
                    move(path, cachepath(f'trashbin/{now()}'))

        def recursive():
            """

            @return:
            """
            sleep(t)
            self.close()
            self.switchto(previouspage)
            sleep(1)
            delog(f'正在检测是否下载到了路径 {root}')
            move([x for x in set(listfile(defaultpath)) if x not in set(previouscontent)][0],
                 root + '/', overwrite=overwrite, autorename=redownload)
            for ii in listfile(root):
                if name in ii and '.crdownload' in ii:
                    deletedirandfile(ii)
                    warn(f'{t}s后下载失败。没有缓存文件存留（自动删除） 请手动尝试 {url}')
                    return pagedownload(url, path, t=t + t, depth=depth + 1, silent=silent,
                                        auto=auto, redownload=redownload, overwrite=overwrite)
                if name in ii:
                    if redownload:
                        move(ii, path, autorename=redownload, overwrite=overwrite)
                    return True
            warn(f'{t}s后下载失败。没有检测到缓存文件  请手动尝试 {url}')
            return False

        # 递归停止条件
        if depth > 5:
            warn('最终下载失败。没有缓存文件存留（自动删除） 请手动尝试 {url}')
            return False

        createpath(path)
        path = standarlizedPath(path, strict=True)
        path = path.replace('~', '_')

        if redownload:
            root = standarlizedPath(cachepath('pagedownload/'), strict=True)
        else:
            root = (path[:path.rfind('\\')])
        name = path[path.rfind('\\') + 1:]

        # 打开页面
        try:
            previouspage = self.driver.current_window_handle
            self.open(url)
            if tellstringsame(self.title(), '403'):
                warn(f'这个url已经被服务器关闭  403  ：{url}')
                return False

        except Exception as e:
            warn(e)
            warn(type(e))
            sys.exit(-1)

        i = 0
        # 如果这个链接打开就能自动下载
        if not auto == None:
            return recursive()

        while i < 10:
            previouscontent = listfile(defaultpath)
            # 什么？？？竟然要尝试10次，哈哈哈真是笑死我了
            try:
                self.driver.execute_script(f"const a1=document.createElement('a');\
                a1.href='{url}';\
                a1.download='{name}';\
                a1.click();")
                # root必须存在，否则会跳出为另存为
                delog(f'pagedownload 正在下载 {url} 到 {root}')
                break
            except Exception as e:
                warn('下载重试中...')
                warn(e)
                warn(type(e))
                i += 1

        return recursive()

    def click(self, *a, strict=True, depth=9):
        if len(a) > 1:
            # ActionChains(self.driver).move_to_element(to_element=Element(s)).click().perform()
            Exit(' 未实现')
        s = a[0]
        if s == None:
            return
        if type(s) in [str]:
            return Edge.click(self, self.element(s, strict=strict, depth=depth))
        if type(s) in [selenium.webdriver.remote.webelement.WebElement]:
            try:
                s.click()
            except:
                try:
                    ActionChains(self.driver).move_to_element(to_element=s).click().perform()
                    return
                except Exception as e:
                    warn(['clickelement error！', e])

    def skip(self, s, strict=False, click=False):
        if not click:
            return skip([self.driver], s, strict=strict)
        e = self.element(s, strict=False)
        if not e == None:
            self.click(e)

    def extendtofull(self, x=None):
        if not self.silent:
            Exit('不支持非静默模式调用')
        self.down()
        if x is None:
            x = self.get_window_size()[0]
        self.set_window_size(x, self.getscrollheight())

    def excutejs(self, jsname):
        if not '.js' in jsname:
            jsname += '.js'
        self.driver.execute_script(''.join(txt(jspath(jsname)).l))

    def get_window_size(self):
        return self.driver.get_window_size()['width'], self.driver.get_window_size()['height']

    def nearend(self):
        """
        判断是否接近底部

        @return:
        """
        return self.getscrolltop() + self.get_window_size()[1] - self.getscrollheight() > 130

    def Down(self, *a, start=0, end=None, scale=100, func=None, pause=1, **b):
        """
        边下滚边执行函数
        @param start:
        @param end:
        @param scale:
        @param func:第一次首参为None，二参为self，循环下滚执行
        @param pause:
        @return:[] 或者 None
        """
        self.scroll(start)
        ret = []
        while True:
            if (not end == None and self.getscrolltop() < end):
                break

            if not func == None:
                ret1 = func(ret, [self], *a, **b)
                if not ret1 == None:
                    ret += ret1
            self.scroll(scale + self.getscrolltop())

            if self.nearend():
                break
            sleep(pause)
        return ret

    # 历史后退
    def backward(self):
        self.driver.back()

    # 历史前进
    def forward(self):
        self.driver.forward()

    # 局内按键
    def hotkey(self, *a):
        for s in a:
            # region
            if s == 'left':
                ActionChains(self.driver).key_down(Keys.ARROW_LEFT).perform()
            elif s == 'right':
                ActionChains(self.driver).key_down(Keys.ARROW_RIGHT).perform()
            elif s == 'up':
                ActionChains(self.driver).key_down(Keys.ARROW_UP).perform()
            elif s == 'down':
                ActionChains(self.driver).key_down(Keys.ARROW_DOWN).perform()
            elif s == 'enter':
                ActionChains(self.driver).key_down(Keys.ENTER).perform()
            elif s == 'esc':
                ActionChains(self.driver).key_down(Keys.ESCAPE).perform()
            elif s == 'backspace':
                ActionChains(self.driver).key_down(Keys.BACKSPACE).perform()
            elif s == 'tab':
                ActionChains(self.driver).key_down(Keys.TAB).perform()
            elif s == 'space':
                ActionChains(self.driver).key_down(Keys.SPACE).perform()
            elif s == 'ctrl':
                ActionChains(self.driver).key_down(Keys.CONTROL).perform()
            elif s == 'alt':
                ActionChains(self.driver).key_down(Keys.ALT).perform()
            elif s == 'shift':
                ActionChains(self.driver).key_down(Keys.SHIFT).perform()
        #     # endregion
        for s in a:
            #         region
            if s == 'left':
                ActionChains(self.driver).key_up(Keys.ARROW_LEFT).perform()
            elif s == 'right':
                ActionChains(self.driver).key_up(Keys.ARROW_RIGHT).perform()
            elif s == 'up':
                ActionChains(self.driver).key_up(Keys.ARROW_UP).perform()
            elif s == 'down':
                ActionChains(self.driver).key_up(Keys.ARROW_DOWN).perform()
            elif s == 'enter':
                ActionChains(self.driver).key_up(Keys.ENTER).perform()
            elif s == 'esc':
                ActionChains(self.driver).key_up(Keys.ESCAPE).perform()
            elif s == 'backspace':
                ActionChains(self.driver).key_up(Keys.BACKSPACE).perform()
            elif s == 'tab':
                ActionChains(self.driver).key_up(Keys.TAB).perform()
            elif s == 'space':
                ActionChains(self.driver).key_up(Keys.SPACE).perform()
            elif s == 'ctrl':
                ActionChains(self.driver).key_up(Keys.CONTROL).perform()
            elif s == 'alt':
                ActionChains(self.driver).key_up(Keys.ALT).perform()
            elif s == 'shift':
                ActionChains(self.driver).key_up(Keys.SHIFT).perform()

    #        # endregion

    def getscrollheight(self):
        return scrollheight([self.driver])

    def scrollheight(self):
        return self.getscrollheight()

    def Height(self):
        return self.getscrollheight()

    def Width(self):
        return scrollwidth([self.driver])

    def fullscreen(self, path=None, scale=100, autodown=True, pause=1, clip=True, clipinterval=0.6,
                   cuttop=0, cutbottom=0, cutleft=0, cutright=0):
        """
        往上获取全屏。固定保存在basic_.png。
        @param path:路径名而不是文件名
        @param scale: 下滚距离
        @param autodown:是否下滚
        @param pause:不切片上滚时间间隔
        @param clip: 是否切片
        @param cuttop: 顶部固定浮动元素高度
        @param clipinterval: 切片时间间隔
        @return:
        """
        if path == None:
            path = collectionpath(f'其它/{self.title()}/basic.png')
        if not '/basic.png' in path:
            path += '/basic.png'
        path = standarlizedPath(path)
        createpath(path)
        delog(f'将把 {self.url()} 的全屏保存到  {path}')

        if autodown:
            self.down()

        if clip:
            self.down()
            # 为了防止图片懒加载跳屏，先上滚一次
            self.up()
            self.down()

            buf = 60
            clipsize = self.getscrollheight() - self.getscrolltop() - Int(cuttop) - Int(
                cutbottom) - buf
            clipcount = 0
            while True:
                self.scroll(
                    int(self.getscrollheight() - clipsize * clipcount - self.get_window_size()[
                        1] + 130))
                sleep(clipinterval)
                # 50是一般认为clipsize不会小于的值
                clippath = f'{parentpath(path)}/clipped/{extentionandname(path, exist=False)[0]}{clipcount}{extentionandname(path, exist=False)[1]}'
                createpath(clippath)
                self.driver.get_screenshot_as_file(clippath)
                delog(f'已保存部分截图到{clippath}')
                clipcount += 1
                if self.getscrolltop() == 0:
                    break
            combineimages(parentpath(clippath), outputname='basic.png', mode='vertical',
                          reverse=True,
                          filelist=[f"{parentpath(clippath)}/basic{i}.png" for i in
                                    range(clipcount)],
                          cuttop=cuttop, cutbottom=cutbottom, cutleft=cutleft, cutright=cutright)
            deletedirandfile(parentpath(clippath), silent=True)
        else:
            self.up(scale=scale, pause=pause)
            x, y = max(1080, scrollwidth([self.driver]) + 100), scrollheight([self.driver])
            self.set_window_size(x, y)
            self.driver.get_screenshot_as_file(path)

        if delog:
            look(path)

    # 避开不安全网页警告
    def skipsystemwarn(self):
        if '受到举报的不安全网站' in self.title():
            self.click('//*[@id="moreInformationDropdownLink"]')
            self.click('//*[@id="overrideLink"]')
        time.sleep(1)

    def save(self, *a, **b):
        config = jsondata('save')
        for i in config.data:
            if i in self.url():
                jsondata('savepage').setdata(config.data[i])
                break
        return self.savepage(*a, **b)

    @useState
    def savepage(self, path=None, video=False, minsize=(100, 100), t=3, titletail=None, scale=100,
                 direct=False,
                 clicktoextend=None, autodown=True, look=False, duplication=False, extrafunc=None,
                 pause=1,
                 overwrite=True, redownload=True, savevideo=False, clip=True,
                 cuttop=0, cutbottom=0, cutleft=0, cutright=0, clipinterval=2):
        """
        保存整个网页，包括截图，图片（大小可过滤），视频（可选），地址默认集锦
        @param path:收藏路径后缀
        @param video:
        @param minsize:
        @param t:
        @param titletail:
        @param scale:
        @param direct:
        @param clicktoextend: 可选点击展开
        @param autodown:
        @param look:
        @param duplication: 可选是覆盖还是新建已保存网页的副本
        @param extrafunc: 需要进行的额外操作
        @param pause: 滚动间隔
        @param overwrite: 是否覆盖
        @param redownload: 是否重新下载
        @param savevideo: 是否保存视频
        @param cuttop: 顶部固定浮动元素高度
        @param clipinterval: 切片时间间隔
        @return:
        """
        # region
        if minsize in [False, None]:
            minsize = (9999, 9999)

        if path == None:
            path = collectionpath(f'其它/{self.title()}/')
        else:
            path = collectionpath(path)
        createpath(path)

        #     附加页面标题到文件夹名
        if not direct:
            sleep(t)
            if not self.title() in path:
                path += self.title()
        if not titletail == None and ' ' + titletail in path:
            path = removetail(path, ' ' + titletail)
        if not titletail == None and titletail in path:
            path = removetail(path, titletail)
        # 没办法，这个空格在不在真的完全是一个玄学
        path += '/'

        # 判断是否新建网页副本
        if not isdir(path):
            createpath(path)
        elif not duplication:
            warn(f'已存在 {path}，将覆盖已保存的网页')
        else:
            # 遍历文件夹产生从0开始的新序号数字
            count = 0
            while isdir(path + str(count)):
                count += 1
            path = re.sub(r'\\+$', '', path)
            path = path + str(count) + '/'
            createpath(path)

        # 展开页面
        if not clicktoextend == None:
            if type(clicktoextend) in (str,):
                self.click(clicktoextend)
                if autodown:
                    self.down()
            else:
                clicktoextend([self])

        # 额外操作
        if not extrafunc == None:
            extrafunc([self])
        # 保存页面截图
        if self.type == 'edge' and not self.silent:
            self.ctrlshifts(path, t)
        else:
            self.fullscreen(f'{path}/basic.png', scale=scale, autodown=autodown, pause=pause,
                            clip=clip,
                            cutright=cutright, cutleft=cutleft, cuttop=cuttop, cutbottom=cutbottom,
                            clipinterval=clipinterval)

        # 保存页面图片
        self.savepics(path, 7, minsize=minsize)

        # 保存页面视频
        if savevideo:
            self.savevideos(path, 20)

        # 留下url记录
        f = txt(f'{path}/url.txt').add(self.url())

        log(f'页面已保存到{path}')
        if look or debug:
            try:
                Open(path + '/img')
            except:
                pass
        return path

    # 保存页面上的所有图片
    def savepics(self, path=None, t=5, minsize=(100, 100)):
        if self.url() == '':
            return
        res = []
        if path == None:
            path = collectionpath(f'/其它/{self.title()}/')
        res = self.elements('//pic', strict=False)+self.elements('//img', strict=False)
        count = 0
        for i in res:
            if i.size['height'] < minsize[1] or i.size['width'] < minsize[0]:
                continue
            count += 1
            url = i.get_attribute('src')
            if url == None:
                url = i.get_attribute('href')
            if url == None:
                Exit(self.url(), '获取图片地址失败')
            #     特殊地址处理
            url = gettail(url, 'blob:', strict=False)
            url = gettail(url, 'data:', strict=False)
            if '<svg' in url:
                continue
            delog(f'图片地址：{url}')

            # 有些图片懒加载
            # if 'data:' in url:
            #     continue

            fname = gettail(url, '/')

            bb = True
            # link里的图片后缀名后面还会有杂七杂八的东西
            for j in ['.jpeg', '.jpg', '.gif', '.png', '.bmp', '.webp']:
                if j in fname:
                    fname = removetail(fname, j) + j
                    bb = False
                    break
            if bb:
                fname += j
            fname = standarlizedFileName(fname)
            dpath = (f'{path}/img/_{count}_{fname}')
            log(f'saving {self.url()}的 {url} 到 {dpath}')
            delog(path)
            try:
                pagedownload(url, dpath, t=t)
            except Exception as e:
                warn(f'保存页面上的图片失败，\n{e}')
            p = pic(dpath)

    # 保存页面上的所有视频
    def savevideos(self, path, t=5, minsize=None):
        res = []
        res += self.elements('//video', strict=False)
        count = 0
        for i in res:
            count += 1
            url = i.get_attribute('src')
            if url == None:
                url = i.get_attribute('href')
            if url == None:
                Exit(self.url(), '获取图片地址失败')

            fname = gettail(url, '/')
            b = True
            for j in ['.mp4', 'mp3']:
                if j in fname:
                    fname = removetail(fname, j) + j
                    b = False
                    break
            if b:
                fname = fname + '.mp4'
            fname = standarlizedFileName(fname)
            dpath = f'{path}/video/<{count}>{fname}'
            log(f'saving {self.url()}的 {url} 到 {dpath}')
            pagedownload(url, dpath, t=t)

    # 快捷键保存截屏
    def ctrlshifts(self, path=None, t=3):
        """
        快捷键保存截屏
        @param path:
        @param t:
        @return:
        """
        if not self.type in 'edge':
            Exit('不是 edge 浏览器。不能用ctrl+shift+S 保存e')
        self.top()
        self.maxwindow()
        self.down(t=t)
        if path == None:
            path = collectionpath(f'/其它/{self.title()}')
        sleep(0.5)
        hotkey('ctrl', 'shift', 's')
        sleep(1)
        lis1 = listfile(userpath('Downloads'))
        click('browser/捕获整页.png')
        sleep(t)
        lis2 = listfile(userpath('Downloads'))
        for i in lis2:
            if not i in lis1:
                break
        move(i, f'{path}/basic.{gettail(i, ".")}')

    # 到上层显示窗口
    def top(self):
        if self.silent == True:
            Exit('静默模式下不显示到上层')
        hotkey('win', 'd')
        self.switchto()

    # 最大化窗口
    def maxwindow(self):
        self.driver.maximize_window()

    # 返回窗口列表
    def windows(self):
        return self.driver.window_handles

    # 新建窗口
    def newwindow(self, url=''):
        if not 'https://' in url:
            url = 'https://' + url
        self.driver.execute_script(f'window.open("{url}")')

    def refresh(self):
        self.driver.refresh()
        sleep(1)

    def url(self):
        return self.driver.current_url

    @listed
    def clickelement(self, *a):
        return Edge.click(a)

    def moveto(self, *a, strict=True, x=None, y=None, xoffset=None, yoffset=None):
        if len(a) > 1:
            # ActionChains(self.driver).move_to_element(to_element=Element(s)).click().perform()
            Exit(' 未实现')

        if not x == None:
            ActionChains(self.driver).move_by_offset(x, y).click().perform()

        s = a[0]
        if s == None:
            return
        if type(s) in [str]:
            return Edge.click(self, Edge.element(self, s, strict=strict))
        if type(s) in [selenium.webdriver.remote.webelement.WebElement]:
            try:
                ActionChains(self.driver).move_by_offset(x, y).perform()
            except Exception as e:
                warn(['moveto失败！', e])

    # 根据多个但只有一个有效的字符串匹配元素，返回第一个
    def element(self, *a, **b):
        ret = self.elements(*a, **b)
        if ret == []:
            return None
        else:
            return next((x for x in ret if x is not None), None)

    def Element(self, *a, **b):
        return self.element(*a, **b)

    @listed
    def elements(self, s, depth=9, silent=True, strict=True, root=None, refresh=False):
        """
        根据多个但只有一个有效的字符串匹配元素，返回第一组
        @param s:匹配字符串或是元素
        @param depth:
        @param silent:
        @param strict:True表示如果没找到，直接报错
        @param root:根元素。默认是self.driver
        @param refresh:找不到元素是否刷新页面
        @return:
        """
        if root == None:
            root = self.driver
        # 重写xpath规则
        s = s.replace('svg', '*[name()="svg"]')

        # 获取元素列表
        if not type(s) == list:
            ret = elements([root], s, depth=depth, silent=silent, strict=strict)
        else:
            for i in s:
                ret = elements([root], i, depth=depth, silent=silent)
                if not ret == []:
                    break
        if ret in [None, []]:
            if refresh:
                self.refresh()
                return self.elements(s, depth=depth, silent=silent, strict=strict, root=root,
                                     refresh=refresh)
            if strict:
                self.errorscr(ret)
        return ret

    def Elements(self, *a, **b):
        return self.elements(*a, **b)

    def scroll(self, a=-1, ite=None):
        if type(a) in [int, float]:
            if a == -1:
                scroll([(self.driver)], ite=None)
            else:
                setscrolltop([self.driver, a])
            return
        if type(a) in [str]:
            e = Edge.element(self, a)
            setscrolltop([self.driver, e.location('y')])
            return
        if type(a) in [selenium.webdriver.remote.webelement.WebElement]:
            setscrolltop([self.driver, a.location['y'] - a.size['height']])
            return

    def scrollto(self, a=None):
        return Edge.scroll(self, a)

    def down(self, ratio=1, t=0.3, ite=None):
        scroll([self.driver], silent=True, ratio=ratio, t=t, ite=ite)

    def getscrolltop(self):
        return getscrolltop([self.driver])

    def setscrolltop(self, h):
        if h < 0:
            warn(f'设置目标浏览器高度小于0')
            h = 0
        return setscrolltop([self.driver, h])

    def up(self, scale=250, pause=1):
        """
        向上滚动
        @param scale:上滚距离
        @param pause: 上滚间隔
        @return:
        """
        h = self.getscrolltop()
        while h > 10:
            if h > scale:
                h -= scale
                if h <= 0:
                    h = 0
                delog(h)
                sleep(pause)
            else:
                h = 0
            self.setscrolltop(h)

    # 如果不退出，可能报错 py sys path likely shutdown balabala...
    def quit(self):
        if not self.driver == None:
            self.driver.quit()

    # 新建标签页并跳转到标签页
    def open(self, url):
        url = 'https://' + url.strip('https://')
        self.driver.execute_script(f"window.open('{url}')")
        Edge.switchto(self, )

    def get(self, url, t=None):
        """

        @param url:
        @param t: 加载后的缓冲时间
        @return:
        """
        try:
            if not 'https://' in url and not 'http://' in url:
                url = 'https://' + url
            self.driver.get(url)
            if t:
                sleep(t)
            else:
                sleep(0.4)
        except Exception as e:
            if e in [selenium.common.exceptions.InvalidArgumentException]:
                Exit(f'请检查url = {url} 是否错误。')
            # if e in[selenium.common.exceptions.NoSuchWindowException]:
            #     pass
            raise(e)

    def switchto(self, n=-1):
        if type(n) in [int]:
            self.driver.switch_to.window(self.driver.window_handles[n])
        if type(n) in [str]:
            self.driver.switch_to.window(n)

    def set_window_size(self, *a, **b):
        log(f'扩展窗口至大小：{a, b}')
        self.driver.set_window_size(*a, **b)

    def elementshot(self, s, path=None, xoffset=None, yoffset=None, moveto=True, overwrite=True):
        """
        会改变窗口大小位置
        @param path:
        @param s: 元素，表达式
        @param xoffset:
        @param yoffset:
        @param moveto: 是否移动到元素位置
        @param overwrite:
        @return: 图片路径
        """
        currentheight = self.getscrolltop()
        if path == None:
            path = cachepath('elementshot.png')
        else:
            path = standarlizedPath(path)
            if isfile(path):
                if overwrite:
                    warn(f'{path}已存在。即将覆盖下载')
                else:
                    return True
            if not '.png' in path:
                path += '.png'

        if type(s) in [selenium.webdriver.remote.webelement.WebElement]:
            y = s.location['y']
            if not yoffset == None:
                y += yoffset
            if moveto:
                self.scroll(y)
            else:
                #     强制重新渲染
                self.scroll(currentheight)
            if 100 + s.size['height'] > self.get_window_size()[1]:
                self.set_window_size(self.get_window_size()[0],
                                     self.get_window_size()[1] + 100 + s.size['height'])
            file('wb', path, s.screenshot_as_png)
            return path

        if type(s) in [str]:
            return Edge.elementshot(self, path, Edge.element(self, s))

    # 遇到异常（元素为空时），终止并检查当前页面截图
    def errorscr(self, t=None):
        if t in [None, False, []]:
            print(nowstr())
            path = f'D:/Kaleidoscope/error/current.png'
            self.driver.get_screenshot_as_file(path)
            look(path)
            pyperclip.copy(self.driver.current_url)
            Exit(f'{self.url()}   {context(4)}  t={t}')

    # 查看当前页面
    def look(self, a=None):
        path = f'D:/Kaleidoscope/cache/current.png'
        if not a == None:
            self.elementshot(a, path)
            look(path)
            return
        deletedirandfile([path])
        self.driver.get_screenshot_as_file(path)
        look(path)

    # 关闭标签页并跳转到上一个标签页
    def close(self):
        self.driver.close()
        try:
            self.switchto(-1)
        except Exception as e:
            warn(e)

    def title(self):
        if self.url() == '':
            Exit('浏览器url为空')
        return title([self.driver])

    def quit(self):
        self.driver.quit()


class Chrome(Edge):
    def __init__(self, url=None, mine=None, silent=None, t=100, driver=None, mute=True):
        self.mine = mine
        #     记录当前在使用mine chrome的context
        # if mine == True:
        #     f = txt(projectpath('browser/ischromeusing.txt'))
        #     if not f.l == [] and not debug:
        #         Open(f.path)
        #
        #         Exit('Chrome 似乎已经在使用了')
        #     if debug:
        #         f.l = context(4)
        #     else:
        #         f.l=['似乎没有关闭上一个带用户缓存的浏览器页面。请确保程序不在用户使用浏览器的情况下使用用户缓存，并且带用户缓存的浏览器同一时间只能存在一个。']
        #     f.l.append(nowstr())
        #     f.save()
        if not driver == None:
            self.driver = driver[0]
            return
        else:
            self.driver = chrome(url=url, mine=mine, silent=silent, t=t, mute=mute)
        if not url == None:
            self.get(url)
        self.silent = silent
        self.type = 'chrome'

    def quit(self):
        super().quit()
        #         更改ischromeusing
        f = txt(projectpath('./browser/ischromeusing.txt'))
        if self.mine:
            if not f.l == []:
                f.l = []
        f.save()

    def maximize(self):
        self.driver.maximize_window()


def edge(url='', silent=None, mine=False, mute=True):
    options = webdriver.EdgeOptions()
    # options.page_load_strategy = 'none'
    if not silent == None:
        options.add_argument('headless')
    if mute:
        options.add_argument('--mute-audio')
    if mine:
        options.add_argument(
            '--user-data-dir=C:\\Users\\17371\\AppData\\Local\\Microsoft\\Edge\\User Data')
        options.add_argument('headless')
    try:
        driver = webdriver.Edge(options=options)
    except selenium.common.exceptions.SessionNotCreatedException:
        warn('貌似msedgedriver.exe版本过低。已经自动复制网址链接。请打开浏览器进行下载。')
        pyperclip.copy('https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/')
        delog('点击 edge://version/ 以查看浏览器版本。')
        sys.exit(-1)
    driver.set_page_load_timeout(7)

    if not url == '':
        if not 'https://' in url and not 'http://' in url:
            url = 'https://' + url
        driver.get(url)
    return driver


def click(x=10, y=10, button='left', silent=True, interval=0.2, confidence=1, limit=0, gap=0.05,
          grayscale=True, xoffset=0, yoffset=0, strict=False,moveto=True):
    """
    点击屏幕或者识别屏幕内容
    @param x:x为坐标，或者图片路径
    @param y:
    @param button: 左键还是右键
    @param silent:
    @param interval:点击完后的等待时间
    @param confidence: 图片识别精确度
    @param limit:图片识别精确度下限
    @param gap: 图片识别精确度下降间隔
    @param grayscale: 是否使用灰度识别图片
    @param xoffset: 图片识别结果的偏移量
    @param yoffset:
    @param strict: 是否严格模式，严格模式下，如果定位不存在，则会返回
    @param moveto:是否移动到
    @return:是否成功
    """

    # 点击图片
    if type(x) in [str]:
        if not '.png' in x:
            x += '.png'
        path = projectpath(x)
        if isfile(path):
            while confidence > limit:
                pos = pyautogui.locateOnScreen(path, confidence=confidence, grayscale=grayscale)
                confidence -= gap
                if pos == None:
                    continue
                else:
                    p = pyautogui.center(pos)
                    click(p.x + xoffset, p.y + yoffset)
                    if not silent:
                        log(p.x + xoffset, p.y + yoffset)
                    return True
        #     没找到
        if strict:
            Open(path)
            Exit(path)
        else:
            return False

    # 点击坐标
    try:
        # 默认xy坐标是在windows UI缩放比例为125%下的，在screenscale.txt中修改当前的缩放比例
        defaultmode = 'center'
        defaultuiscale = 125
        defaultxscale = 1920
        defaultyscale = 1080
        global uiscale, xsize, ysize
        X, Y = x - defaultxscale / 2, y - defaultyscale / 2
        X, Y = int(X / defaultxscale * xsize / defaultuiscale * uiscale), int(
            Y / defaultyscale * ysize / defaultuiscale * uiscale)
        x, y = X + xsize / 2, Y + ysize / 2
        if x == 0:
            x = 1
        if y == 0:
            y = 1
        if moveto:
            pyautogui.click(x, y, button=button)
        sleep(interval)
        if not silent:
            print(f'{x}   {y}')
    except Exception as e:
        if type(e) in [pyautogui.FailSafeException]:
            Exit(f'可能是选取点击的坐标过于极端。 x:{x}    y:{y}')
        warn(e)
        sys.exit(-1)


# 右击屏幕
def rclick(x, y):
    click(x, y, button='cutright')


# 点击元素
def clickelement(l):
    if len(l) > 2:
        try:
            Element(l).click()
            return
        except:
            try:
                ActionChains(l[0]).move_to_element(to_element=Element(l)).click().perform()
                return
            except Exception as e:
                warn(['clickelement error！', e])
    else:
        page = l[0]
        element = l[1]
        try:
            element.click()
            return
        except:
            try:
                ActionChains(page).move_to_element(to_element=element).clickelement().perform()
                return
            except Exception as e:
                warn(['clickelement error!', e])

    sleep(1)


def MyPress(l):
    page = l[0]
    s = l[1]
    if s == 'down':
        k = Keys.DOWN
    ActionChains(page).key_down(k).key_up(k).perform()


def title(l):
    page = l[0]
    element = Element([page], s='/html/head/title')
    if element == None:
        return ''
    return standarlizedFileName(element.get_attribute('text'))


def setscrolltop(l):
    (page, x) = l
    page.execute_script(f'document.documentElement.scrollTop={x}')


@consume
def pagedownload(url, path, t=15, silent=True, depth=0, auto=None, redownload=None,
                 overwrite=False):
    """
    @param url:
    @param path: 必须指定文件名，建议指定后缀名。文件名自动重命名"~"为"_"
    @param t:下载和下载后浏览器自动安全检查的时间
    @param silent:
    @param depth:
    @param auto:是否是打开页面即自动下载
    @param overwrite: 覆盖下载或是覆盖移动
    @param redownload: 一定会重新下载。
    @return:True 下载了并且下载成功；False 下载了但是下载失败；字符串 返回检测到的以前的错误命名
    """

    path = standarlizedPath(path)
    # if not '.'in path:
    #     path+=
    if not redownload:
        #     已下载
        if exists(path) and not size(path) == 0:
            if not overwrite:
                log(f'{path} 已存在，将不下载')
                return True
            else:
                move(path, cachepath(f'trashbin/{now()}'))

    def recursive():
        sleep(t)
        page.quit()
        sleep(1)
        delog(f'正在检测是否下载到了路径 {root}')
        for ii in listfile(root):
            if name in ii and '.crdownload' in ii:
                deletedirandfile(ii)
                warn(f'{t}s后下载失败。没有缓存文件存留（自动删除） 请手动尝试 {url}')
                return pagedownload(url, path, t=t + t, depth=depth + 1, silent=silent, auto=auto,
                                    redownload=redownload, overwrite=overwrite)
            if name in ii:
                if redownload:
                    move(ii, path, autorename=redownload, overwrite=overwrite)
                return True
        warn(f'{t}s后下载失败。没有检测到缓存文件  请手动尝试 {url}')
        return False

    # 递归停止条件
    # region
    if depth > 5:
        warn('最终下载失败。没有缓存文件存留（自动删除） 请手动尝试 {url}')
        return False
    # endregion

    originalpath = path
    createpath(path)
    # region
    path = standarlizedPath(path, strict=True)
    path = path.replace('~', '_')
    # if os.path.exists(path):
    #     # 存在以前的浏览器自动重命名'~'为'_'的文件
    #     if not originalpath == path:
    #         rename(path, originalpath)
    #         return originalpath

    if redownload:
        root = standarlizedPath(cachepath('pagedownload/'), strict=True)
    else:
        root = (path[:path.rfind('\\')])
    name = path[path.rfind('\\') + 1:]
    options = webdriver.ChromeOptions()
    # 设置下载路径
    prefs = {'download.default_directory': f'{root}'}
    options.add_experimental_option('prefs', prefs)
    options.add_argument('--mute')
    if silent == True:
        options.add_argument('--headless=new')
    page = webdriver.Chrome(chrome_options=options)
    # endregion

    # 打开页面
    try:
        page.get(url)
        # 如果服务器直接403
        # region
        if tellstringsame(page.title, '403 forbidden'):
            warn(f'这个url已经被服务器关闭  403  ：{url}')
            return False
        # endregion

    except Exception as e:
        # 仍然可以强制下载的报错
        if type(e) in [ZeroDivisionError, ]:
            warn(e)
        elif type(e) in [selenium.common.exceptions.WebDriverException]:
            # 需要重启pagedownload的下载报错
            warn(e)
            page.quit()
            return pagedownload(url, path, t=t, depth=depth + 1, silent=silent, auto=auto,
                                redownload=redownload, overwrite=overwrite)
        else:
            warn(e)
            warn(type(e))
            sys.exit(-1)

    i = 0
    # 如果这个链接打开就能自动下载
    # region
    if not auto == None:
        return recursive()
    # endregion

    # region
    while i < 10:
        # 什么？？？竟然要尝试10次，哈哈哈真是笑死我了
        try:
            page.execute_script(f"const a1=document.createElement('a');\
            a1.href='{url}';\
            a1.download='{name}';\
            a1.click();")
            # root必须存在，否则会跳出为另存为
            delog(f'pagedownload 正在下载 {url} 到 {root}')
            break
        except Exception as e:
            warn('下载重试中...')
            warn(e)
            warn(type(e))
            i += 1
    # endregion

    return recursive()


def scrshot(l):
    (element, path) = l
    path = standarlizedPath(path)
    if isfile(path):
        warn(f'{path}已存在。即将覆盖下载')
    path = path.strip('.png') + '.png'
    file('wb', path, element.screenshot_as_png)


# endregion


# 初始化2
# region
user = getsettings('userName')
if setRootPath(d='d') == 'HerMAJESTY':
    Debug()
consoletxt = Json('D:/Kaleidoscope/console.txt')
consolerunning = txt(projectpath('ConsoleShow.txt'))
try:
    uiscale = int(txt(projectpath('ScreenScale.txt')).l[0])
    xsize = int(txt(projectpath('ScreenScale.txt')).l[1])
    ysize = int(txt(projectpath('ScreenScale.txt')).l[2])
except:
    warn('ScreenScale未配置，使用默认参数。')
    uiscale = 125
    xsize = 1920
    ysize = 1080


def RuntimeRoot():
    ret = standarlizedPath(__file__)
    ret = ret[:ret.rfind('/')] + '/'
    return ret


tip('MyUtils already loaded')
# endregion
