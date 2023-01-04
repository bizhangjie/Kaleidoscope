from ProgressBar import *

# 定义一个返回函数的函数
# 参数cost为任务耗时（秒）、epoch为迭代次数、name为任务名、_sub_task为子任务
def task(cost=0.5, epoch=3, name="", _sub_task=None):
    def _sub():
        bar = ProgressBar(max_value=epoch, name=name)
        # 调用start方法进行进度条的初始化
        bar.start()
        for _ in range(epoch):
            # 利用time.sleep方法模拟任务耗时
            # 自己要计时程序位置
            time.sleep(cost)

            # 如果有子任务的话就执行子任务
            if _sub_task is not None:
                _sub_task()
            # 调用update方法更新进度条
            bar.update()
    return _sub
# 定义三个任务Task1、Task2、Task3
# 其中Task2、Task3分别为Task1、Task2的子任务
task(name="Task1", _sub_task=task(
    name="Task2", _sub_task=task(
        name="Task3")))()