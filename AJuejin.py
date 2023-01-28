import MyUtils

if __name__ == '__main__':
    for url in ['https://juejin.cn/post/7022561176248647711']:
        page = MyUtils.Edge(url, silent=True)
        titletail=' - 掘金'
        path='./掘金/'
        page.save(path=path,minsize=(200, 200), scale=300, autodown=True, look=True,titletail=titletail)
        page.quit()

