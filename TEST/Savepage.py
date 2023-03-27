import MyUtils


cuttop, cutbottom, cutright ,cutleft= 0, 0, 0,0
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
        while url==None:
            url=MyUtils.txt(MyUtils.cachepath('savepage/savepage.txt')).l[0]
            MyUtils.sleep(3)
        MyUtils.log(f'准备保存网页：  {url}')
        page = MyUtils.Chrome(url, silent=False,mine=False)
        if 'baijiahao'in url:
            cutright=400
            cuttop=90
            path='百家号/'

        page.save(minsize=minisize, scale=scale, look=look, t=t,path=path,
                  extrafunc=extrafunc,pause=pause,
                  cutright=cutright,cuttop=cuttop,cutbottom=cutbottom,
                  )
        page.quit()
        MyUtils.txt(MyUtils.cachepath('savepage/savepage.txt')).delete(url)
