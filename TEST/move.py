import MyUtils

if __name__ == '__main__':
    t1=MyUtils.txt(MyUtils.cachepath('test1/dir/1.txt'))
    t2=MyUtils.txt(MyUtils.cachepath('test2/test1/dir/1.txt'))
    t1.l=['1','2',MyUtils.nowstr()]
    t1.save()
    src=MyUtils.cachepath('test1')
    tar=MyUtils.cachepath('test2/test1')
    MyUtils.move(src,tar,autorename=True,merge=True,overwrite=False)
    MyUtils.look(src)
    MyUtils.look(tar)
    MyUtils.sleep(40)
    MyUtils.deletedirandfile(MyUtils.cachepath('test2'))
