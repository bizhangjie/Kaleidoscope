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
print(f"{bcolors.BOLD} this this {bcolors.FAIL}")

# MyUtils.CMD(f'cd d:;cd {MyUtils.projectpath()};git push',silent=True)






# \033是ESC的转义ASCII码  '\033['叫做CSI(Control Sequence Introducer)，相当于控制头。
CSI    = '\033['
# 35前景色;45背景色;    5  256色模式;
COLOR256_FORE = '38;5;'
COLOR256_BACK = '48;5;'
def color256_reset_all():
    return CSI + '0m'
def color256_bold():
    return CSI + '1m';
def color256_color(n):
    return CSI + COLOR256_FORE + str(n) + 'm'
def color256_bgcolor(n):
    return CSI + COLOR256_BACK + str(n) + 'm'
def color256_reset_fore():
    return CSI + '39m'
def color256_reset_back():
    return CSI + '49m'


print(color256_reset_all(), end='')
print(color256_reset_all())
print(color256_bold() + "Important")
print(color256_reset_all())
print()

# for TEST in range(0,256):
#     print(f'{TEST}'+color256_bgcolor(TEST)+'\t'*10)

def log(s):
    print(color256_bgcolor(5)+s)
log('这是一段内容')