import A20min
import Anote
import MyUtils
import DouyinDetect
import DouyinDownload
import multiprocessing
import RAM

# 在注意各优先级不冲突的同时，进行巡航
if __name__ == '__main__':
    pool1 = multiprocessing.Pool(9)
    pool1.apply_async(RAM.init)
    pool1.apply_async(A20min.main)
    pool1.apply_async(Anote.main)



    # for i in range(2):
    #     pool1.apply_async(DouyinDetect.__main__,())
    # for i in range(3):
    #     pool1.apply_async(DouyinDownload.__main__,())
    pool1.close()
    pool1.join()