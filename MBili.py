import BUtils
import Maintainace
import MyUtils

# 压力测试
# 多作者、多P
# 组织方式约定：
# ./bili/upUID/
#        视频标题_BV********.jpg(png)，
#                 分P标题.MP4，简介内容.txt。字幕文件


videospectrum = BUtils.videospectrum
videouserspectrum = BUtils.videouserspectrum
videouserexpired = BUtils.videouserexpired
coverspectrum = BUtils.coverspectrum
downloadedindisk = BUtils.downloadedindisk
missing = BUtils.missing


# 记录操作盘user、pieces
def makerecord():
    length1 = videospectrum.length()
    f = []
    for i in MyUtils.listdir('./bili'):
        f.append(i[i.rfind('_') + 1:])
        for k in MyUtils.listdir(i):
            j = MyUtils.filename(k)
            num = (BUtils.filenametonum(j))
            title = j[:-len('_' + num)]
            videospectrum.addpiece(num, BUtils.filenametonum(i), title)
    MyUtils.log('user: ', len(f))

    MyUtils.log(f'{length1}->{videospectrum.length()}')


# 打开VideoUser，决定User是否要expire
def checkweb():
    page = MyUtils.edge()
    count = 0
    for i in range(videouserspectrum.length()):
        num = videouserspectrum.get()
        count += 1
        page.execute_script(f"window.open('https://space.bilibili.com/{num}')")
        print(num)
        if count >= 20:
            break
    expire()


# 立刻从Expired更新UserList
def expire():
    while True:
        num = input('请输入expire编号：')
        num = num.strip('?').strip('https://space.bilibili.com/')
        videouserspectrum.delete(num)
        videouserexpired.add(num)
        MyUtils.log(f'{num} expired.')


# 删除操作盘里的作者文件
def delete():
    lis = []
    for i in videouserexpired.l:
        dirs = MyUtils.listdir('./bili')
        for k in dirs:
            num = k[k.rfind('_') + 1:]
            if num == i:
                lis.append(k)

    print(f'操作盘中存在的作者： {lis}')
    MyUtils.deletedirandfile(lis)


# 立刻命令行添加用户
def adduser():
    BUtils.add()


# 反向从操作盘中检查申明
def checkisindisk():
    def func(tuple):
        (uid, au, ti, d1, d) = tuple
        b = False
        for i in MyUtils.listdir('./bili'):
            if MyUtils.tellstringsame(i, au):
                b = True
                break
        if b == False:
            MyUtils.delog(f'不存在{d}{222}')
            return False
        for j in MyUtils.listdir(i):
            if MyUtils.tellstringsame(MyUtils.filename(j), f'{ti}_{uid}'):
                MyUtils.delog(f'存在{d}')
                return True
        MyUtils.delog(f'不存在{d1}{(MyUtils.listdir(i), f"{ti}_{uid}")}')
        return False

    Maintainace.checkisindisk(videospectrum, func)


def countdownloaded():
    count = 0
    for i in MyUtils.listdir('./bili'):
        for j in MyUtils.listdir(i):
            count += 1
    MyUtils.log(f'已下载个数：{count}')


def countrecord():
    MyUtils.log(f'记录总数：{videospectrum.length()}')


def count():
    # 15024
    countrecord()
    # 1224
    countdownloaded()


# 可能产生的错误，视频作者归并错了
# 先查用户所有的bv号，再核对，没有的报错，然后进行人工检查
def mistake():
    for i in MyUtils.listdir('./bili'):
        if 'bili/cache' in i or 'bili/trash' in i:
            continue
        author, useruid = MyUtils.splittail(i, '_')
        author = MyUtils.gettail(author, '/')
        print((useruid, author))
        up = BUtils.up(uid=useruid)
        vlist = []
        movelist = []
        for j in up.vlist:
            vlist.append(j.bvid)
        for j in MyUtils.listdir(i):
            bvid = MyUtils.gettail(j, '_')
            # 这个bv号是不属于这个upid对应的up主
            if not bvid in vlist:
                MyUtils.warn(f'{author} {bvid}')
                movelist.append(j)
        #         移动文件夹
        for j in movelist:
            MyUtils.move(j, f'./bili/trash/{MyUtils.filename(j)}')
        #             批量重命名
        for f in MyUtils.listdir('./bili/trash'):
            MyUtils.move(f, f'./bili/{up.author}_{up.uid}/{MyUtils.filename(f)}')


if __name__ == '__main__':
    MyUtils.setrootpath('e')
    BUtils.deletehash('./bili/collection')
    count()
    # adduser()
    # checkweb()
    # delete()
    # checkisindisk()
    # mistake()
    # makerecord()
    pass
