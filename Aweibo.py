import MyUtils
import WBUtils

# region
allusers = WBUtils.allusers


# endregion
def getlinklist(page):
    page = page[0]
    page.get('https://weibo.com/u/page/follow/5849475471/followGroup?tabid=4864853400880908')
    MyUtils.sleep(1)
    return page.elements('//*[@id="scroller"]//div[@class="vue-recycle-scroller__item-view"]//a[contains(@href,"/")]/@href')


# 更新头像、描述、用户名等信息，并且创建保存用户内容的文件夹
def adduser(page):
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
        page.hotkey('left')
        MyUtils.sleep(1)


def addposters(page, useruid, author, userpath, t=2):
    page = page[0]
    MyUtils.sleep(t)
    posteruids = []
    for i in MyUtils.listdir(userpath):
        posteruids.append(MyUtils.filename(i))
    maxheight = -1
    # 持续下滚
    while maxheight < page.scrollheight():
        maxheight = page.scrollheight()
        MyUtils.delog(maxheight)
        es = page.elements('//div[@class="vue-recycle-scroller__item-view"]')
        e1s = page.elements(f'//div[@class="vue-recycle-scroller__item-view"]//a[contains(@href,"https://")]')
        ecount=0
        for e in es:
            e1=e1s[ecount]
            ecount+=1
            href, date = e1.get_attribute('href'), MyUtils.Time(e1.get_attribute('title'))
            posteruid = MyUtils.standarlizedFileName(f'{useruid}_{date}')
            if posteruid in posteruids:
                continue
            posteruids.append(posteruid)
            # 下载缩略封面
            page.elementshot(f'{userpath}/{posteruid}_poster', e,yoffset=-53,extend=True)
            # 打开详情页
            page.open(href)
            page.fullscreen(path=f'{userpath}/{posteruid}', autodown=True,scale=300)
            # 保存图片
            getpics(page=[page], path=f'{userpath}/{posteruid}', )
            page.close()
        MyUtils.sleep(2)
        page.scroll(es[-1])
        MyUtils.sleep(3)


if __name__ == '__main__':
    MyUtils.setrootpath(dname=[-1])
    page = MyUtils.Chrome(mine=True, silent=True)
    linklist = getlinklist([page])
    for userlink in linklist:
        page.get(f'{userlink}')
        MyUtils.sleep(1)
        useruid, author, userpath = adduser([page])
        addposters([page], useruid, author, userpath)
