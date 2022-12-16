import MyUtils

if __name__ == '__main__':
    tar1=(MyUtils.userpath('/Videos/VID_20221130_182855.mp4'))
    src=(MyUtils.desktoppath('工作台/视频库'))
    MyUtils.mp4tomp3(tar1)