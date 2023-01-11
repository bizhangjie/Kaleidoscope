import MyUtils

# 执行可执行文件生成csv
def excute():
    MyUtils.Open(r'D:\standardizedPF\repositories\hack-browser-data-windows-64bit\hack-browser-data-windows-64bit.exe')
    MyUtils.sleep(7)

# 移植csv内容
def move():
    sourcepath=r'D:\standardizedPF\repositories\hack-browser-data-windows-64bit\results\microsoft_edge_default_history.csv'
    targetpath=MyUtils.projectpath('self/记录 语录 随笔 随想/浏览器记录/edge.csv')
#     将sourcepath csv的内容复制到targetpath csv
    f1=MyUtils.Csv(sourcepath,title=['Title','URL','VisitCount','LastVisitTime'])
    f2=MyUtils.Csv(targetpath,title=['Title','URL','VisitCount','LastVisitTime'])
    f2.merge(f1)
    # MyUtils.Open(f2.path)

    sourcepath = r'D:\standardizedPF\repositories\hack-browser-data-windows-64bit\results\chrome_default_history.csv'
    targetpath = MyUtils.projectpath('self/记录 语录 随笔 随想/浏览器记录/chrome.csv')
    #     将sourcepath csv的内容复制到targetpath csv
    f1 = MyUtils.Csv(sourcepath, title=['Title', 'URL', 'VisitCount', 'LastVisitTime'])
    f2 = MyUtils.Csv(targetpath, title=['Title', 'URL', 'VisitCount', 'LastVisitTime'])
    f2.merge(f1)
    # MyUtils.Open(f2.path)

def main():
    # excute()
    move()

if __name__ == '__main__':
    main()
