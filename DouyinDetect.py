import time

from retrying import retry
from selenium.webdriver.common.by import By

import DouyinUtils
import MyUtils
import Maintainace

# region
allusers = DouyinUtils.allusers
allusers.rollback()
allpieces = DouyinUtils.allpieces
readytodownload = DouyinUtils.readytodownload
ExceptionUser = DouyinUtils.exceptuser
history = DouyinUtils.history
# endregion


# @retry(retry_on_exception=MyUtils.retry)
def main():
    global host,page
    host=MyUtils.Chrome(mine=False)
    page=host
    while True:
        useruid = list(allusers.get()[0].keys())[0]
        host.get(f'https://douyin.com/user/{useruid}?showTab=post')
        MyUtils.sleep(4)
        DouyinUtils.滑块验证([host])
        DouyinUtils.跳转验证([host])
        try:
            author,urls,=DouyinUtils.hostdata([host],tab='作品')
        except Exception as e:
            MyUtils.warn(['用户异常。\n']+[e])
            continue
        DouyinUtils.addauthor(useruid, author)
        MyUtils.delog(f'  ------转到{author}的主页-----',useruid)
        for videourl in MyUtils.Set(urls):
            DouyinUtils.load([page], videourl, author=author)
            while readytodownload.length() > DouyinUtils.maxready:
                MyUtils.log('下载队列已满。Detect 等待中...')
                time.sleep(10)

if __name__ == '__main__':
    main()
