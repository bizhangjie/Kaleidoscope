import MyUtils

if __name__ == '__main__':
    # url = 'https://pc.yiyouliao.com/msn/article.html?recId=8d400f7d290240cda7bf5c7849c0ac67_s&infoId=II00YG88X54UAMO'
    url='https://pc.yiyouliao.com/msn/article.html?recId=667e103c535b423e8e0c7d96841804fb_s&infoId=II00AMQR1FKBY0J'
    # page=MyUtils.Chrome(url,silent=True,mine=True)
    # page = MyUtils.Chrome(url, silent=True, mine=False)
    page = MyUtils.Edge(url, silent=True)
    # page.set_window_size(1200,3000)
    page.save(minsize=(200, 200), scale=1200, autodown=1, look=True)
    page.quit()
