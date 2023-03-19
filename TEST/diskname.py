import MyUtils


def main():
    print(MyUtils.diskpath)
    print(MyUtils.standarlizedPath('./'))
    MyUtils.setrootpath('d')
    print(MyUtils.diskpath)
    print(MyUtils.standarlizedPath('./'))


if __name__ == '__main__':
    main()
