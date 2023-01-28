import calendar

import MyUtils

root=MyUtils.projectpath('self/记录 语录 随笔 随想/浏览器记录/edge/')
downloadpath=r'D:/'
date=MyUtils.Time('2022-10-23')

def spawnandmerge():
    for i in MyUtils.listfile(downloadpath):
        if not None==MyUtils.research('_times.txt',MyUtils.filename(i)):
            ftimes=MyUtils.txt(i)
            i=MyUtils.filename(i)
            i=MyUtils.rmtail(i,',')
            t=MyUtils.Time(i)
        if not None==MyUtils.research('_urls.txt',MyUtils.filename(i)):
            furls=MyUtils.txt(i)
        if not None==MyUtils.research('_titles.txt',MyUtils.filename(i)):
            ftitles=MyUtils.txt(i)
    csvpath=root+t.date()+'.csv'
    if MyUtils.isfile(csvpath):
        MyUtils.warn(t.date()+'重复了')
        return
    f=MyUtils.Csv(csvpath,title=['time','url','title'])
    MyUtils.delog(len(ftimes.l))
    for i in range(len(ftimes.l)):
        f.add([ftimes.l[i],furls.l[i],ftitles.l[i]])
    MyUtils.deletedirandfile([ftimes.path,furls.path,ftitles.path],silent=True)

# 下载的移动到
def move(downloadpath):
    if not []==MyUtils.listfile(root):
        return
    for i in MyUtils.listfile(downloadpath):
        if not None==MyUtils.research(r"_\d+\.csv$", i):
            MyUtils.move(i, root+'/'+MyUtils.filename(i))


def openpage():
    MyUtils.openedge(['edge://history'])
    MyUtils.sleep(2)


def excutejs():
    MyUtils.sleep(1)
    MyUtils.hotkey('ctrl', 'shift', 'j')
    MyUtils.sleep(1)
    for file in ['getinfo.js','joinurls.js', 'jointimes.js', 'jointitles.js']:
        MyUtils.sleep(0.5)
        f=MyUtils.txt(MyUtils.projectpath('browser/'+file))
        str=''
        for i in f.l:
            str+=i+'\n'
        MyUtils.copyto(str)
        MyUtils.sleep(0.3)
        MyUtils.click(MyUtils.projectpath('browser/js console.png'),yoffset=-100)
        MyUtils.sleep(1)
        MyUtils.hotkey('ctrl','v')
        MyUtils.hotkey('enter')
        MyUtils.sleep(1)


def adjustdate(date=None):
    picroot=MyUtils.projectpath('browser/calender/')
    now=MyUtils.Now()
    month=now.month()
    if date==None:
        t=now-24*3600
    else:
        t=MyUtils.Time(date)
    day=t.day()
    if t.day()=='1':
        t=t+(24*3600*(calendar.monthrange(int(t.year()),int(t.month()))[1]))-1
    while not month==t.month():
        t=t+(24*3600*(calendar.monthrange(int(t.year()),int(t.month()))[1]))-1
        MyUtils.click(picroot+'back.png',limit=0.8)
        MyUtils.sleep(1)
#     不可能是蓝色已选中状态
    MyUtils.click(picroot+str(day)+'.png',grayscale=False)
    MyUtils.sleep(1)

def close():
    MyUtils.hotkey('ctrl','w')
    MyUtils.hotkey('ctrl','w')


def main(date=MyUtils.Time()-24*3600):
    # # 打开网页和打开控制台
    openpage()
    # # 调整到正确的日期（昨天的日期）
    adjustdate(date)
    # # 获取所有的变量
    excutejs()
    # # 关闭窗口
    close()
    # 合并文件
    spawnandmerge()


def getdate():
    lastdate=MyUtils.Time('2023-01-01')
    for i in MyUtils.listfile(root):
        newdate=MyUtils.Time(MyUtils.removetail(MyUtils.filename(i),'.csv'))
        if newdate>lastdate:
            lastdate=newdate
    return lastdate+3600*24

if __name__ == '__main__':
        date=getdate()
        while date<MyUtils.Now()-24*3600:

            MyUtils.delog(date)
            main(date)
            date+=24*3600
            MyUtils.sleep(1)