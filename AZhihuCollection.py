import os
import time

import MyUtils

countt=8

Aurl = 'https://www.zhihu.com/collection/782323705'
# page=MyUtils.chrome('https://www.zhihu.com/collection/791721748', silent=True,mine=True)
# page = MyUtils.Chrome('https://www.zhihu.com/collection/782323705', silent=True, mine=True)
page = MyUtils.Chrome(Aurl, silent=True, mine=True)
# page = MyUtils.Chrome(Aurl, silent=False, mine=True)
# MyUtils.skip([page,By.XPATH,'/html/body/div[1]/div/div[4]/div[1]/div[1]/a'])
time.sleep(2)

while True:
    # 获取标题
    answertitle = page.element(['//*[@id="root"]//main//*[@class="ContentItem-title"]'])
    title = answertitle.text
    answerurl=page.element(['//*[@id="root"]//main//*[@class="ContentItem-title"]//a']).get_attribute('href')
    # 点击标题产生新窗口
    # 不一定能点击成功，我也不知道为什么
    page.newwindow(answerurl)
    if len(page.windows())==2:
        page.switchto(-1)
    else:
        MyUtils.Exit()
    time.sleep(2)
    # 第二窗口，如果是文章
    if '/p/' in page.url():
        page.save(MyUtils.collectionpath(f'知乎/{MyUtils.gettail(page.url(),"/")}'),titletail='- 知乎')
    else:
        # 打开第二个窗口，在这里操作回答
        Answer = page.element(['//*[@id="root"]//main//div[@class="QuestionAnswer-content"]//div[@class="ContentItem AnswerItem"]',
                               '/html/body/div[1]/div/main/div/article', # 文章，全屏
                               '/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div[1]/div[1]/div/div/div/div[2]/span[1]/div',
                               '/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div[1]/div[1]/div/div/div/div[2]/div[2]/button[1]',
                               ])
        te = Answer.text
        if len(te) < 50:
            MyUtils.Exit(te)
        title = MyUtils.standarlizedFileName(title + te[:80])

        # 保存回答的文本
        # if not os.path.exists(f'./知乎/plaintext/{title}.txt'):
        #     MyUtils.txt(f'./知乎/plaintext/{title}').add(te)

        # 展开回答
        page.click('//*[@id="root"]//main//div[@class="QuestionAnswer-content"]//div[contains(@class,"RichContent")]//button[contains(@class,"plain")]')
        MyUtils.sleep(2)

        #再展开一次页面
        Answer=page.element('//*[@id="root"]//main//div[@class="QuestionAnswer-content"]//div[@class="ContentItem AnswerItem"]')
        height=2000 + Answer.size['height']
        page.set_window_size(800, height)

        # 点开每个展开的评论
        # btns=page.elements('//*[@id="root"]//main//div[contains(@class,"Comments-container")]//button[contains(text(),"条回复")]')



        # # 截屏
        # #    需要滚动一下，否则图片会虚化
        # for i in range(height):
        #     i+=100
        #     page.scroll(height)
        # MyUtils.scrshot([page.element(['/html/body/div[1]/div/main/div/div/div[3]/div[1]/div/div[2]/div/div',
        #                                '/html/body/div[1]/div/main/div/article',
        #                                '/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div[1]/div[1]']), (f'./知乎/{title}/{title}.png')])
        # time.sleep(2)

        # # 回答里的图片保存
        # piccount = 0
        # pics = page.elements(['//*[@id="root"]//main//div[@class="RichContent-inner"]//figure//img'],strict=False)
        # for pic in pics:
        #     url = pic.get_attribute('data-actualsrc')
        #     piccount += 1
        #     picpath = f'./知乎/{title}/{piccount}.png'
        #     try:
        #         if MyUtils.isfile(picpath):
        #             continue
        #         if False == MyUtils.pagedownload(url, picpath, t=5):
        #             MyUtils.Exit(-1)
        #     except Exception as e:
        #         page.look()
        #         MyUtils.Exit(e)

        # 用新方法保存
        page.save(MyUtils.collectionpath(f'./知乎/{MyUtils.gettail(page.url(),"/")}'),titletail='- 知乎')

    page.close()
    page.switchto(0)
    # 取消收藏
    e = page.element(['/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div[1]/div[1]/div/div/div/div[2]/div/button[2]',
                      '/html/body/d iv[1]/div/main/div/article/div[4]/div/div/button[3]'])
    if not e.text == '取消收藏':
        e = page.element('/html/body/div[1]/div/main/div/div[1]/div[2]/div[2]/div[1]/div[1]/div/div/div/div[2]/div/button[1]')
    if not e.text == '取消收藏':
        page.look()
        MyUtils.Exit('取消收藏失败')
    page.click(e)
    time.sleep(2)
    page.refresh()

    MyUtils.log(f'已保存回答：{title}')
    countt-=1
    if countt<0:
        break
