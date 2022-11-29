import MyUtils

if __name__=='__main__':
    f=MyUtils.rtxt(MyUtils.projectpath('browser/tieba.txt'))
    page=MyUtils.Edge(silent=True)
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
        for pn in range(1,lastpagenum+1):
            page.get(f'tieba.baidu.com/p/{num}?pn={pn}')
            if 'wappass'in page.url():
                MyUtils.Exit('反爬验证异常。')
        path=MyUtils.userpath(f'Pictures/集锦/tieba/{num}_{title}/第{pn}页/')
        page.save(path=path)

