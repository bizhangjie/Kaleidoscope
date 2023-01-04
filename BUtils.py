import time

import MyUtils
import sys
import requests
from selenium.webdriver.common.by import By

videospectrum = MyUtils.rjson('D:/Kaleidoscope/bili/VideoSpectrum.txt')
videouserspectrum = MyUtils.rjson('D:\Kaleidoscope/bili/VideoUserSpectrum.txt')
videouserexpired = MyUtils.RefreshTXT('D:\Kaleidoscope/bili/VideoUserExpired.txt')
coverspectrum = MyUtils.RefreshTXT('D:\Kaleidoscope/bili//CoverSpectrum.txt')
coveruserspectrum = MyUtils.RefreshTXT('D:/Kaleidoscope/bili/CoverUserSpectrum.txt')
downloadedindisk = MyUtils.RefreshTXT('./bili/Downloaded.txt')
readytodownload=MyUtils.cache("D:/Kaleidoscope/bili/ReadytoDownload.txt")
missing = MyUtils.rjson('D:\Kaleidoscope/bili/Missing.txt')
cachepath=MyUtils.userpath('/Videos/cache')
collectionpath=MyUtils.standarlizedPath('./bili/collection/')
collecitonvideorecord=MyUtils.rtxt(MyUtils.projectpath('./bili/CollectionVideo'))

# 从收藏夹导入用户
def addwebuser(f=videouserspectrum):
    page = MyUtils.Chrome('https://space.bilibili.com/661654199/fans/follow?tagid=475631', mine=True)
    els = page.elements('/html/body/div[2]/div[4]/div/div/div/div[2]/div[2]/div[2]/ul[1]/li/a')
    names = page.elements('/html/body/div[2]/div[4]/div/div/div/div[2]/div[2]/div[2]/ul[1]/li/a/img')
    for i in range(len(els)):
        el = els[i]
        name = names[i].get_attribute('alt')
        uid = el.get_attribute('href')
        uid = uid[len('https://space.bilibili.com/'):].strip('/')
        f.add({uid: name})
    page.quit()


@MyUtils.consume
# 提供duplication的存储解决方案
def addpiece(d):
    d = MyUtils.jsontodict(d)
    k = MyUtils.key(d)
    v = MyUtils.value(d)
    for i in videospectrum.l:
        if k == MyUtils.key(MyUtils.jsontodict(i)):
            if not v in MyUtils.value(MyUtils.jsontodict(i)):
                videospectrum.add(MyUtils.dicttojson({k: MyUtils.extend(MyUtils.value(MyUtils.jsontodict(i)), [v])}))
            else:
                return
    videospectrum.add(MyUtils.dicttojson({k: [v]}))


# 获得用户主页的response （暂时不是json - request
def hostjson(uid, pagenum, ):
    url = (f'https://api.bilibili.com/x/space/arc/search?mid={uid}&ps=30&tid=0&pn={pagenum}&keyword=&order=pubdate&jsonp=jsonp')
    MyUtils.delog('hostjson request请求')
    MyUtils.delog(f'探测作者{uid}视频页的第{pagenum}页')
    res = requests.get(url, headers=MyUtils.headers)
    # 如果结束就退出
    if pagenum * 30 > res.json()['data']['page']['count'] and not pagenum == 1:
        return False
    return res.json()

# 获得收藏夹的response （暂时不是json - request
def collectionjson(uid, pagenum, ):
    url = (f'https://api.bilibili.com/x/v3/fav/resource/list?media_id={uid}&pn={pagenum}&ps=20&keyword=&order=mMyUtils&type=0&tid=0&platform=web&jsonp=jsonp')
    MyUtils.delog(f'探测收藏夹{uid}视频页的第{pagenum}页')
    res = requests.get(url, headers=MyUtils.headers)
    # 如果结束就退出
    if pagenum * 30 > res.json()['data']['info']['media_count'] and not pagenum == 1:
        return False
    return res.json()


# 从url中获得useruid
def urltouseruid(c):
    p = ['https://space.bilibili.com/', ]
    for i in p:
        if i in c:
            c = c[len(i):]
    if c.find('/') > 0:
        c = c[:c.find('/')]
    else:
        pass
    return c


# 将用户加入下载列表
def add(uid=None):
    if not uid == None:
        c = input('请输入要添加的用户：')
    else:
        c = uid
        MyUtils.log(f'{urltouseruid(c)} added.')


