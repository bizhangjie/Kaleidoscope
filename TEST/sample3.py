import random
from win32file import CreateFile, SetFileTime, GetFileTime, CloseHandle
from win32file import GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING
from pywintypes import Time  # 可以忽视这个 Time 报错（运行程序还是没问题的）
import time
import os


def modifyFile(filePath, createTime, modifyTime, accessTime, offset):
    """
    用来修改任意文件的相关时间属性，时间格式：YYYY-MM-DD HH:MM:SS 例如：2019-02-02 00:01:02
    :param filePath: 文件路径名
    :param createTime: 创建时间
    :param modifyTime: 修改时间
    :param accessTime: 访问时间
    :param offset: 时间偏移的秒数,tuple格式，顺序和参数时间对应
    """
    try:
        format = "%Y-%m-%d %H:%M:%S"  # 时间格式
        cTime_t = OffsetAndStruct(createTime, format, offset[0])
        mTime_t = OffsetAndStruct(modifyTime, format, offset[1])
        aTime_t = OffsetAndStruct(accessTime, format, offset[2])
        fh = CreateFile(filePath, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)
        createTimes, accessTimes, modifyTimes = GetFileTime(fh)
        createTimes = Time(time.mktime(cTime_t))
        accessTimes = Time(time.mktime(aTime_t))
        modifyTimes = Time(time.mktime(mTime_t))
        SetFileTime(fh, createTimes, accessTimes, modifyTimes)
        CloseHandle(fh)
        return 0
    except:
        return 1


def OffsetAndStruct(times, format, offset):
    return time.localtime(time.mktime(time.strptime(times, format)) + offset)


def files(file, cTime, mTime, aTime, offset):
    f = os.listdir(file)
    for i in f:
        fName = os.path.join(file, i)
        # 调用函数修改文件创建时间，并判断是否修改成功
        r = modifyFile(fName, cTime, mTime, aTime, offset)
        if r == 0:
            print('修改完成')
        elif r == 1:
            print('修改失败')


def run():
    # 需要自己配置
    cTime = f"2022-9-21 21:{random.randint(10, 20)}:{random.randint(10, 40)}"  # 创建时间
    mTime = f"2022-9-22 00:{random.randint(15, 30)}:{random.randint(10, 40)}"  # 修改时间
    aTime = f"2022-7-22 00:{random.randint(18, 35)}:{random.randint(10, 40)}"  # 访问时间
    offset = (0, 1, 2)  # 偏移的秒数（不知道干啥的）
    fName = r'D:\Kaleidoscope\TEST\res' # 使用绝对路径
    files(fName, cTime, mTime, aTime, offset) # 调用修改文件相关操作
    print('----->修改文件时间结束')


if __name__ == '__main__':
    run()

