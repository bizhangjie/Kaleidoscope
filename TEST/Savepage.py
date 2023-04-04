import MyUtils
extrafunc=None
scale=1000
minisize=(300,300)
look=True
t=2
pause=0.5
path=None
def provisional(page):
    page = page[0]
    page.scroll(800)
    page.click('//*[contains(text(),"阅读剩余")]')
    # page.scroll(26000)
    pass
# https://pc.yiyouliao.com/msn/article.html?recId=667e103c535b423e8e0c7d96841804fb_s&infoId=II00AMQR1FKBY0J
if __name__ == '__main__':
    while True:
        url=MyUtils.txt(MyUtils.cachepath('savepage/savepage.txt')).l[0]
        # url=r'https://blog.google/technology/ai/bard-google-ai-search-updates'
        while url==None:
            url=MyUtils.txt(MyUtils.cachepath('savepage/savepage.txt')).l[0]
            MyUtils.sleep(3)
        MyUtils.log(f'准备保存网页：  {url}')
        page = MyUtils.Chrome(url, silent=False,mine=False)
        page.save(minsize=minisize, scale=scale, look=look, t=t,path=path,
                  extrafunc=extrafunc,pause=pause,
                  )
        # page.save(minsize=minisize, scale=scale, look=look, t=t,path=path,
        #           extrafunc=extrafunc,pause=pause,
        #           cuttop=85,cutbottom=95
        #           )
        page.quit()
        MyUtils.txt(MyUtils.cachepath('savepage/savepage.txt')).delete(url)
