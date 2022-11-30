import MyUtils


def fun():
    pass


def main():
    fun()


if __name__ == '__main__':
    # print(MyUtils.desktoppath('sample'))
    # print(MyUtils.userpath('sample'))
    # print(MyUtils.projectpath('sample'))
    MyUtils.rmempty(MyUtils.desktoppath('sample/'))
