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
    MyUtils.delog(f'探测作者{uid}视频页的第{pagenum}页')
    res = requests.get(url, headers=MyUtils.headers)
    # 如果结束就退出
    if pagenum * 30 > res.json()['data']['page']['count'] and not pagenum == 1:
        return False
    return res

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
def uidtoid(UID):
    url = (f'https://api.bilibili.com/x/space/arc/search?mid={UID}&ps=30&tid=0&pn={1}&keyword=&order=pubdate&jsonp=jsonp')
    res = requests.get(url, headers=MyUtils.headers)
    # 这个就是第一个作者author
    # print(f"[upid] {res.json()['data']['list']['vlist'][0]['author']}")
    try:
        for i in res.json()['data']['list']['vlist']:
        # 由于存在可能有合作，多个author，因此要遍历
            # 一般来说只会有一个mid，对应相应的author
            if not i['mid'] == int(UID):
                continue
            return MyUtils.standarlizedFileName(i['author'])
    except:
        MyUtils.Exit(f"[upid] error when trying mid(UID)={UID}")


# 通过up名称从记录中获取up uid
def idtouid(id):
    return videouserspectrum.find(id)

def skipdownloaded(bvid):
    return str(bvid) in MyUtils.keys(videospectrum.d)

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
    def __init__(self,d):
        self.bvid=d['bvid']
        # self.length=d['length']
        # self.author=d['author']
        # self.title=d['title']
        # self.description=d['description']
        # self.pic=d['pic']
        # self.subtitle=d['subtitle']

# 检查cache是否为空
def checkempty():
    cachepath='./bili/cache'
    if not [] == MyUtils.listdir(cachepath):
        MyUtils.Open(MyUtils.standarlizedPath(cachepath))
        MyUtils.Exit('cache不为空。')

# 下载器打开情况下MyUtils下载
def download(bvid,author=None):
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