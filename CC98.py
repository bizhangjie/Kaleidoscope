import time

import MyUtils

if __name__ == '__main__':
    page=MyUtils.Chrome(mine=True,silent=True)
    f=MyUtils.txt(MyUtils.projectpath('browser/cc98.txt'))
    MyUtils.rtxt.set(f)
    lis2=[]
    lis1=[]
    for i in f.l:
        if not 'https://www.cc98.org/topic/' in i:
            lis2.append(i)
            continue
        else:
            lis1.append(i)
        page.get(i)


        page.save(path=MyUtils.userpath(f'Pictures/集锦/cc98/'),minsize=(150,150),titletail=' - CC98论坛')

        time.sleep(2)

    print(len(lis1))
    MyUtils.openedge(lis2)
# 今日之事，所作所为，所行所历，与神迹何干？
# 诸天之上，谁立于九霄云巅？
