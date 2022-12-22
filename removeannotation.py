import MyUtils

def main():
    for fname in ['Geometry.cpp','Geometry.h','Rtree.cpp','Rtree.h','Rtree.cpp','test.cpp','hw6.cpp','QuadTree.cpp','QuadTree.h',]:
        path=MyUtils.desktoppath(f'地理空间数据库/hw6-2022 王勇健/{fname}')
        if not MyUtils.isfile(path):
            return
        f=MyUtils.txt(path)
        newl=[]
        for i in f.l:
            if '//'in i and not './/'in i:
                i=MyUtils.removetail(i,'//')
            newl.append(i)
            print(i)
        f.l=newl
        f.save()

if __name__ == '__main__':
    main()