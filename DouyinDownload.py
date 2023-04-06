import time

from retrying import retry

import DouyinUtils
import MyUtils

@retry(retry_on_exception=MyUtils.retry)
def download():
    # 变量
    Failed = DouyinUtils.failed
    allpieces = DouyinUtils.allpieces
    readytoDownload = DouyinUtils.readytodownload

    # 下载
    while True:
        # 获取参数
        # region
        rec = readytoDownload.get()
        if rec == None:
            return
        (VideoNum, author, title, VideoUrl, ispic) = rec["list"]
        if author==None:
            continue
        if VideoUrl==[]:
            MyUtils.warn(f'下载url为空。')
            return
        if DouyinUtils.skipdownloaded(ispic, allpieces, VideoNum, title, author,num=len(VideoUrl)):
            MyUtils.warn('已下载。弹回。', f'VideoNum={VideoNum} HostID={author} title={title} VideoUrl={VideoUrl}')
            return
        path = './抖音/' + author
        MyUtils.delog(f'VideoNum={VideoNum} HostID={author} title={title} VideoUrl={VideoUrl}')
        # endregion
        # 判断是否图文
        if not len(VideoUrl) > 1:
            # 视频
            # region
            try:
                t = MyUtils.pagedownload(url=VideoUrl[0], path=f'{path}/{VideoNum}_{title}.mp4', t=10, )
                MyUtils.delog(f't={t}')
            except Exception as e:
                MyUtils.warn(e)
                t = False
            #     endregion
        else:
            # 图片
            # region
            t = True
            i = 0
            for url in VideoUrl:
                i += 1
                MyUtils.delog(f'开始下载，url={url}')
                try:
                    t = MyUtils.pagedownload(url=url, path=f'{path}/{VideoNum}_{title}/{i}.png', t=2) and t
                except Exception as e:
                    MyUtils.warn(e)
                    t = False
            #     endregion

        # 是否下载成功
        if t:
            if ispic:
                ispic='note'
            else:
                ispic='video'
            allpieces.addpiece(ispic+VideoNum, author, title)
            MyUtils.log(f'下载成功，{VideoNum}记录补全.\n{allpieces}]{author}  :作品编号：{VideoNum}     作品标题：{title}\n{VideoUrl}')
            # endregion
        else:
            # region
            Failed.add(MyUtils.simplinfo(VideoNum, author, title))
            MyUtils.warn(f'下载失败，{VideoNum} 记录补全到 {Failed.path}.{author} 的编号:{VideoNum} 标题:{title}\n{VideoUrl}')
        # endregion

def main(t=3):
    # 持续性唤醒
    while True:
        download()
        # MyUtils.log(f'Downloader 循环等待中...')
        t+=1
        if t>=2:
            t=0
        time.sleep(t)

if __name__=='__main__':
    main()
