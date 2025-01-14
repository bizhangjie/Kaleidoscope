# 每二十分钟改变鼠标位置来提醒需要记录了
# 如果一个时间内没有记录，则记为空；
# 在下一次记录返回后，先记录本次，再依次询问之前的记录补全

import MyUtils

def main():
    while True:
        if not MyUtils.now().minute in [0,20,40,60]:
            MyUtils.sleep(60)
            continue
        MyUtils.getscreenlock()
        t = MyUtils.table(f'D:/Kaleidoscope/self/20MINUTES/{MyUtils.today()}.csv', title=['时间', '内容'])
        f=MyUtils.txt(MyUtils.projectpath('./self/20MINUTES/cache.txt'))
        suggestion=['请输入当前：']
        f.l=suggestion
        f.save()
        MyUtils.hotkey('win','d')
        f.look()
        MyUtils.sleep(60)
        f=MyUtils.txt(MyUtils.projectpath('./self/20MINUTES/cache.txt'))
        l=f.l
        ls=''
        if not l==suggestion:
            for i in l:
                ls=ls+'\n'+i
        t.add({'时间':MyUtils.nowstr(mic=False),'内容':ls})
        MyUtils.releasescreenlock()


if __name__ == '__main__':
    main()
