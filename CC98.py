import MyUtils

if __name__ == '__main__':
    # page=MyUtils.Chrome(mine=True,silent=True)
    f = MyUtils.txt(MyUtils.projectpath('browser/cc98.txt'))


    # 已经在edge中打开，需要获取url批量保存
    def get1(loop=2):
        lis = MyUtils.geturls(loop)
        print(lis)
        f.add(lis)


    #     已经记录，直接批量保存第一页
    def get2():
        for i in f.l:
            i = i[:34]
            page = MyUtils.Chrome(i, silent=True, mine=True)
            page.save(MyUtils.collectionpath('cc98/'), titletail=' - CC98论坛', minsize=(150, 150), scale=400)
            page.quit()
        #     全部成功以后，清空待爬记录
        f.clear()


    # 保存所有页
    def get3():
        # page=MyUtils.Chrome(url,mine=True,silent=True)
        def func1(s):
            return MyUtils.gettail(s, '/')

        def func2(l):
            ret = []
            page, uid = l
            es = page.elements('//*[@id="root"]//ul/li[@class="page-item"]/a/@href')
            e = es[-1]
            e = MyUtils.removetail(e, '#')
            lastnum = MyUtils.gettail(e, '/')
            for i in range(2, int(lastnum) + 1):
                ret.append(f'https://www.cc98.org/topic/{uid}/{i}')
            return ret

        def func3(*a):
            MyUtils.sleep(3)

        for url1 in f.l:
            url = url1[:34]
            MyUtils.forum(url, '- CC98论坛', 'cc98', func1, func2, func3, t=6, scale=600, saveuid=False, look=False)
            f.delete(url1)
        f.clear()


    get1(20)
    # get2()
    # get3()
