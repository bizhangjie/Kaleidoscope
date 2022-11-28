import time

import MyUtils


def fun():
    pass


def main():
    fun()


if __name__ == '__main__':
    page=MyUtils.Chrome('https://www.cc98.org/topic/5471822',mine=True,silent=True)
    time.sleep(7)
    page.fullscreen()
    page.quit()