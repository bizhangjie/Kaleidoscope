import MyUtils
import DouyinUtils

table = MyUtils.Csv(MyUtils.projectpath('p1.csv'),
                    title=['key_word', 'uid', 'avatar', 'author1', 'author2', 'like', 'followers',
                           'description'])


def previous():
    f = MyUtils.txt(MyUtils.projectpath('p1.txt'))
    l = []
    for i in f.l:
        l.append(i[1:-1])
    f.l = list(set(l))
    f.save()


# previous()

def step1():
    f = MyUtils.cache(MyUtils.projectpath('p1.txt'), json=False)
    url='https://www.douyin.com/search/123?aid=819531e7-eda3-4d28-afd8-d95544a39fb0&publish_time=0&sort_type=0&source=normal_search&type=general'
    page = MyUtils.Chrome(url)
    page.maximize()
    MyUtils.sleep(1)
    MyUtils.click(603,262)

    while True:
        i = f.get()
        if i == "":
            continue
        MyUtils.click(DouyinUtils.搜索栏,xoffset=-100)
        MyUtils.copyto(' '+i+'')
        MyUtils.hotkey('ctrl', 'a')
        MyUtils.hotkey('ctrl', 'v')
        MyUtils.hotkey('enter')
        MyUtils.delog(i)
        MyUtils.delog(page.url())
        DouyinUtils.登录验证([page])

        for j in range(1, 7):
            try:
                str1 = f'//*[@id="douyin-right-container"]//ul/li[{j}]/div'
                avatar = page.element(str1 + '/a//img[contains(@src, "aweme-ava")]/@src',strict=False)
                if avatar==None:
                    continue
                url1 = page.elements(str1 + '/a/@href')[-1]
                uid = MyUtils.gettail(MyUtils.rmtail(url1, '?'), '/')
                l = page.elements(str1 + '/a//span[text() and not(normalize-space(text())="")]/text()')
                MyUtils.delog(len(l), l)
                l = [l[0]] + l[-5:-1]
                author1, author2, like, followers, description = l
            except:
                pass

            table.add({
                          'key_word': i, 'uid': uid, 'avatar': avatar, 'author1': author1,
                          'author2': author2, 'like': like, 'followers': followers,
                          'description': description
                      })


step1()
