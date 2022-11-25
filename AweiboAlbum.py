import time

import MyUtils

if __name__ == '__main__':
    useruid='3799320765'
    page = MyUtils.Chrome(f'https://weibo.com/u/{useruid}?tabtype=album', mine=True)
    # page.scroll()
    time.sleep(2)
    s=page.title()
    s1=' 的个人主页 - 微博'
    if s1 in s:
        author=MyUtils.removetail(s,s1)
    if author[0]=='@':
        author=author[1:]
    picurls=[]
    for i in page.elements('//*[@id="app"]//div[@class="woo-box-item-inlineBlock"]//img'):
        picurls.append(i.get_attribute('src'))
    for i in picurls:
        fname=MyUtils.gettail(i,'/')
        path=f'./微博/{author}/相册/{fname}'
        if not MyUtils.isfile(path):
            MyUtils.pagedownload(i,path,t=5)
    MyUtils.sleep(2)
