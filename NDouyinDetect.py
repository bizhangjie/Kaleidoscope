from retrying import retry
import DouyinUtils
import MyUtils

# 变量
users = DouyinUtils.allusers
users.rollback()
allpieces = DouyinUtils.allpieces
readytodownload = DouyinUtils.readytodownload
ExceptionUser = MyUtils.txt('/抖音/FailedUsers.txt')


@retry(retry_on_exception=MyUtils.retry)
def main():
    # 变量
    Host = MyUtils.Chrome()
    Detail = MyUtils.Chrome()
    page=Detail
    useruid = 'nothing'

    def detect():
        # 探测
        # 获取参数
        # region
        flag = DouyinUtils.IsPic([VideoElement])
        # endregion

        # 作品网页
        Detail.get(elementurl)
        Detail.click('//div[@class="dy-account-close"]',strict=False)
        Detail.skip('//*[@id="captcha-verify-image"]')

        # 获取参数-标题
        # region
        title = DouyinUtils.Title([Detail.driver])
        MyUtils.delog(f' title={title}')
        # endregion

        # 如果当前操作磁盘里有，增加记录
        # region
        if DouyinUtils.skipdownloaded(flag, allpieces, VideoNum, title, author):
            return
        # endregion

        # 获取下载地址
        DouyinUtils.load(flag, page, VideoNum, author, title, readytodownload)

    # 开始用户循环
    while useruid:
        User = users.get()[0]
        fffff = MyUtils.txt('D:/Kaleidoscope/抖音/History.txt')
        fffff.add(str(User))
        useruid = list(User.keys())[0]

        # 清除UserUID的https://www.douyin.com/user/前缀
        # region
        if useruid.find('www.douyin.com') > 0:
            users.delete(useruid)
            useruid.replace('https://www.douyin.com/user/', '')
            users.add(useruid)
        # endregion

        # 用户主页
        # region
        HostUrl = 'https://www.douyin.com/user/' + useruid.replace('https://www.douyin.com/user/', '')
        Host.get(HostUrl)
        Host.down()
        Host.click('//div[@class="dy-account-close"]',strict=False)
        author=MyUtils.removetail(Host.element('/html/head/title/text()'),'的主页')
        DouyinUtils.addauthor(useruid, author, users)
        douyinSum = 0
        PiecesNum = DouyinUtils.HostPiecesNum([Host.driver])
        if PiecesNum == 0:
            ExceptionUser.add(useruid)
            continue
        Host.down(t=0.3)

        # 作品列表循环
        for VideoElement in DouyinUtils.host_pieces([Host.driver]):
            # 获取变量
            # region
            (elementurl, VideoNum) = DouyinUtils.piecetourlnum([VideoElement])
            # endregion

            # 跳过已记录
            # region
            if DouyinUtils.skiprecorded(VideoNum):
                continue
            # endregion
            detect()
            douyinSum += 1

            #     持续性休眠
            while readytodownload.length() > 15:
                MyUtils.log('下载队列已满。Detect 等待中...')
                MyUtils.sleep(10)

    # 结束
    # region
    #     endregion


if __name__ == '__main__':
    main()
