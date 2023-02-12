import MyUtils
new='chrome'

def main():
    root=r'D:\standardizedPF\python\310'
    root=MyUtils.standarlizedPath(root)
    if new=='chrome':
        page=MyUtils.Edge('https://chromedriver.chromium.org/downloads')
        href=page.element('/html/body/div[1]/div/div[2]/div[3]/div/div[1]/section[2]/div[2]/div/div/div/div/div/div/div/div/ul[1]/li[2]/p/a/@href')
        page.get(href)
        el=page.element('/html//table//a[text()="chromedriver_win32.zip"]')
        href=el.get_attribute('href')
        MyUtils.pagedownload(href,root+'/chromedriver_win32.zip',redownload=True)
        MyUtils.unzip(root+'/chromedriver_win32.zip')
        MyUtils.move(root+'/chromedriver_win32/chromedriver.exe',root+'/chromedriver.exe',overwrite=True)
    if new=='edge':
        page=MyUtils.Chrome('https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/')
        href=page.element('//*[@id="downloads-channel"]//a[contains(@aria-label,"stable channel")and contains(@aria-label,"x64")]/@href')
        MyUtils.pagedownload(href,root+'/edgedriver_win64.zip',redownload=True)
        MyUtils.unzip(root+'/edgedriver_win64.zip')
        MyUtils.move(root+'/edgedriver_win64/msedgedriver.exe',root+'/msedgedriver.exe',overwrite=True)
    page.quit()

if __name__ == '__main__':
    main()
