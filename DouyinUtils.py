import json
import os
import time

from selenium.webdriver.common.by import By
import MyUtils

if __name__ in ['DouyinDownload']:
    MyUtils.setrootpath(MyUtils.getsettings('douyin'))
maxready = 9999
# 文件定义
allusers = MyUtils.RefreshJson('D:/Kaleidoscope/抖音/AllUsers.txt')
specialusers = MyUtils.RefreshJson('D:/Kaleidoscope/抖音/SpecialUsers.txt')
allpieces = MyUtils.RefreshJson('D:/Kaleidoscope/抖音/AllPieces.txt')

readytodownload = MyUtils.cache('D:/Kaleidoscope/抖音/ReadytoDownload.txt', silent=MyUtils.debug)
exceptuser = MyUtils.rtxt('D:/Kaleidoscope/抖音/FailedUsers.txt')
failed = MyUtils.Json('D:/Kaleidoscope/抖音/FailedPieces.txt')
missing = MyUtils.rjson('D:/Kaleidoscope/抖音/Missing.txt')
expirepiecex = MyUtils.rjson(MyUtils.projectpath('./抖音/ExpiredPieces.txt'))
history = MyUtils.txt('D:/Kaleidoscope/抖音/History.txt')


def turn_host_tab(l, tab='作品'):
    """
    切换主页展示条目，并返回数目。失败返回False
    @param l:
    @param tab:
    @return: 建议作品数；False代表获取失败
    """
    page = l[0]
    page.click(f'//span[text()="{tab}"]')
    try:
        psn = page.element(f"//span[text()='{tab}']/following-sibling::span/text()", strict=False)
        if psn == 0:
            MyUtils.warn(f'用户无作品。{page.url()}')
        if psn == None:
            return False
    except Exception as e:
        MyUtils.warn(f'发现用户异常。{page.url()}')
        # exceptuser.add(MyUtils.gettail(Page.url(),'/'))
        return False
    return int(psn)


def host_pieces(l, tab='作品'):
    """
    获取主页的作品
    @param l:页面数组
    @return: url数组
    """
    page = l[0]
    psn = turn_host_tab(l, tab)

    def func(ret, l):
        page = l[0]
        ret = MyUtils.Set(ret)
        登录验证([page])
        if page.click('//span[text()="刷新"]', strict=False, depth=10):
            MyUtils.sleep(1)
            #     上抬一下，以继续滚动
            page.setscrollheight(page.getscrollheight() - 100)
        oldlen = len(ret)
        if ret is None:
            ret = []
        ret = MyUtils.Set(ret + l[0].elements(
            '//div[contains(@data-e2e,"user-post-list") or contains(@data-e2e,"user-like-list")]//li//a/@href'))
        if len(ret) == oldlen:
            # 触发服务器保护机制，长久停滞
            # 这个问题似乎暂时无法解决
            MyUtils.Exit('建议尼玛重启')
            MyUtils.sleep(10)
        return ret

    ret = func([], l)
    # 如果数量获取失败就只获取一次
    if psn == False:
        psn = 1
    MyUtils.delog(f'psn = {psn}', )
    page.Down(pause=2, scale=1000)
    while psn and len(ret) < psn * 0.9:
        MyUtils.warn(f'作品数量不匹配 {len(ret)}/{psn}')
        ret = MyUtils.Set(
            ret + page.Down(start=page.getscrollheight(), scale=1300, pause=0, func=func))

    # 去重
    length1 = len(ret)
    ret = MyUtils.Set(ret)
    if not length1 == len(ret):
        MyUtils.warn('*******************\n\n\n********', f'作品重复 {length1}/{len(ret)}')

    return ret


@MyUtils.consume
def piecetourlnum(l):
    """

    @param l:作品元素
    @return: 作品url,uid
    """
    VideolElement = l[0]
    elementurl = VideolElement.get_attribute('href')
    if elementurl.find('?') > 0:
        VideoNum = elementurl[elementurl.rfind('/') + 1:elementurl.find('?')]
    else:
        VideoNum = elementurl[elementurl.rfind('/') + 1:]
    return (elementurl, VideoNum)


