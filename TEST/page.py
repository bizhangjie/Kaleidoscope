import time

import MyUtils


def fun(page):
    page = MyUtils.Chrome('https://www.baidu.com', silent=False)
    MyUtils.sleep(10)


def main():
    page = MyUtils.Chrome('https://www.baidu.com', silent=False)
    fun(page)


if __name__ == '__main__':
    main()
