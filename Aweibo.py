import MyUtils
import WBUtils

# region
allusers = WBUtils.allusers


# endregion
def geturls():
    """
    从一打开的网页中获取 rul 并保存到 savepage.txt
    @return:
    """
    def func(c):
        return MyUtils.rmtail(c,'?')
    type='edge'
    MyUtils.geturls(loop=5,func=func,type=type)


def adduser(page):
    """
    打开用户主页，更新头像、描述、用户名等信息，创建用户文件夹
    @param page:
    @return:
    """
    page = page[0]
    author = MyUtils.removetail(page.title(), ' 的个人主页')[1:]
    useruid = MyUtils.gettail(page.url(), '/')
    allusers.adduser(useruid, author)

    for i in MyUtils.listdir('./微博'):
        if useruid in i:
            return useruid, author, i
    return useruid, author, f'./微博/{author}_{useruid}'


def getpics(page, path):
    page = page[0]
    # 图片元素列表
    es = page.elements('//*[@id="app"]//main//div[contains(@class,"content")]//div[contains(@class,"woo-picture-")]/img', strict=False)
    if es == []:
        return
    # 点击图片
    page.click(es[0])
    MyUtils.sleep(1)
    # 查看大图
    page.click('//*[@id="app"]//*[contains(text(),"查看大图")]')
    for count in range(len(es)):
        page.click('//*[@id="app"]//*[contains(@title,"查看原图")]')
        page.switchto(-1)
        MyUtils.pagedownload(page.url(), f'{path}/{count}', t=7)
        page.close()
        page.hotkey('cutleft')
        MyUtils.sleep(1)


def saveposter(page, useruid, author, userpath, t=2):
    page = page[0]
    # 我们先假设，上下定格足够保存所有的 poster
    # poster 按uid命名
    MyUtils.sleep(t)
    for i in MyUtils.listdir(userpath):
        posteruids =MyUtils.listdir(f'{userpath}/poster/')

        es = page.elements('//div[@class="vue-recycle-scroller__item-view"]')
        eposters = page.elements(f'//div[@class="vue-recycle-scroller__item-view"]//a[contains(@href,"https://")]')
        ecount=0
        for e in es:
            e1=eposters[ecount]
            ecount+=1
            href, date = e1.get_attribute('href'), MyUtils.Time(e1.get_attribute('title'))
            posteruid = MyUtils.standarlizedFileName(MyUtils.gettail(href, '/'))
            if posteruid in posteruids:
                continue
            posteruids.append(posteruid)
            # 下载缩略封面
            page.elementshot(f'{userpath}/poster/{posteruid}', e,yoffset=-53,extend=True)
            # 打开详情页
            page.open(href)
            page.fullscreen(path=f'{userpath}/poster/{posteruid}', autodown=True,scale=300,)
            # 保存图片
            getpics(page=[page], path=f'{userpath}/poseter/{posteruid}', )
            page.close()


if __name__ == '__main__':
    MyUtils.setrootpath(dname="HerMAJESTY")
    page = MyUtils.Chrome(mine=True, silent=True)
    linklist = WBUtils.getwebusers([page])
    for hostlink in linklist:
        page.get(f'{hostlink}',t=1)
        useruid, author, userpath = adduser([page])
        saveposter([page], useruid, author, userpath)
