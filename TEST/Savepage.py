import MyUtils


def provisional(page):
    page = page[0]
    page.scroll(800)
    page.click('//*[@id="artical"]/div[4]/a')
    page.scroll(26000)

if __name__ == '__main__':
    # url='https://pc.yiyouliao.com/msn/article.html?recId=667e103c535b423e8e0c7d96841804fb_s&infoId=II00AMQR1FKBY0J'
    # for url in ['https://m.thepaper.cn/baijiahao_6678131']:
    # for url in ['http://www.studyofnet.com/588830253.html']:
    for url in ['https://csdnnews.blog.csdn.net/article/details/128668479?spm=1000.2115.3001.5927']:
        page = MyUtils.Edge(url, silent=True)

        # page.save(minsize=(200, 200), scale=300, autodown=True, look=True, t=2, )
        page.save(minsize=(500,500), scale=1000, autodown=False, look=True, t=2, extrafunc=None,pause=0.5)
        page.quit()

