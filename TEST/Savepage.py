import time

import MyUtils


def fun():
    pass


def main():
    fun()


if __name__ == '__main__':

    page=MyUtils.Chrome(url='www.baidu.com',mine=True,silent=True)
    for i in MyUtils.txt(MyUtils.desktop('0.txt')).l:
        page.get(i)
        time.sleep(7)
        page.save()
    page.quit()