import BUtils
import MyUtils
import BUtils


if __name__ == '__main__':
    useruid='11146827'
    author=BUtils.uidtoid(useruid)
    page=MyUtils.Chrome(f'space.bilibili.com/{useruid}/article',silent=True,mine=True)
    urls=[]
    titles=[]
    e=page.element('//*[@id="page-article"]//span[@class="be-pager-total"]/text()')
    num=int(MyUtils.removetail(e[2:],' 页'))
    for i in range(num):
        MyUtils.sleep(0.3)
        MyUtils.extend(urls,page.elements('//*[@id="page-article"]//li[contains(@class,"article-item")]//h2/a/@href'))
        # MyUtils.extend(titles,page.elements('//*[@id="page-article"]//li[contains(@class,"article-item")]//h2/a/text()'))
        if i==num-1:
            break
        page.click('//*[@id="page-article"]//li[@class="be-pager-next"]')

    MyUtils.delog()
    for url in urls:
        page.get(url)
        page.save(MyUtils.collectionpath(f'bili/article/{author}/'),scale=250)


    page.quit()