import time

import MyUtils


def fun():
    pass


def main():
    fun()


if __name__ == '__main__':

    f = MyUtils.rtxt(MyUtils.projectpath('browser/Spectrum.txt'))
    # 对Edge浏览器导出的Spectrum收藏夹（第二个）进行遍历网站收集
    def addto():
        page = MyUtils.Edge('file:///D:/Kaleidoscope/favorites_2022_11_29.html', silent=True)
        lis = page.elements('/html/body/dl/dt[1]/dl/dt[2]//a/@href')
        for i in lis:
            f.add(i)
    addto()

    def allocate():
        for j in ['youtube','bili','zhihu','huya','weibo','douyin','baijiahao','tieba','twitter','wallhaven','dandanzan','cc98','xiaohongshu','weixin','baike','haokan','www.baidu.com']:
            ff=MyUtils.rtxt(MyUtils.projectpath(f'/browser/{j}.txt'))
            dlis=[]
            for i in f.l:
                if j in i:
                    ff.add(i)
                    dlis.append(i)
            f.delete(dlis)
    # allocate()
