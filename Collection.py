import time

import MyUtils

if __name__ == '__main__':
#     下载页面中的图片、视频
    page=MyUtils.Edge()
    while True:
        url=input()
        MyUtils.log(url)
        page.get(url)
        if '受到举报的不安全网站'in page.title():
            page.click('//*[@id="moreInformationDropdownLink"]')
            page.click('//*[@id="overrideLink"]')
        time.sleep(1)
        e1=page.elements('//video',strict=False)
        e2=page.elements('//source',strict=False)
        e3=page.elements('//pic',strict=False)
        MyUtils.extend(e1,e2,e3)
        e1=list(set(e1))
        urls=[]
        for e in e1:
            url=(e.get_attribute('href'))
            if not url==None:
                urls.append(url)
            url=(e.get_attribute('src'))
            if not url==None:
                urls.append(url)
        for url in urls:
            if url=='':
                continue
            fname=MyUtils.gettail(url,'/')
            MyUtils.pagedownload(url,f'./网页集锦/{fname}')
