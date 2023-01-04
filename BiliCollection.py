import MyUtils
import BUtils

# 不管是否和用户模式下载重复

# MyUtils.hotkey('alt','tab')
def skipdownloaded(bvid):
    return bvid in BUtils.collecitonvideorecord.l

def download(maxn=10):
    pagenum = 1
    BUtils.opendownloader()
    while True:
        json=BUtils.collectionjson('1033475199',pagenum)
        if json==False:
            break
        pagenum+=1
        for i in json['data']['medias']:
            bvid=i['bvid']
            if skipdownloaded(i['bvid']):
                continue
            BUtils.download(bvid,overdownloaded=True)
            MyUtils.delog(f'downloading {i["bvid"]}')
            BUtils.wait(t=5,silent=False)
            move()
            maxn-=1
            if maxn<0:
                BUtils.quitdownloader()
                return
    BUtils.quitdownloader()

def move():
    for i in MyUtils.listdir(BUtils.cachepath):
        MyUtils.move(i,f'./bili/collection/{MyUtils.removetail(MyUtils.filename(i),"-")}')


# 加到记录
def addtorecord():
    for i in MyUtils.listdir(BUtils.collectionpath):
        if '待移动'in i:
            continue

        bvid=MyUtils.gettail(i,'-')
        BUtils.collecitonvideorecord.add(bvid)

move()
# download(999)
# move()
addtorecord()
# page=MyUtils.Chrome('https://space.bilibili.com/661654199/favlist?fid=1033475199')
