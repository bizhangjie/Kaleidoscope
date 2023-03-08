import MyUtils

def main():
    page = MyUtils.Chrome('https://www.zhihu.com', silent=False,mine=True)

if __name__ == '__main__':
    main()
