import MyUtils


def main():
    t=MyUtils.excel(MyUtils.cachepath('testexcel'),title=['第一列','第二列','第三列'])
    t.add([MyUtils.nowstr(),None,len(t)])

if __name__ == '__main__':
    main()