def IsPic(l):
    """
    传入元素，需要消除二维码页面
    @param l: 视频元素
    @return: 图文（真）还是视频
    """
    elements = MyUtils.Edge.elements(None, './div/div[3]/div', root=l[0], strict=False)
    # 思路是找到一个图文标签即可
    # 似乎图文都是在svg里的
    for el in elements:
        if el.text in ['图文'] or not None == MyUtils.Element([el, By.XPATH, './/svg'], depth=9,
                                                            silent=True):
            MyUtils.delog('图文')
            return True
            # if MyUtils.Element([el, By.XPATH, './/span/text()'], depth=9, silent=True) in ['置顶','共创']:
    MyUtils.delog('视频')
    return False


def HostPiecesNum(l):
    page = l[0]
    MyUtils.setscrolltop([page, 0])
    time.sleep(0.2)
    l1 = MyUtils.Element([page, By.XPATH, '//h2/span[2]'], depth=9, silent=True)
    l2 = MyUtils.Element([page, By.XPATH,
                          '/html/body/div[1]/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div/div[1]/span[2]'],
                         depth=9, silent=True)
    ret = 0
    if not l1 == None:
        ret = int(l1.text)
    elif not l2 == None:
        ret = int(l2.text)
    else:
        MyUtils.warn(f'作品数量获取失败.。{l1, l2}')
    MyUtils.delog(f'作品数量：{ret}')
    return ret


