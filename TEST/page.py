import MyUtils

def main():
    page = MyUtils.Chrome('https://www.zhihu.com/hot', silent=False,mine=True)

if __name__ == '__main__':
    main()
