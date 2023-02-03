import MyUtils


def main():
    print(MyUtils.diskname)
    print(MyUtils.standarlizedPath('./'))
    MyUtils.setrootpath('d')
    print(MyUtils.diskname)
    print(MyUtils.standarlizedPath('./'))


if __name__ == '__main__':
    main()
