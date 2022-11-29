import time

import MyUtils


def fun():
    pass

def main():
    fun()


if __name__ == '__main__':
    main()
    page=MyUtils.Chrome(mine=True)
    time.sleep(1)
    time.sleep(1)
    page.quit()
