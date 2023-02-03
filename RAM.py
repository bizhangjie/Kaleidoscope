import MyUtils
MyUtils.setrootpath('d')
def init():
    path=MyUtils.projectpath(f'./self/RAM/{MyUtils.today()}.md')
    if MyUtils.isfile(path):
        MyUtils.look(path)
    else:
        # 生成并载入最近一天的md没做完的事
        min=9999999
        for i in MyUtils.listfile(MyUtils.projectpath(f'self/RAM/')):
            fn=MyUtils.filename(i).strip('.md')
            if not '-'in i:
                continue
            delt=MyUtils.Time(fn).counttime()
            if delt<24*3600:
                latest=i
                break
            if min>delt:
                latest=i
                min=delt
        latest=MyUtils.txt(latest)

        # 添加没做完的事
        f=MyUtils.txt(path)
        for i in latest.l:
            if '- [ ]'in i:
                f.add(i)

        # 自动打开
        f.look()
if __name__=='__main__':
    MyUtils.sleep(3)
    init()