def HostLikeNum(l):
    page = l[0]
    l1 = MyUtils.Elements(
        [page, By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[4]/div[1]/div[1]/div[2]/span'],
        depth=9, silent=True)
    l2 = MyUtils.Elements([page, By.XPATH,
                           '/html/body/div[1]/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]/span[2]'],
                          depth=9, silent=True)
    LikeElement = l1 + l2[0]
    LikeNum = LikeElement.text
    LikeElement.click()
    return LikeNum


# 增加记录
def addauthor(useruid, author, users=allusers):
    User = None
    for i in users.l:
        if not useruid == list(MyUtils.jsontodict(i).keys())[0]:
            continue
        else:
            User = i
    if User == None:
        users.add({useruid: [author]})
        MyUtils.delog(f'添加了新用户在{users.path}中')
        return
    authors = MyUtils.jsontodict(User)[useruid]
    if not author in authors:
        users.add({useruid: authors + [author]})
        MyUtils.delog(f'添加了用户名称在{users.path}中')


def simplinfo(num, author, title):
    return json.dumps({str(num): {'disk': MyUtils.getdiskname(), 'author': author, 'title': title}},
                      ensure_ascii=False)
    # return json.dumps({str(num):{'disk':MyUtils.hashcode,'author':author,'title':title}},ensure_ascii=True)


def load(l, videourl, author=None, readytoDownload=readytodownload, ispic=None, useruid=None):
    """
    作品页进行下载
    @param l: 页面
    @param videourl: 作品url
    @param author: 已知作者
    @param readytoDownload:
    @param ispic:
    @return:useruid（如果没有传入），author（如果没有传入）
    """
    page = l[0]
    if skiprecorded(videourl=videourl, author=author):
        MyUtils.delog('已在记录中，跳过')
        return
    page.get(videourl)
    if author == None:
        userlink = page.element('//div[@data-e2e="user-info"]//a/@href')
        if 'live' in userlink:
            MyUtils.delog('直播')
            return None, None
        useruid = MyUtils.gettail(userlink, '/')
        author = page.element('//div[@data-e2e="user-info"]//a//span[not(text()="")]/text()')
    if ispic == None:
        ispic = 'note' in page.url()
    while True:
        try:
            if not ispic:
                VideoUrl = page.elements('//xg-video-container/video/source[1]/@src', depth=8)
                break
            else:
                VideoUrl = page.elements(
                    '//*[@id="root"]/div[1]/div[2]/div/main/div[1]/div[1]/div/div[2]/div/img/@src',
                    depth=8)
                break
        except:
            page.refresh()
    num = MyUtils.gettail(page.url(), '/')
    title = MyUtils.rmtail(page.element("//title/text()"), ' - 抖音')
    title = title.replace('/', '_')
    title = MyUtils.standarlizedFileName(title)
    readytoDownload.add({"list": [num, author, title, VideoUrl, ispic]})
    MyUtils.delog(f'下载队列 ({readytoDownload.length()})')
    if not useruid == None:
        return useruid, author


def dislike(l):
    Page = l[0]
    l1 = Page.elements('//*[@id="root"]/div[1]/div[2]/div/main/div[1]/div[2]/div/div[1]/div[1]',
                       strict=False)
    l1 += Page.elements(
        '//*[@id="root"]/div[1]/div[2]/div/div/div[1]/div[3]/div/div[2]/div[1]/div[1]/div',
        strict=False)
    Page.click(l1[0])
    MyUtils.delog('已取消喜欢')
    time.sleep(3)


def skiprecorded(videourl=None, author=None):
    """
    跳过记录中的
    @param videourl:
    @param author:
    @return:
    """
    _, VideoNum = MyUtils.splittail(videourl, '/')
    for i in allpieces.d.keys():
        if VideoNum in i:
            if allpieces.d[i][0]['author'] == author:
                MyUtils.log(f'作品 {VideoNum} 在记录中，跳过')
                return True
    return False


def skipdownloaded(flag, record, VideoNum, title, author, num=None):
    '''
    检查是否在磁盘中并补全记录
    @param flag:
    @param record:
    @param VideoNum:
    @param title:
    @param author:
    @param num: 应该要有的图片数
    @return:
    '''
    path = './抖音/' + author
    if (os.path.exists(f'{path}/{VideoNum}_{title}.mp4') and not flag):
        record.add(simplinfo('video' + VideoNum, author, title))
        MyUtils.log(f' {MyUtils.standarlizedPath(path)}/{VideoNum}_{title}.mp4  已存在磁盘中，补全记录')
        return True
    if flag:
        if len(MyUtils.listfile(f'{path}/{VideoNum}_{title}')) == num:
            record.add(simplinfo('pic' + VideoNum, author, title))
            MyUtils.log(f' {path}/{VideoNum}_{title} 共{num}张图片已存在磁盘中，补全记录')
            return True
        else:
            if not MyUtils.isemptydir(f'{path}/{VideoNum}_{title}'):
                MyUtils.warn(
                    f"未下载满：\n\t{path}/{VideoNum}_{title}  {len(MyUtils.listfile(f'{path}/{VideoNum}_{title}'))}/{num}")
            return False
    return False


def 滑块验证(l):
    page = l[0]
    page.skip('//*[@id="captcha_container"]', strict=False)


def 跳转验证(l):
    page = l[0]
    while '验证码中间' in page.title():
        MyUtils.sleep(3)
        MyUtils.log('等待页面跳转中...')


def 登录验证(l):
    page = l[0]
    page.click('//div[@class="dy-account-close"]', strict=False, depth=10)


def skipverify(l):
    """

    @param l:页面
    @return:
    """
    page = l[0]
    MyUtils.sleep(1)
    page.skip('//*[@id="captcha-verify-image"]', strict=False)
    page.click('//div[@class="dy-account-close"]', strict=False)
    page.click('//*[@id="login-pannel"]/div[@class="dy-account-close"]', strict=False)
    while '验证码中间' in page.title():
        MyUtils.sleep(3)
        MyUtils.log('等待页面跳转中...')


MyUtils.tip('DouyinUtils loaded.')


def hostdata(l, tab='作品'):
    """

    @param l:主页
    @return: author，作品url

    """
    Host = l[0]
    登录验证([Host])
    author = MyUtils.rmtail(Host.title(), '的主页')
    ps = host_pieces([Host], tab=tab)
    return author, ps


def piecepagedata(l):
    """

    @param l:作品页
    @return: 作品标题，ispic

    """
    Page = l[0]
    title = MyUtils.rmtail(Page.title(), ' - 抖音')
    ispic = 'note' in Page.url()
    return title, ispic
