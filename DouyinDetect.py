import time

from retrying import retry
from selenium.webdriver.common.by import By

import DouyinUtils
import MyUtils
import Maintainace

# 变量
# region
users = DouyinUtils.allusers
allpieces = DouyinUtils.allpieces
readytodownload = DouyinUtils.readytodownload
ExceptionUser = MyUtils.txt('/抖音/FailedUsers.txt')
# endregion


@retry(retry_on_exception=MyUtils.retry)
def main():
    Maintainace.SeleniumSpace()
    users.rollback()
    MyUtils.Run()
    # region
    host = MyUtils.chrome()
    page = MyUtils.chrome()
    global Host,Page
    Host=MyUtils.Chrome(driver=[host])
    Page=MyUtils.Chrome(driver=[page])
    useruid = 'nothing'
    # endregion

    def detect():
        # 探测
        # 获取参数
        # region
        global Host,Page
        DouyinUtils.skipverify([Host])
        flag = DouyinUtils.IsPic([VideoElement])
        if flag:
            flagtext='图文'
        else:
            flagtext='视频'
        # endregion

        # 作品网页
        page.get(elementurl)
        MyUtils.delog(f' 探测{flagtext} {elementurl} ...')
        DouyinUtils.skipverify([Page])

        # 获取参数-标题
        # region
        title = DouyinUtils.Title([page])
        MyUtils.delog(f' title={title}')
        # endregion

        # 如果当前操作磁盘里有，增加记录
        # region
        if DouyinUtils.skipdownloaded(flag, allpieces, VideoNum, title, author):
            return
        # endregion

        # 获取下载地址
        time.sleep(1)
        DouyinUtils.load(flag, page, VideoNum, author, title, readytodownload)

    # 开始用户循环
    while useruid:
        # region
        User = users.get()[0]
        fffff = MyUtils.txt('D:/Kaleidoscope/抖音/History.txt')
        fffff.add(str(User))
        useruid = list(User.keys())[0]
        # 清除UserUID的https://www.douyin.com/user/前缀
        if useruid.find('www.douyin.com') > 0:
            users.delete(useruid)
            useruid.replace('https://www.douyin.com/user/', '')
            users.add(useruid)
        # endregion

        # 用户主页
        # region
        HostUrl = 'https://www.douyin.com/user/' + useruid.replace('https://www.douyin.com/user/', '')
        host.get(HostUrl)
        # 为什么这句会有两次import输出？？？
        # endregion
        # 获取变量
        # region
        DouyinUtils.skipverify([Host])
        author = MyUtils.Element([host, By.XPATH, '/html/head/title']).get_attribute('text')
        author = author[0:author.rfind('的主页')]
        DouyinUtils.addauthor(useruid, author, users)
        MyUtils.log(f'  ------转到{author}的主页-----',HostUrl)
        douyinSum = 0
        PiecesNum = DouyinUtils.HostPiecesNum([host])
        if PiecesNum == 0:
            ExceptionUser.add(useruid)
            continue
        # endregion
        # 下滚
        # region
        MyUtils.scroll([host])
        DouyinUtils.skipverify([Host])
        # endregion
        # 获取变量
        # region
        # endregion

        # 作品列表循环
        for VideoElement in DouyinUtils.HostPieces([host]):
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
                time.sleep(10)

    # 结束
    # region
    #     endregion


if __name__ == '__main__':
    main()
