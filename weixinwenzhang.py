import MyUtils

if __name__ == '__main__':
    url='https://mp.weixin.qq.com/s?__biz=MzU3ODk0MTA4OQ==&mid=2247484900&idx=1&sn=f0cb3bc3a8e760c284482cf588005a68&scene=21#wechat_redirect'
    page=MyUtils.Edge(url,silent=True)
    page.save(MyUtils.collectionpath('微信/文章/'))