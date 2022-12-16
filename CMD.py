import os

import MyUtils
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

MyUtils.CMD.listall()
print(MyUtils.CMD.front(75),MyUtils.CMD.background(238),MyUtils.CMD.font(1),'这是一段日志文字\nThis is a delog.')
print(MyUtils.CMD.front(148),MyUtils.CMD.background(238),MyUtils.CMD.font(1),'这是一段日志文字\nThis is a log.')
print(MyUtils.CMD.front(166),MyUtils.CMD.background(238),MyUtils.CMD.font(1),'这是一段日志文字\nThis is a warn.')
print(MyUtils.CMD.front(248),MyUtils.CMD.background(238),MyUtils.CMD.font(9),'这是一段日志文字\nThis is a tip.')
print(MyUtils.CMD.front(241),MyUtils.CMD.background(238),MyUtils.CMD.font(1),'这是一段日志文字\nThis is a tip.')
print(MyUtils.CMD.front(242),MyUtils.CMD.background(238),MyUtils.CMD.font(1),'这是一段日志文字\nThis is a tip.')
print(MyUtils.CMD.front(243),MyUtils.CMD.background(238),MyUtils.CMD.font(1),'这是一段日志文字\nThis is a tip.')
print(MyUtils.CMD.front(240),MyUtils.CMD.background(238),MyUtils.CMD.font(1),'这是一段日志文字\nThis is a tip.')
# print(f'\x1b[7;30m')
# print(f'\x1b[0m')
# print(f'\033[7;31m')
# print(f'\x1b[0m')
# print(f'\033[48;5;30m')
# print(f'\x1b[0m')