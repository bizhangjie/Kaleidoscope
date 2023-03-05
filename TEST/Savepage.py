import MyUtils


def provisional(page):
    page = page[0]
    # page.scroll(800)
    page.click('/html/body/div[2]/div/div[1]/button/i')
    # page.scroll(26000)

# https://pc.yiyouliao.com/msn/article.html?recId=667e103c535b423e8e0c7d96841804fb_s&infoId=II00AMQR1FKBY0J
if __name__ == '__main__':
    while True:
        url=None
        while url==None:
            url=MyUtils.txt(MyUtils.cachepath('savepage/savepage.txt')).l[0]
            MyUtils.sleep(20)
        MyUtils.log(f'准备保存网页：\t {url}')
    # for url in ['']:
        page = MyUtils.Edge(url, silent=True)
        page.save(minsize=(300,300), scale=1000, autodown=False, look=True, t=2, extrafunc=None,pause=0.5)
        page.quit()
        MyUtils.txt(MyUtils.cachepath('savepage/savepage.txt')).delete(url)
