import MyUtils
import BUtils

# 不管是否和用户模式下载重复

# MyUtils.hotkey('alt','tab')
def skipdownloaded(bvid):
    return bvid in BUtils.collecitonvideorecord.l

def download():
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
            BUtils.wait(t=5)
            BUtils.collecitonvideorecord.add(bvid)
            move()
    BUtils.quitdownloader()

def move():
    for i in MyUtils.listdir(BUtils.cachepath):
        MyUtils.move(i,f'./bili/collection/{MyUtils.filename(i)}')


# 加到记录
def addtorecord():
    for i in MyUtils.listdir(BUtils.collectionpath):
        i=MyUtils.removetail(i,'-')
        bvid=MyUtils.gettail(i,'-')
        BUtils.collecitonvideorecord.add(bvid)

download()
move()
addtorecord()
# page=MyUtils.Chrome('https://space.bilibili.com/661654199/favlist?fid=1033475199')
