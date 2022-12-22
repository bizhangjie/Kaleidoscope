import MyUtils



if __name__ == '__main__':
    path=MyUtils.desktoppath('地理空间数据库/hw6-2022 王勇健/Geometry.cpp')
    f=MyUtils.txt(path)
    newl=[]
    for i in f.l:
        if '//'in i and not './/'in i:
            i=MyUtils.removetail(i,'//')
        newl.append(i)
    f.l=newl
    f.save()
