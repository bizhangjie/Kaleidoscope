import MyUtils


if __name__ == '__main__':
    l1=[1,2,2]
    l2=[3,4]
    l3=[5,6]
    while True:
        lis=MyUtils.extend(l1,set=True)
        break
    print(lis)
    print(MyUtils.extend(l1,l2,l3))
