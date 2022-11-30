import MyUtils

# 更新import list
if __name__ == '__main__':
    ff=MyUtils.txt(MyUtils.projectpath('importlist.txt'))
    ff.l=[]
    ff.save()
    res=[]
    # for i in MyUtils.extend(MyUtils.listfile(MyUtils.projectpath('./')),MyUtils.listfile(MyUtils.projectpath('./TEST/'))):
    for i in MyUtils.listfile(MyUtils.projectpath('./')):
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
            if 'M'in i:
                continue
            i=(MyUtils.gettail(i,'import '))
            while '.'in i:
                i=MyUtils.removetail(i,'.')
            while ' 'in i:
                i=MyUtils.removetail(i,' ')
            while ' as'in i:
                i=MyUtils.removetail(i,' as')
            res.append(i)
    res=list(set(res))
    for i in ['os','asyncio','sys','time','multiprocessing','json','queue','csv','re','shutil']:
        res.remove(i)
    ff.l=res
    ff.save()