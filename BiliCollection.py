import MyUtils
import BUtils

# 不管是否和用户模式下载重复
所有下载数=200
单次下载数=4

# MyUtils.hotkey('alt','tab')
@MyUtils.consume
def skipdownloaded(bvid):
    return bvid in BUtils.collecitonvideorecord.l

def download(maxn=10,clip=3):
    # 最多总数；同时下载最多总数
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
            if 1==maxn%clip:
                BUtils.wait(t=5,silent=False)
                move()
                global page
                page.refresh()
            maxn-=1
            MyUtils.delog(f'remaining {maxn}')
            if maxn<0:
                BUtils.quitdownloader()
                return
    BUtils.quitdownloader()

def move():
    BUtils.deletehash(BUtils.cachepath)
    for j in MyUtils.listdir(BUtils.cachepath):
        for i in MyUtils.listfile(j):
            BUtils.deletehash(i)
        MyUtils.move(j,f'./bili/collection/{MyUtils.filename(j)}')


# 加到记录
def addtorecord():
    for i in MyUtils.listdir('./bili/collection'):
        if '待移动'in i:
            continue
        bvid=MyUtils.gettail(i,'-')
        BUtils.collecitonvideorecord.add(bvid)


if __name__=='__main__':
    MyUtils.getscreenlock()
    MyUtils.getcopylock()
    MyUtils.rmempty('./bili/collection')
    MyUtils.rmempty(BUtils.cachepath)
    BUtils.rmnomp4(BUtils.cachepath)
    BUtils.deletehash('./bili/collection')
    global page
    page=MyUtils.Chrome('https://www.bilibili.com/video/BV1H3411v78r',mute=True, silent=True)
    move()
    addtorecord()
    download(所有下载数,单次下载数)
    move()
    MyUtils.rmempty('./bili/collection')

    MyUtils.rmempty(BUtils.cachepath)
    BUtils.deletehash('./bili/collection')
    addtorecord()

    MyUtils.releasescreenlock()
    MyUtils.releasecopylock()
