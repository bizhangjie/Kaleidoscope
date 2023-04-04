import MyUtils

if __name__ == '__main__':
    page = MyUtils.Chrome(silent=True)
    f = MyUtils.txt(MyUtils.projectpath('./browser/baike.txt'))
    for url in f.l:
        page.get(url)
        page.down()
        page.set_window_size(1300,page.getscrollheight())
        path = page.save(MyUtils.collectionpath('./百度百科/'), titletail='_百度百科', minsize=(9999, 9999),
                         top=80,bottom=80)
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
            namelist+=page.elements('//*[@id="picture-dialog"]/div[1]/div[1]//*/text()', strict=False),
                           page.elements('//*[@id="picture-dialog"]//div[contains(@class,"picture-footer")]//span[@class="text"]/text()', strict=False)
            for i in namelist:
                name += f'{i} - '
            name += f'{count}'
            MyUtils.pagedownload(imgurl, f'{path}/相册图片/{name}.jfif')
            page.click('//*[@id="imgPicture"]')
            MyUtils.sleep(1)
            imgurl = page.element('//*[@id="imgPicture"]/@src')

    page.quit()
    f.clear()