# 获取bv
def filenametonum(s):
    if s == '':
        MyUtils.warn()
        sys.exit(-1)
    return s[s.rfind('_') + 1:]

# upid号转换为up名称，并且记录
@MyUtils.consume
def uidtoid(UID,refresh=False):
    # 从远程更新
    if refresh:
        url = (f'https://api.bilibili.com/x/space/arc/search?mid={UID}&ps=30&tid=0&pn={1}&keyword=&order=pubdate&jsonp=jsonp')
        page=MyUtils.Edge('www.bilibili.com',silent=True)
        page.get(url)
        e=page.element('/html/body/pre/text()')
        page.quit()
        d=MyUtils.jsontodict(e)
        # res = requests.get(url, headers=MyUtils.headers)
        # 这个就是第一个作者author
        # print(baijiahao"[upid] {res.json()['data']['list']['vlist'][0]['author']}")
        try:
            for i in d['data']['list']['vlist']:
            # 由于存在可能有合作，多个author，因此要遍历
                # 一般来说只会有一个mid，对应相应的author
                if not i['mid'] == int(UID):
                    continue
                # 更新本地记录
                ret= MyUtils.standarlizedFileName(i['author'])
                videouserspectrum.add({UID:ret})
                return ret
        except Exception as e:
            MyUtils.out(str(e)+'\n'+url)
            MyUtils.Exit(f"{e}\n[upid] error when trying mid(UID)={UID}")
#     从本地获取
    else:
        d=videouserspectrum.d
        if not UID in MyUtils.keys(d):
            return uidtoid(UID,refresh=True)
        idl=d[UID]
        if idl==[]:
            return uidtoid(UID,refresh=True)
        return idl[0]


# 通过up名称从记录中获取up uid
def idtouid(id):
    return videouserspectrum.find(id)

def skipdownloaded(bvid):
    return not  str(bvid) in MyUtils.keys(videospectrum.d)

# up主
class up():
    def __init__(self,uid=None,author=None):
        if not uid==None:
            self.uid=uid
        else:
            self.uid=idtouid(author)
        if not author==None:
            self.author=author
        else:
            self.author=uidtoid(uid)

        self.getvlist()

    def getvlist(self):
        page=MyUtils.Chrome(f'https://space.bilibili.com/{self.uid}',silent=True)
        vnum=page.element('//*[@id="page-index"]//*[@class="section-title"]/span').text
        vnum=int(vnum)
        self.vlist=[]
        pagenum=0
        while True:
            pagenum += 1
            json=hostjson(self.uid,pagenum)
            if not json:
                break
            json=json.json()['data']['list']['vlist']
            for i in json:
                self.vlist.append(video(i))

# 视频
class video():
    @MyUtils.consume
    def __init__(self, a):
        self.exist=True
        self.authors=[]
        self.useruids=[]

        # 用网页视频列表json构建
        # 这个有实际用到？？？？
        if type(a)in[dict]:
            self.bvid=a['bvid']
            self.length=a['length']
            self.author=a['author']
            self.title=a['title']
            self.description=a['description']
            self.pic=a['pic']
            self.subtitle=a['subtitle']

        #     用网页即时搜索构建
        if type(a)in [str] and 'BV'in a:
            self.bvid=bvid=a
            page=MyUtils.Edge(f'https://www.bilibili.com/video/{bvid}',silent=True)

            # 视频已失效
            if '出错啦'in page.title() or '视频去哪了呢'in page.title():
                self.exist=False
                return

            # 视频被收录到番剧内
            isfanju=page.element('/html//meta[@content="哔哩哔哩番剧"]',strict=False)
            if not isfanju==None:
                page.get(f'https://search.bilibili.com/all?keyword={bvid}&from_source=webtop_search&spm_id_from=666.25')
                time.sleep(2)
                self.title=page.elements('//*[@id="i_cecream"]/div/div[2]//h3/span.text')[-1]
                # 只保存第一个作者
                self.authors=page.elements('//span[@class="bili-video-card__av--author"].text')
                for i in page.elements('//a[@class="bili-video-card__av--owner"]@href'):
                    self.useruids.append(MyUtils.gettail(i,'com/'))
                self.author=self.authors[0]
                self.useruid=self.useruids[0]
                page.quit()
                return


            self.title=page.element(['//*[@id="viewbox_report"]/h1','//*[@id="app"]//div[@class="media-wrapper"]/h1']).text

            es=page.elements("//body//*[@id='app']//a[starts-with(@href,'//space') and contains(@class,'vip') or starts-with(@href,'//space') and contains(@class,'user') or starts-with(@href,'//space') and contains(@class,'up')]")
            useruids=[]
            authors=[]
            for i in es:
                useruids.append(MyUtils.gettail(i.get_attribute('href'),'/'))
            self.useruids=useruids=list(set(useruids))
            for i in useruids:
                authors.append(uidtoid(i))
            self.authors=authors
            if authors==[]:
                page.look()
                MyUtils.Exit(authors,es)
            if len(self.useruids)==1:
                self.useruid=useruids[0]
                self.author=authors[0]
            page.quit()

