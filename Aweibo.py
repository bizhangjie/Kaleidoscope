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
        return MyUtils.rmtail(c, '?')

    type = 'edge'
    MyUtils.geturls(loop=5, func=func, type=type)


def adduser(page):
    """
    创建用户文件夹
    打开用户主页，更新头像、描述、用户名等信息
    @param page:
    @return:
    """
    page = page[0]
    author = MyUtils.removetail(page.title(), ' 的个人主页')[1:]
    useruid = MyUtils.gettail(page.url(), '/')
    userpath = f'./微博/{author}_{useruid}'
    allusers.adduser(useruid, author)

    # 保存 profile
    eprofile = page.element('//div[@state="noside"]//div[@class="wbpro-pos"]/parent::node()')
    page.up()
    page.elementshot(eprofile, f'./微博/{author}_{useruid}/profile/profile0.png', moveto=False)
    MyUtils.move(f'./微博/{author}_{useruid}/profile/profile0.png',
                 f'./微博/{author}_{useruid}/profile/profile.png', overwrite=True)
    MyUtils.deletedirandfile(f'./微博/{author}_{useruid}/profile/profile0.png')

    # 保存 avatar
    MyUtils.pagedownload(page.element(
        '//div[@state="noside"]//div[@class="wbpro-pos"]/following-sibling::*//div[starts-with(@class,"woo-avatar")]/img/@src'),
        f'./微博/{author}_{useruid}/profile/avatar.png', t=2, redownload=True, overwrite=True)

    # 保存 cover
    page.click('//div[@state="noside"]//div[@class="woo-picture-cover"]')
    MyUtils.pagedownload(page.element('//div[starts-with(@class,"Viewer_wrap")]//img[1]/@src'),
                         f'./微博/{author}_{useruid}/profile/cover.png', t=3, redownload=True,
                         overwrite=True)

    page.refresh()

    return useruid, author, userpath


def getpics(page, path):
    page = page[0]
    # 图片元素列表
    es = page.elements(
        '//*[@id="app"]//main//div[contains(@class,"content")]//div[contains(@class,"woo-picture-")]/img',
        strict=False)
    if es == []:
        return
    # 点击图片
    page.click(es[0])
    MyUtils.sleep(1)
    # 查看大图
    page.click('//*[@id="app"]//*[contains(text(),"查看大图")]')
    for count in range(len(es)):
        if MyUtils.isfile(f'{path}/{count}.jfif', notnull=True) or MyUtils.isfile(
                f'{path}/{count}.jpg', notnull=True) or MyUtils.isfile(f'{path}/{count}.png',
                                                                       notnull=True) or MyUtils.isfile(
            f'{path}/{count}.png', notnull=True):
            continue
        # 查看原图
        page.click('//*[@id="app"]//*[contains(@title,"查看原始图片")]', strict=False)
        page.switchto(-1)
        page.download(page.url(), f'{path}/{count}', t=4, overwrite=True, redownload=False)
        page.close()
        page.hotkey('right')
        MyUtils.sleep(1)


def saveposter(page, useruid, author, userpath, t=2):
    page = page[0]
    # 我们先假设，上下定格足够保存所有的 poster
    page.set_window_size(877, 2000)

    for i in MyUtils.listdir(userpath):
        dates=[]
        # num=4
        def func(ret, l):
            page=l[0]
            posteruids = MyUtils.listdir(f'{userpath}/poster/')
            eposters = page.elements('//div[@class="vue-recycle-scroller__item-view"]')[:]
            etimes = page.elements(
                f'//div[@class="vue-recycle-scroller__item-view"]//a[contains(@href,"https://")]')[:]
            for etime, eposter in zip(etimes, eposters):
                try:
                    href, date = etime.get_attribute('href'), MyUtils.Time(etime.get_attribute('title')).s()
                    if not date in dates:
                        dates.append(date)
                        # 只保存用户创建的微博
                        if useruid in href:
                            posteruid = MyUtils.standarlizedFileName(date)
                            if not posteruid in posteruids:
                                posteruids.append(posteruid)
                                # 下载缩略封面
                                if not MyUtils.isfile( f'{userpath}/poster/{posteruid}/.png',notnull=True):
                                    page.elementshot(eposter, f'{userpath}/poster/{posteruid}/', yoffset=-93)
                                # 打开详情页
                                page.open(href)
                                if not MyUtils.isfile(f'{userpath}/poster/{posteruid}/basic.png', notnull=True):
                                    page.fullscreen(path=f'{userpath}/poster/{posteruid}', autodown=True, scale=100,
                                                    cutleft=240, cuttop=135)
                                # 保存图片
                                getpics(page=[page], path=f'{userpath}/poster/{posteruid}', )
                                page.close()
                except Exception as e:
                    continue
        page.Down(start=0,func=func,scale=150)


if __name__ == '__main__':
    page = MyUtils.Chrome(mine=True, silent=False)
    linklist = WBUtils.getwebusers([page])
    for hostlink in linklist:
        page.get(f'{hostlink}', t=1)
        useruid, author, userpath = adduser([page])
        saveposter([page], useruid, author, userpath)
