import MyUtils

# 更新import list
if __name__ == '__main__':
    ff=MyUtils.rtxt(MyUtils.projectpath('importlist.txt'))
    res=[]
    for i in MyUtils.extend(MyUtils.listfile(MyUtils.projectpath('./')),MyUtils.listfile(MyUtils.projectpath('./TEST/'))):
        if not '.py'in i:
            continue
        f=MyUtils.txt(i)
        for i in f.l:
            if not 'import 'in i:
                continue
            if '#'in i:
                continue
            if 'from'in i:
                continue
            if 'Util'in i:
                continue
            if ')'in i:
                continue
            if '\''in i:
                continue
            if ':'in i:
                continue
            i=(MyUtils.gettail(i,'import '))
            while '.'in i:
                i=MyUtils.removetail(i,'.')
            while ' 'in i:
                i=MyUtils.removetail(i,' ')
            res.append(i)
    ff.l=(list(set(res)))
    ff.save()