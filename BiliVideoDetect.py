import time

from retrying import retry

import BUtils
import MyUtils

allusers = BUtils.videouserspectrum
readytodownload = BUtils.readytodownload
MAX = 30

BUtils.addwebuser()


@retry(retry_on_exception=MyUtils.retry)
def main():
    for useruid in allusers.d:
        MyUtils.sleep(10)
        vlist = []
        page = 1
    # 准备工作 - 检查为空，添加下载列表
        BUtils.iscacheempty()
        res = BUtils.hostjson(useruid, page)
        for a in res['data']['list']['vlist']:
            vlist.append(a['bvid'])
        readytodownload.add({useruid: vlist})
        readytodownload.add({useruid: vlist})
        MAX=MAX-1
        if MAX==0:
            break


if __name__ == '__main__':
    main()
