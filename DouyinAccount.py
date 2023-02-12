import time

from retrying import retry
from selenium.webdriver.common.by import By

import DouyinUtils
import MyUtils
# 小号
# Account='MS4wLjABAAAAlHut0BHZMJOe2xxGFCq9IDcV-MuLNL_XIxRTZiO8nThhJMYmWRhbFlzfrIo5MqCH'
# 大号
Account='MS4wLjABAAAAPw9P0loZpA5wjaWiHzxQb4B9E2Jgt4ZPWfiycyO_E4Q'

@retry(retry_on_exception=MyUtils.retry)
def main():
    # 初`始`化``
    users = DouyinUtils.allusers
    allpieces = DouyinUtils.allpieces
    readytodownload = DouyinUtils.readytodownload

    # 变量
    likecount = {}
    ispic = []
    Page = MyUtils.Chrome(mine=True)
    page = Page.driver

    while True:
        # 登录
        # region
        page.get(f'https://www.douyin.com/user/{Account}?showTab=like')
        # MyUtils.skip([page, By.ID, "captcha-verify-image"])
        # MyUtils.skip([page, By.ID, "login-pannel"])
        # endregion

        # 转到喜欢页面
        # page.get(MyUtils.MyElement([page, By.XPATH, '//a[starts-with(@href,"//www.douyin.com/user/")]']).get_attribute('href'))
        # time.sleep(1)
        # DouyinUtils.HostPiecesLike([page])

        # 下滚，保存url列表
        MyUtils.scroll([page])
        urllist = []
        for VideoElement in DouyinUtils.HostPieces([page]):
            VideoUrl, VideoNum = DouyinUtils.piecetourlnum([VideoElement])
            urllist.append(VideoUrl)
            ispic.append(DouyinUtils.IsPic([VideoElement]))

        # 逐一打开
        for url in urllist:
            stole = MyUtils.nowstr()
            # 转到Video页面，没下过的第一遍进WebUserSpectrum
            page.get(url)

            # 跳过验证
            MyUtils.skip([page, By.ID, "captcha-verify-image"])
            e = Page.element('//*[@id="login-pannel"]/div[@class="dy-account-close"]', strict=False)
            if not e == None:
                Page.click(e)

            # 变量
            pic = ispic.pop(0)
            VideoNum = MyUtils.tail(url, '/')

            # if DouyinUtils.skiprecorded(VideoNum):
            #     continue
            title = DouyinUtils.Title([page])
            s = MyUtils.Element([page, By.XPATH, '/html/head/meta[3]']).get_attribute('content')
            userid = s[s.rfind(' - ') + 3:s.rfind('发布在抖音，已经收获了') - 9]
            # if DouyinUtils.skipdownloaded(pic, allpieces, VideoNum, title, userid):
            #     # 取消喜欢
            #     DouyinUtils.dislike([page])
            #     MyUtils.delog('已取消喜欢')
            #     continue
            path = '../抖音/' + userid

            # 添加下载
            DouyinUtils.load(pic, page, VideoNum, userid, title, DouyinUtils.readytodownload)

            # 跳过直播
            try:
                userurl = MyUtils.Element([page, By.XPATH, '//*[@id="root"]//div[@data-e2e="user-info"]//a[contains(@href,"www.douyin.com/user")]'], depth=9, silent=True).get_attribute('href')
            except Exception as e:
                MyUtils.warn(e)
                time.sleep(999)
            if userurl.rfind('live') > 0:
                continue

            # 获取UserUID
            ueruid = userurl[userurl.rfind('/') + 1:]
            MyUtils.delog(ueruid)

            # 取消喜欢
            DouyinUtils.dislike([page])
            MyUtils.delog('已取消喜欢')

            # # 跳过UserUID已经记录的
            if (ueruid in list(users.d.keys())):
                MyUtils.delog('已在用户列表中')
                continue

            #     查看是否需要记录UserUID，出现重复超过1次的用户即记录
            if likecount.get(ueruid) == None:
                likecount.update({ueruid: 1})
                MyUtils.log('新用户')
            else:
                likecount.update({ueruid: likecount.get(ueruid) + 1})
                MyUtils.log('出现过的的用户')
                if likecount.get(ueruid) > 1:
                    likecount.update({ueruid: -111})
                    MyUtils.log('记录了新用户')
                    DouyinUtils.addauthor(ueruid, userid, users)

            MyUtils.log(f'上个作品添加下载耗时{MyUtils.counttime(stole)}')
            MyUtils.delog(likecount)
        # 结束
        page.quit()


if __name__ == '__main__':
    main()
