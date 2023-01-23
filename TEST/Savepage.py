import MyUtils


def provisional(page):
    page = page[0]
    page.scroll(43100)

if __name__ == '__main__':
    # url='https://pc.yiyouliao.com/msn/article.html?recId=667e103c535b423e8e0c7d96841804fb_s&infoId=II00AMQR1FKBY0J'
    # for url in ['https://m.thepaper.cn/baijiahao_6678131']:
    for url in ['https://pc.yiyouliao.com/msn/article.html?recId=8d400f7d290240cda7bf5c7849c0ac67_s&infoId=II00YG88X54UAMO']:
        page = MyUtils.Edge(url, silent=True)
        # 掘金
        # titletail=' - 掘金'
        # path='./掘金'
        # page.save(path=path,minsize=(200, 200), scale=300, autodown=True, look=True,titletail=titletail)

        # page.save(minsize=(200, 200), scale=300, autodown=True, look=True, t=2, )
        page.save(minsize=(500,500), scale=1000, autodown=False, look=True, t=2, extrafunc=provisional,pause=0.5)
        page.quit()

