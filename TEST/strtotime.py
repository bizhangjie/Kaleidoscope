import MyUtils
import time
import multiprocessing

from selenium.webdriver.common.by import By
from retrying import retry


@retry(retry_on_exception=MyUtils.retry)
def fun():
    ()


def main():
    fun()


if __name__ == '__main__':
    main()
    print(MyUtils.Time('星期一'))
    print(MyUtils.Time('星期三'))
    print(MyUtils.Time('星期日'))
    print(MyUtils.strtotime('2022-11-06 21:52:39.267631'))
    print(MyUtils.strtotime('2022-11-06'))
    print(MyUtils.strtotime('21:52:39.267631'))
    print(MyUtils.strtotime('2022-11-06 21:52'))
    print(MyUtils.strtotime('11-06 21:52'))
    print(MyUtils.Now().counttime(MyUtils.strtotime('2022-11-06 21:52:39.267631')))