import MyUtils


def main():
    for i in MyUtils.listdir('e:/抖音'):

        MyUtils.delete_similar(i,new=True)

if __name__ == '__main__':
    main()
