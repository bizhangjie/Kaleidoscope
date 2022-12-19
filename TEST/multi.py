import multiprocessing
import time

import MyUtils
import Test1
import Test2
import Apushgithub

def func(a, b=1, c=1):
    while True:
        print(a, b, c)
        time.sleep(0.9)


def main():
    pool1 = multiprocessing.Pool(5)
    for i in range(1):
        pool1.apply_async(Apushgithub.main,())
    for i in range(3):
        pool1.apply_async(Test2.main,())

    pool1.close()
    pool1.join()
    print('parent sleeping...')
    MyUtils.sleep(10)

# close,joinpool和函数声明位置必须与上面保持一致,Pool的声明至少要在一个函数中而不是外部。
if __name__ == '__main__':
    main()
    print('parent end')
