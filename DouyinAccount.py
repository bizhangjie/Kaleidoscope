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
    likecount = {}
    ispic = []
    urllist = []
    page = MyUtils.Chrome(f'https://www.douyin.com/user/{Account}',mine=True)
    _,urls=DouyinUtils.hostdata([page],tab='喜欢')
    for videourl in urls:
        useruid,author=DouyinUtils.load([page], videourl)
        if useruid==None:
            continue
        DouyinUtils.dislike([page])

        if (useruid in list(users.d.keys())):
            MyUtils.delog('已在用户列表中')
            continue

        #     查看是否需要记录UserUID，出现重复超过1次的用户即记录
        if likecount.get(useruid) == None:
            likecount.update({useruid: 1})
            MyUtils.log('新用户')
        else:
            likecount.update({useruid: likecount.get(useruid) + 1})
            MyUtils.log(f'出现过的的用户{useruid}')
            if likecount.get(useruid) > 1:
                likecount.update({useruid: -111})
                MyUtils.log(f'记录了新用户{useruid}')
                DouyinUtils.addauthor(useruid, author, users)
    page.quit()


if __name__ == '__main__':
    main()
