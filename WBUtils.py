import MyUtils
# /微博/author_useruid/profile/profile.png,cover.png,avator.png
# /微博/author_useruid/poster/postertime/png, video, basic

allusers=MyUtils.rjson(MyUtils.projectpath('微博/allusers.txt'))
MyUtils.setrootpath(dname=[-1])
def fun():
    pass


def main():
    fun()


if __name__ == '__main__':
    main()


def getwebusers(l):
    """
    从关注中获取用户列表
    @param l:
    @return:用户主页 Url
    """
    page=l[0]
    page.get('https://weibo.com/u/page/follow/5849475471/followGroup?tabid=4864853400880908')
    MyUtils.sleep(1)
    # return ['https://weibo.com'+i for i in page.elements('//*[@id="scroller"]//div[@class="vue-recycle-scroller__item-view"]//a[contains(@href,"/")]/@href')]
    return [i for i in page.elements('//*[@id="scroller"]//div[@class="vue-recycle-scroller__item-view"]//a[contains(@href,"/")]/@href')]
