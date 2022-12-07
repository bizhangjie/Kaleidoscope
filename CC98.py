import time

import MyUtils

if __name__ == '__main__':
    # page=MyUtils.Chrome(mine=True,silent=True)
    f=MyUtils.txt(MyUtils.projectpath('browser/cc98.txt'))
    # 已经在edge中打开，需要获取url批量保存
    def get1():
        loop=2
        lis=MyUtils.geturls(loop)
        print(lis)
        f.add(lis)
    # get1()

    def get2():
    #     已经记录，直接批量保存第一页
        for i in f.l:
            page = MyUtils.Chrome(i,silent=True,mine=True)
            page.save(MyUtils.collectionpath('cc98/'),titletail=' - CC98论坛',minsize=(150,150))
            page.quit()
    get2()
# 今日之事，所作所为，所行所历，与神迹何干？
# 诸天之上，谁立于九霄云巅？
