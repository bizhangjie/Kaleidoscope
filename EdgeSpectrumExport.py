import time

import MyUtils


def fun():
    pass


def main():
    fun()


if __name__ == '__main__':
    # 对Edge浏览器导出的Spectrum收藏夹（第二个）进行遍历网站收集
    page=MyUtils.Edge('file:///D:/Kaleidoscope/%E6%94%B6%E8%97%8F%E5%A4%B9%E5%AF%BC%E5%87%BA/favorites_2022_11_28.html')
    lis=page.elements('/html/body/dl/dt[1]/dl/dt[2]//a/@href')
    f=MyUtils.txt(MyUtils.projectpath('browser/Spectrum.txt'))
