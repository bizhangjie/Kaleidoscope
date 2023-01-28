import MyUtils

downloadpath=r'D:\Programme Files\Steam\steamapps\workshop\content\431960'
targetpath=r'e:/wallpaper engine//'
sourcepath=r'D:\Programme Files\Steam\steamapps\workshop\content\431960'



# 运行完后，能保证可以直接清空视频文件夹。
def move(source,target):
    for src in source:
        def issame(newname,path):
                dst=path+newname
                if MyUtils.isfile(dst):
                    v1=MyUtils.video(src)
                    v2=MyUtils.video(dst)
                    if v1.duration==v2.duration:
                        if MyUtils.size(src)<=MyUtils.size(dst):
                            return True
                return False
        b,newname=MyUtils.regeneratename(MyUtils.filename(src),target,regenerate=issame)
        dst=targetpath+'/'+newname
        c=MyUtils.isfile(dst)
        if b:
            MyUtils.delog('复制：',src,'    ====>   ',dst)
            # MyUtils.delog(src,dst)
            MyUtils.copyfile(src,dst)
# 同名视频比较长度。长度相通比较清晰度。
def getdownloaded(path):
    l1=[]
    for dir in MyUtils.listdir(path):
        for file in MyUtils.listfile(dir):
            if '.mp4'in file:
                l1.append(file)
                break
    return l1

def main():
    MyUtils.setrootpath('e')
    l1=getdownloaded(sourcepath)
    move(l1,targetpath)

if __name__ == '__main__':
    main()
    # MyUtils.deletedirandfile(downloadpath)