# 检查cache是否为空
def checkempty():
    if not [] == MyUtils.listdir(cachepath):
        MyUtils.Open(MyUtils.standarlizedPath(cachepath))
        MyUtils.Exit('cache不为空。')

# 下载器打开情况下MyUtils下载
def download(bvid,author=None,useruid=None,overdownloaded=False):
    if not  skipdownloaded(bvid) and not overdownloaded:
        return
    # if author==None:
    #     if useruid==None:
    #         author=video(bvid).author
    #     else:
    #         author=uidtoid(useruid)
    # if useruid==None:
    #     useruid=idtouid(author)
    MyUtils.copyto(f'https://www.bilibili.com/video/{bvid}')
    MyUtils.click(1449, 214)
    MyUtils.sleep(0.7)
    MyUtils.click(988, 500)
    MyUtils.sleep(1)
    MyUtils.hotkey('ctrl', 'v')
    MyUtils.sleep(0.7)
    MyUtils.hotkey('enter')
    MyUtils.sleep(5)

    MyUtils.click(708, 504)
    MyUtils.sleep(0.7)
    MyUtils.click(1208, 576)
    MyUtils.sleep(0.7)
    # 可能有8k 4k 1080p60 1080p 720 480 320 七种清晰度，导致有三行，同时出现多P
    MyUtils.click(1208, 606)
    MyUtils.sleep(0.7)
    MyUtils.log(f'{author} {bvid}已加入下载器')
    MyUtils.click(1246, 722)
    MyUtils.sleep(1.5)

    # 等待下载完毕后转移文件
def move(a=True):
    wait()
    if not a==True:
        useruid=a
    for i in MyUtils.listdir(cachepath):
        # 如果里面有.m4s文件就跳过
        b=True
        for j in MyUtils.listfile(i):
            if '.m4s'in j:
                b=False
                MyUtils.deletedirandfile([i])
        if not b:
            continue
        j = MyUtils.filename(i)
        j = MyUtils.removetail(j, '-')
        j, bvid = MyUtils.cuttail(j, '-')
        title, author = MyUtils.cuttail(j, '-')
        MyUtils.move(i, f'./bili/{author}_{useruid}/{title}_{bvid}')


# 等待下载完毕
def wait(t=20,silent=True):
    fsize=0
    while True:
        # 通过监视大小判断是否全部下载完成
        # newsize=MyUtils.size(cachepath)
        # if newsize==fsize:
        #     MyUtils.log(f'下载文件大小停止变化，最终为{int(fsize)}MB.')
        #     break
        # fsize=newsize
        # if not silent:
        #     MyUtils.delog(f'{cachepath}  大小：){int(fsize)}MB')

        # 通过检查是否存在.m4s文件判断是否全部下载完成
        time.sleep(7)
        bb=False
        for i in MyUtils.listdir(cachepath):
            for j in MyUtils.listfile(i):
                if '.m4s'in j:
                    bb=True
                    break
        if not bb:
            break
        if not silent:
            MyUtils.delog(f'waiting ... 等待所有下载完毕。还存在  {j}')

        time.sleep(t)


def quitdownloader():
    MyUtils.click(1426,209)
    time.sleep(0.4)
    MyUtils.hotkey('alt','tab')
    time.sleep(0.4)

def opendownloader():
    MyUtils.hotkey('alt','tab')
    time.sleep(0.4)
    MyUtils.click(1426,209)

# 清空空文件夹，删除包含m4s的，重命名文件夹
def repaircache():
    MyUtils.rmempty(cachepath)


    for i in MyUtils.listdir(cachepath):
        MyUtils.rename(i,MyUtils.removetail(i,'-'))

    dlis=[]
    for i in MyUtils.listdir(cachepath):
        for j in MyUtils.listfile(i):
            if 'm4s'in j:
                dlis.append(i)
                break
    MyUtils.deletedirandfile(dlis)
