import MyUtils


def fun():
    pass

@MyUtils.multisingleargs
def main(a):
    print(a)


if __name__ == '__main__':
    main(1,2,3)
