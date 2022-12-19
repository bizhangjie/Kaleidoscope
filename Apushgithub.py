import time

import MyUtils


def fun():
    pass


def main():
    fun()


if __name__ == '__main__':
    # 持续推送到github
    while True:
        f=MyUtils.txt(MyUtils.projectpath('txt.txt'))
        f.add(MyUtils.nowstr())
        MyUtils.CMD(f'cd d:;cd {MyUtils.projectpath()};git add .',silent=True)
        MyUtils.CMD(f'cd d:;cd {MyUtils.projectpath()};git push',silent=True)
        MyUtils.log('已推送。')
        time.sleep(60*5)

