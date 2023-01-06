import MyUtils

if __name__ == '__main__':
    page = MyUtils.Chrome(silent=True)
    f = MyUtils.txt(MyUtils.projectpath('./browser/baike.txt'))
    for url in ['https://baike.baidu.com/item/%E5%85%8B%E9%87%8C%E5%A7%86%E6%9E%97%E5%AE%AB/522193?fr=aladdin',
                'https://baike.baidu.com/item/%E4%BF%84%E7%BD%97%E6%96%AF%E5%85%8B%E9%87%8C%E5%A7%86%E6%9E%97%E5%AE%AB/1182168?fr=aladdin']:
        # for url in f.l:
        page.get(url)
        path = page.save(MyUtils.collectionpath('./百度百科/'), titletail='_百度百科', minsize=(9999, 9999), scale=200)
        albumurl = page.element('/html/body//div[@class="summary-pic"]//a[starts-with(@href,"/pic/")]/@href')
        page.open(albumurl)
        checklist = []
        imgurl = page.element('//*[@id="imgPicture"]/@src')
        count = 0
        while not imgurl in checklist:
            checklist.append(imgurl)
            count += 1
            namelist = []
            name = ''
            MyUtils.extend(namelist, page.elements('//*[@id="picture-dialog"]/div[1]/div[1]//*/text()', strict=False),
                           page.elements('//*[@id="picture-dialog"]//div[contains(@class,"picture-footer")]//span[@class="text"]/text()', strict=False))
            for i in namelist:
                name += f'{i} - '
            name += f'{count}'
            MyUtils.pagedownload(imgurl, f'{path}/相册图片/{name}.jfif')
            page.click('//*[@id="imgPicture"]')
            MyUtils.sleep(1)
            imgurl = page.element('//*[@id="imgPicture"]/@src')

    page.quit()
