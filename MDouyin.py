import os

import DouyinUtils
import MyUtils

allpieces = DouyinUtils.allpieces
allusers = DouyinUtils.allusers
missing = DouyinUtils.missing


# 删除不存在操作盘的作品记录
def deleteRecorded():
    deletelis = []
    count = 0
    tstart=MyUtils.now()
    for dkey in allpieces.d:
        count += 1
        if count % 10000 == 0:
            MyUtils.delog(f'正在检查记录中的是否存在操作盘 {MyUtils.diskname} 内{count}/{allpieces.length()}  不存在的计数：{len(deletelis)}')
        for i in allpieces.d[dkey]:
            if type(i) == list:
                MyUtils.delog(f'检测到存在多存储：{i}')
            if not i['disk'] == MyUtils.diskname:
                # MyUtils.warn(f'记录不属于操作盘')
                continue
            author, title = i['author'], i['title']
            
            if  not os.path.exists(f'./抖音/{author}/{dkey}_{title}.mp4') and [] == MyUtils.listfile(f'./抖音/{author}/{dkey}_{title}'):
                j = ({dkey: {"disk": MyUtils.diskname, 'author': author, "title": title}})
                deletelis.append(j)
                missing.add(j,silent=True)
    MyUtils.out(MyUtils.extend([f'将删除以下{len(deletelis)} 个记录在 {allpieces.path} 中'],deletelis))
    allpieces.delete(deletelis,silent=True)


#  删除后来又下载的missing
def deleteMissing():
    lis1 = []
    for i in missing.l:
        d = MyUtils.jsontodict(i)
        k = MyUtils.key(d)
        d = MyUtils.value(d)[0]
        path = MyUtils.standarlizedPath(f'./抖音/{d["author"]}/{k}_{d["title"]}')
        # MyUtils.delog(f'在Missing中检查是否已下载： {path}')
        if os.path.exists(path) and not [] == MyUtils.listfile(path):
            lis1.append(i)
        if os.path.exists(path + '.mp4'):
            lis1.append(i)
    MyUtils.log(f'后来新增的{len(lis1)} 个  ：{lis1}')
    for j in lis1:
        MyUtils.rtxt.delete(missing, j)


# 手动添加作者
def adduser():
    while True:
        c = input('直接输入uid添加用户：')
        DouyinUtils.allusers.add({c: ['']})


# 统计总数
def count():
    file = 0
    dir = 0
    for i in MyUtils.listdir('./抖音'):
        dir += len(MyUtils.listdir(i))
        file += len(MyUtils.listfile(i))
    MyUtils.log(f'记录总数：{allpieces.length()}')
    MyUtils.log(f"作者总数：{allusers.length()}")
    MyUtils.log(f"失败总数：{missing.length()}")
    MyUtils.log(f"视频总数：{file}")
    MyUtils.log(f"图片总数：{dir}")
    table = MyUtils.table(MyUtils.projectpath('./抖音/record.csv'))
    if file>67000:
        table.add((allpieces.length(), allusers.length(), missing.length(), file, dir, MyUtils.removetail(MyUtils.Time().s(), '.')))


# 统计重复的作品
def findduplicate():
    lis = []
    lis1 = []
    # 先统计操作盘
    for user in MyUtils.listdir('./抖音/'):
        for title in MyUtils.listdir(user):
            lis.append((MyUtils.filename(user), MyUtils.filename(title)))
        for title in MyUtils.listfile(user):
            lis.append((MyUtils.filename(user), MyUtils.filename(title).strip('.mp4')))
    MyUtils.delog(f'操作盘 {MyUtils.diskname} 统计完毕')
    #    再统计记录
    for i in DouyinUtils.allpieces.l:
        d = MyUtils.jsontodict(i)
        d = d[MyUtils.keys(d)[0]]
        if d['disk'] == MyUtils.diskname:
            continue
        p = (d['author'], d['title'])
        if p in lis:
            lis1.append(MyUtils.dicttojson({'author': p[0], 'title': p[1], 'disk': d['disk']}) + '\n')
    MyUtils.delog('记录统计完毕')
    # 输出结果
    MyUtils.txt(MyUtils.desktoppath('new')).add(lis1)
    print(lis1)

# 删去作品
def expirepiece():
    pass

# 删除O抖音中重复的
def O():
    for originaluser in MyUtils.listdir('./O抖音', full=False):
        if not originaluser in MyUtils.listdir('./抖音', full=False):
            continue
        originalpieces = MyUtils.listfile(f'./抖音/{originaluser}', full=False)
        for piece in MyUtils.listfile(f'./抖音/{originaluser}', full=False):
            for j in originalpieces:
                if j in piece and MyUtils.size(f'./抖音/{originaluser}/{j}') == MyUtils.size(f'./O抖音/{originaluser}/{piece}'):
                    MyUtils.log(f'./O抖音/{originaluser}/{piece}')
                    continue


def SET():
    allusers.set()
    allpieces.set()


if __name__ == '__main__':
    # adduser()
    # SET()
    deleteRecorded()
    deleteMissing()
    count()
    # findduplicate()
