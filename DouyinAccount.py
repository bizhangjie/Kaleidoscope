import time

from retrying import retry
from selenium.webdriver.common.by import By

import DouyinUtils
import MyUtils
# 小号
# Account='MS4wLjABAAAAlHut0BHZMJOe2xxGFCq9IDcV-MuLNL_XIxRTZiO8nThhJMYmWRhbFlzfrIo5MqCH'
# 大号
Account='MS4wLjABAAAAPw9P0loZpA5wjaWiHzxQb4B9E2Jgt4ZPWfiycyO_E4Q'
users = DouyinUtils.allusers
readytodownload = DouyinUtils.readytodownload

@retry(retry_on_exception=MyUtils.retry)
def main():

    # 变量
    likecount = {}
    ispic = []
    urllist = []
    Page = MyUtils.Chrome(mine=True)
    page = Page.driver

    # 登录
    # region
    page.get(f'https://www.douyin.com/user/{Account}?showTab=like')
    # MyUtils.skip([page, By.ID, "captcha-verify-image"])
    # MyUtils.skip([page, By.ID, "login-pannel"])
    # endregion

    # 下滚，保存url列表
    Page.down()
    MyUtils.log(f'下滚完毕。请等待一段相当长的时间')
    for VideoElement in DouyinUtils.HostPieces([page]):
        VideoUrl, VideoNum = DouyinUtils.piecetourlnum([VideoElement])
        urllist.append(VideoUrl)
        ispic.append(DouyinUtils.IsPic([VideoElement]))
    MyUtils.log(f'获取完毕。共{len(urllist)}个作品。')

    # 转到Video页面，没下过的第一遍进WebUserSpectrum
    for url in urllist:
        stole = MyUtils.nowstr()
        page.get(url)
        MyUtils.skip([page, By.ID, "captcha-verify-image"])
        Page.skip('//*[@id="login-pannel"]/div[@class="dy-account-close"]',click=True)

        pic = ispic.pop(0)
        VideoNum = MyUtils.tail(url, '/')

        # 对喜欢的内容，进行强制覆盖下载，不检测本地文件和记录。

        title = DouyinUtils.Title([page])
        s = MyUtils.Element([page, By.XPATH, '/html/head/meta[3]']).get_attribute('content')
        userid = s[s.rfind(' - ') + 3:s.rfind('发布在抖音，已经收获了') - 9]
        DouyinUtils.load(pic, page, VideoNum, userid, title, readytodownload)

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
            MyUtils.log(f'出现过的的用户{userid}')
            if likecount.get(ueruid) > 1:
                likecount.update({ueruid: -111})
                MyUtils.log(f'记录了新用户{userid}')
                DouyinUtils.addauthor(ueruid, userid, users)

        # MyUtils.delog(f'视频页单次耗时{MyUtils.counttime(stole)}')
        # MyUtils.delog(likecount)
    page.quit()


if __name__ == '__main__':
    main()
