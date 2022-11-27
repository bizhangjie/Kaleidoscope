import MyUtils


def fun(a):
    print(a)

@MyUtils.newname
def main(fun,a):
    pass


if __name__ == '__main__':
    main('1')
