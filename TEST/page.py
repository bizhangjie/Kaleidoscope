import MyUtils
url='www.bilibili.com'

if __name__ == '__main__':
    page = MyUtils.Chrome(url, silent=False,mine=False, mute=True)
    MyUtils.sleep(10)