import MyUtils

if __name__ == '__main__':
    tar1=MyUtils.desktoppath('工作台/视频转音频')
    src=(MyUtils.desktoppath('工作台/视频库'))
    MyUtils.mp4tomp3(src,tar1)