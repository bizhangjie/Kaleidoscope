import MyUtils

# 最大操作个数
countt = 4

Aurl = 'https://www.zhihu.com/collection/782323705'
# 获取链接和取消收藏的页面
page = MyUtils.Chrome(Aurl,silent=False,mute=True,mine=True)
def login(l):
    page=l[0]
    MyUtils.delog('等待知乎登录中')
    while 'zhihu.com/signin' in page.url() or '安全验证 - 知乎'in page.title():
        page.look()
        if '安全验证 - 知乎'in page.title():
            page.click('//*[@id="root"]/div/div[2]/footer/a')
            MyUtils.delog('clicked')
            MyUtils.sleep(1.5)
            continue
        MyUtils.sleep(30)
        page.refresh()
# login([page])
page.get(Aurl)

while True:
    answertitle = page.element(['//*[@id="root"]//main//*[@class="ContentItem-title"]'])
    title = answertitle.text
    answerurl = page.element(['//*[@id="root"]//main//*[@class="ContentItem-title"]//a']).get_attribute('href')
    page.open(answerurl)
    MyUtils.sleep(2)
    # 如果是文章
    if '/p/' in page.url():
        page.set_window_size(1000,page.get_window_size()[1])
        page.save(path=MyUtils.collectionpath(f'知乎/{MyUtils.gettail(page.url(), "/")}'), titletail='- 知乎',
                  cuttop=63,cutbottom=84,minsize=(200,200))
    else:
        # 打开第二个窗口，在这里操作回答

        # 展开问题描述
        page.click('//*[@id="root"]//main//button[contains(@class,"Button QuestionRichText-more")]', strict=False)

        Answer = page.element('//*[@id="root"]//main//div[@class="QuestionAnswer-content"]//div[@class="ContentItem AnswerItem"]',
                               '/html/body/div[1]/div/main/div/article',  # 文章，全屏
                               '/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div[1]/div[1]/div/div/div/div[2]/span[1]/div',
                               '/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div[1]/div[1]/div/div/div/div[2]/div[2]/button[1]',
                               )
        te = Answer.text
        if len(te) < 50:
            MyUtils.Exit(te)
        title = MyUtils.standarlizedFileName(title + te[:80])

        # 保存回答的文本
        # if not os.path.exists(f'./知乎/plaintext/{title}.txt'):
        #     MyUtils.txt(f'./知乎/plaintext/{title}').add(te)

        # 展开评论
        page.setscrolltop(page.getscrollheight())
        MyUtils.sleep(1)
        page.setscrolltop(page.getscrollheight()+100)
        e=page.element('//*[@id="root"]//main//div[@class="QuestionAnswer-content"]//div[contains(@class,"RichContent")]//button[contains(@class,"plain")]', strict=False)
        page.scroll(e)
        page.setscrolltop(page.getscrolltop()+100)
        page.click(e)
        MyUtils.sleep(2)
        # 展开回复
        # page.click('//*[@id="root"]/div/main//button[contains(text(),"条回复")]',strict=False)

        # 再展开一次页面
        Answer = page.element('//*[@id="root"]//main//div[@class="QuestionAnswer-content"]//div[@class="ContentItem AnswerItem"]')
        height = Answer.size['height']+500
        page.scroll(height)
        page.set_window_size(750, height)

        # 用新方法保存
        page.save(path=MyUtils.collectionpath(f'./知乎/{MyUtils.gettail(page.url(), "/")}'), titletail='- 知乎', look=True,scale=350,
                  cuttop=63,cutbottom=84,minsize=(200,200),)

    page.close()
    page.switchto(0)
    # 取消收藏
    def dicollection(l):
        page=l[0]
        e = page.element(['/html/body//div[@class="Card CollectionsDetailPage-list"]//button[contains(@class,"Collection")]',
                          '/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div[1]/div[1]/div/div/div/div[2]/div/button[2]',
                          '/html/body/div[1]/div/main/div/article/div[4]/div/div/button[3]'],strict=False)
        if not e.text == '取消收藏':
            e = page.element('/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div[1]/div[1]/div/div/div/div[2]/div/button[1]')
        if not e.text == '取消收藏':
            page.look()
            MyUtils.Exit('取消收藏失败')
        page.click(e)
        MyUtils.sleep(2)
        page.refresh()
    dicollection([page])

    MyUtils.log(f'已保存回答：{title}')
    countt -= 1
    if countt < 0:
        break

page.quit()
