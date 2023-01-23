import multiprocessing
import time

import A20min
import Apushgithub
import MyUtils
import RAM

# 常规组
workgroup0 = 3
# 临时组
workgroup1 = 0
# 抖音组
workgroup2 = 5
# bili组
workgroup3 = 0
#
workgroup4 = 0
poolnum = 3 + workgroup0 + workgroup1 + workgroup2 + workgroup3 + workgroup4

# 在注意各优先级不冲突的同时，进行巡航
if __name__ == '__main__':
    MyUtils.Run()

    pool1 = multiprocessing.Pool(poolnum)

    if workgroup0:
        pool1.apply_async(A20min.main)
        pool1.apply_async(Apushgithub.main)
        pool1.apply_async(RAM.init)

    if workgroup2:
        import DouyinDetect
        import DouyinDownload

        for i in range(int(workgroup2*0.4)):
            pool1.apply_async(DouyinDetect.main, ())
            time.sleep(3)
        for i in range(int(workgroup2*0.6)):
            pool1.apply_async(DouyinDownload.main, ())
            time.sleep(3)

    time.sleep(5)
    pool1.close()
    pool1.join()
    MyUtils.warn('Cruiser Exiting ....')
    time.sleep(999)
