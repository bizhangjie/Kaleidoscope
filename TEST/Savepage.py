import MyUtils


def provisional(page):
    page = page[0]
    # page.scroll(800)
    page.click('/html/body/div[2]/div/div[1]/button/i')
    # page.scroll(26000)

if __name__ == '__main__':
    # url='https://pc.yiyouliao.com/msn/article.html?recId=667e103c535b423e8e0c7d96841804fb_s&infoId=II00AMQR1FKBY0J'
    for url in ['https://mp.weixin.qq.com/s?__biz=MjM5ODE5NzY0Nw==&mid=2651042284&idx=1&sn=9a66a7e44343b46d06352b420bc479f6&chksm=bd39710c8a4ef81aa6c69549167aa3b3019089d02c38ad05bd6674bdfae9968f9f3f289b13d4&scene=27']:
    # for url in ['http://www.studyofnet.com/588830253.html']:
        page = MyUtils.Edge(url, silent=True)

        # page.save(minsize=(200, 200), scale=300, autodown=True, look=True, t=2, )
        # page.save(minsize=(500,500), scale=1000, autodown=False, look=True, t=2, extrafunc=provisional,pause=0.5)
        page.save(minsize=(300,300), scale=1000, autodown=False, look=True, t=2, extrafunc=None,pause=0.5)
        page.quit()

