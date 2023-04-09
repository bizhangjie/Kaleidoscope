import MyUtils
import XHSUtils
allusers=XHSUtils.allusers
MyUtils.setrootpath(dname=["4","HerMAJESTY"])

if __name__ == '__main__':
    page=MyUtils.Chrome(mine=True,silent=False)
    # 不要用不带缓存的selenium打开，否则直接全禁一段时间！！！
    for i in allusers.l:
        # 转到网页
        page.get(f'https://www.xiaohongshu.com/user/profile/{i}')

        # 获取用户数据
        author=page.element('//*[@id="app"]/div[1]/div[1]/div/div[1]/span/text()')
        des=page.elements('//*[@id="app"]/div[1]/div[1]/div/div[3]/text()')
        # 下载头像
        avatorpath=f'./小红书/{author}/avator/'
        newpath=avatorpath+f'{0}.jfif'
        MyUtils.pagedownload(MyUtils.rmtail(page.element('//*[@id="app"]/div[1]/div[1]/div/img/@src'),'?image'),newpath,overwrite=True,redownload=True,t=3)


        # 获取作品列表
        if not MyUtils.debug:
            page.down()
            MyUtils.sleep(3)
        while not page.getscrolltop()==0:
            lis1=MyUtils.extend([],page.elements('//*[@id="app"]/div[1]//div[@class="feeds-container"]//a[contains(@href,"explore")]/@href'),set=True)
            page.setscrolltop(page.getscrolltop()-200)
            MyUtils.sleep(2)

            for url in lis1:
                page.open(url)
                PieceNum=MyUtils.gettail(page.url(),'/')[1:]



                picurls=page.elements('//*[@id="app"]//div[@class="swiper-wrapper"]//div/@style',strict=False)
                videourl=page.element('//*[@id="app"]//div[@class="note-container"]//xg-poster/@style',strict=False)

                descriptionshot=page.elementshot(s='//*[@id="app"]/div[1]/div/div[2]/div[2]//div[@class="note-content"]',)

                if not picurls==[]:
                    for i in picurls:
                        durl=(MyUtils.gettail(i,'https:'))

                if not videourl==None:
                    durl=(MyUtils.gettail(videourl,'https:'))
                    MyUtils.pagedownload(durl,f'./小红书/{author}/video/{PieceNum}.mp4',t=5)
