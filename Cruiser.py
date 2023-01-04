import multiprocessing
import time

import A20min
import Apushgithub
import MyUtils
import RAM

workgroup1=False
workgroup2=False
workgroup3=False
workgroup4=False
# 在注意各优先级不冲突的同时，进行巡航
if __name__ == '__main__':
    MyUtils.Run()
    pool1 = multiprocessing.Pool(5)


    pool1.apply_async(A20min.main)
    pool1.apply_async(Apushgithub.main)
    pool1.apply_async(RAM.init)

    workgroup2 = False
    if workgroup2 == True:
        import DouyinDetect
        import DouyinDownload
        import provisional

        for i in range(1):
            pool1.apply_async(provisional.main, ())
            time.sleep(3)
        for i in range(2):
            pool1.apply_async(DouyinDetect.main, ())
            time.sleep(3)
        for i in range(3):
            pool1.apply_async(DouyinDownload.main, ())
            time.sleep(3)

    time.sleep(5)
    pool1.close()
    pool1.join()
    MyUtils.warn('Cruiser Exiting ....')
    time.sleep(999)
