import MyUtils


def main():
    global p
    # p=MyUtils.SortedName(['basic.png','basic_1.png'])
    MyUtils.out(MyUtils.SortedName(['basic0.png','basic11.png','basic2.png','basic3.png','basic4.png','basic5.png','basic6.png','basic7.png','basic8.png','basic9.png',
        'content.png','content1.png']))

if __name__ == '__main__':
    global p
    main()
    print(p)