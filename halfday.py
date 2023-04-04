import MyUtils


def main():
    opened=False
    while True:
        while not MyUtils.now().hour in [12,13,14,15,16,20,21,22,23]:
            MyUtils.sleep(60*20)
            continue
        # 准备打开或者保存半日
        if not opened:
            opened=True
            f=MyUtils.txt(MyUtils.cachepath('halfday.txt'))
            f.clear()
            f.l+=['"今天的我将和现实对话。今天的我将和未来的自我对话。\n']
            f.save()
            MyUtils.getscreenlock()
            MyUtils.look(f.path)
            MyUtils.releasescreenlock()
        # 保存
        if MyUtils.now().hour in [16,23]:
            opened=False
            d={16:'白日时',23:'夜日时'}
            f=MyUtils.txt(MyUtils.cachepath('halfday.txt'))
            fout=MyUtils.txt(MyUtils.projectpath(f'self/半日记/{MyUtils.today()}_{d[MyUtils.now().hour]}.txt'))
            fout.l=f.l
            fout.save()
            MyUtils.sleep(60*120)




if __name__ == '__main__':
    main()
