import MyUtils
import BUtils

# 不管是否和用户模式下载重复

pagenum = 1
# MyUtils.hotkey('alt','tab')
while True:
    json=BUtils.collectionjson('1033475199',pagenum)
    if json==False:
        break
    pagenum+=1
    for i in json['data']['medias']:
        BUtils.download(i['bvid'])


# page=MyUtils.Chrome('https://space.bilibili.com/661654199/favlist?fid=1033475199')
