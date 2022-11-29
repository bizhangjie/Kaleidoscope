import MyUtils

if __name__=='__main__':
    f=MyUtils.rtxt(MyUtils.projectpath('browser/tieba.txt'))
    page=MyUtils.Edge()
    f.set()
    for url in f.l:
        num=url
        if '?'in url:
            num=MyUtils.removetail(url, '?')
        num=MyUtils.gettail(num,'/')
        page.get(url)
        title=page.title()
        title=MyUtils.removetail(title,'_百度贴吧')
        lasturl=page.element("//a[contains(text(),'尾页')]/@href")
        lastpagenum=int(MyUtils.gettail(lasturl,'='))
        page.quit()
        for pn in range(1,lastpagenum+1):
            # 貌似每次要新建浏览器，不能直接该地址，否则会反爬
            page=MyUtils.Chrome(f'tieba.baidu.com/p/{num}?pn={pn}',silent=True,mine=True)
            if 'wappass'in page.url():
                MyUtils.Exit('反爬验证异常。')
            path=MyUtils.userpath(f'Pictures/集锦/tieba/{num}_{title}/第{pn}页/')
            page.save(path=path)
            page.quit()

