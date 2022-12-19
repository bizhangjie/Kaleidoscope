import time

import A20min
import Anote
import MyUtils
import DouyinDetect
import DouyinDownload
import multiprocessing
import RAM

# 在注意各优先级不冲突的同时，进行巡航
if __name__ == '__main__':
    MyUtils.Run()
    pool1 = multiprocessing.Pool(5)
    pool1.apply_async(A20min.main)
    pool1.apply_async(RAM.init)

    for i in range(2):
        pool1.apply_async(DouyinDetect.main,())
        time.sleep(3)
    for i in range(3):
        pool1.apply_async(DouyinDownload.main,())
        time.sleep(3)
    time.sleep(5)
    pool1.close()
    pool1.join()
    MyUtils.warn('Cruiser Exiting ....')
    time.sleep(999)