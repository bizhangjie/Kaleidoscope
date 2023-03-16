import time

from retrying import retry
from selenium.webdriver.common.by import By

import DouyinUtils
import MyUtils
import Maintainace

# 变量
# region
allusers = DouyinUtils.allusers
allpieces = DouyinUtils.allpieces
readytodownload = DouyinUtils.readytodownload
ExceptionUser = DouyinUtils.exceptuser
history = DouyinUtils.history
# endregion


@retry(retry_on_exception=MyUtils.retry)
def main():
    # region
    if not MyUtils.debug:
        Maintainace.SeleniumSpace()
    else:
        allusers.rollback()
    global Host,Page,host,page
    Host=MyUtils.Chrome()
    Page=MyUtils.Chrome()
    host=Host.driver
    page=Page.driver
    # endregion
    # 开始用户循环
    while True:
        User = allusers.get()[0]
        history.add(MyUtils.value(User))
        useruid = list(User.keys())[0]
        useruid=MyUtils.Strip(useruid,'https://www.douyin.com/user/')

        # 用户主页
        Host.get('https://www.douyin.com/user/' + useruid)
        PiecesNum,author,ps=DouyinUtils.hostdata([Host])
        if PiecesNum==0:
            continue
        MyUtils.delog(f'  ------转到{author}的主页-----',useruid)
        DouyinUtils.addauthor(useruid, author, allusers)
        Host.scroll()

        # 作品页
        for elementurl in ps:
            VideoNum=MyUtils.gettail(elementurl,'/')
            if DouyinUtils.skiprecorded(VideoNum):
                continue
            Page.get(elementurl)
            MyUtils.sleep(1)
            DouyinUtils.skipverify([Page])
            title,ispic,=DouyinUtils.piecepagedata([Page])
            DouyinUtils.load(ispic, Page.driver, VideoNum, author, title, readytodownload)


            #     ready下载数量过载保护
            while readytodownload.length() > DouyinUtils.maxready:
                MyUtils.log('下载队列已满。Detect 等待中...')
                time.sleep(10)

if __name__ == '__main__':
    main()
