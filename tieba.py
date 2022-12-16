import MyUtils

if __name__=='__main__':
    f=MyUtils.txt(MyUtils.projectpath('browser/tieba.txt'))
    f.set()
    for url in ['https://tieba.baidu.com/p/8016719603']:
    # for url in f.l:
        def func1(url):
            num=url
            if '?'in url:
                num=MyUtils.removetail(url, '?')
            num=MyUtils.gettail(num,'/')
            return num

        def func2(l):
            page=l[0]
            num=l[1]
            lasturl=page.element("//a[contains(text(),'尾页')]/@href")
            lastpagenum=int(MyUtils.gettail(lasturl,'='))
            ret=[]
            for pn in range(2,lastpagenum+1):
                ret.append(f'tieba.baidu.com/p/{num}?pn={pn}')
            return ret

        def func3(l):
            page=l[0]
            if 'wappass'in page.url():
                page.look()
                MyUtils.Exit('反爬验证异常。')

        MyUtils.forum(url,'_百度贴吧','tieba',func1,func2,func3)
