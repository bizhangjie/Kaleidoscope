import MyUtils


def main():
    t=MyUtils.excel(MyUtils.cachepath('testexcel'))
    print(t.title)

if __name__ == '__main__':
    main()
