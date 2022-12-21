import MyUtils

if __name__ == '__main__':
    src=MyUtils.listdir(MyUtils.desktoppath('sample/1'))[0]
    tar=MyUtils.listdir(MyUtils.desktoppath('sample/2'))[0]
    MyUtils.move(src,tar)