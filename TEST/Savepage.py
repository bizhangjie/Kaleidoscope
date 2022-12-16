import MyUtils

if __name__ == '__main__':
    url=''
    # url='https://blog.csdn.net/xu_ya_fei/article/details/40214097'
    # url = 'https://pc.yiyouliao.com/msn/article.html?recId=8d400f7d290240cda7bf5c7849c0ac67_s&infoId=II00YG88X54UAMO'
    page=MyUtils.Chrome(url,silent=True,mine=True)
    # page = MyUtils.Chrome(url, silent=True, mine=False)
    # page = MyUtils.Edge(url, silent=True)
    # page.set_window_size(1200,3000)
    page.save(minsize=(200, 200), scale=400, autodown=1, look=True)
    page.quit()
