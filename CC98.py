import time

import pyperclip

import MyUtils

if __name__ == '__main__':
    # MyUtils.provisionalout(MyUtils.geturls(4))
    lis=MyUtils.provisionalin()
    # page=MyUtils.Chrome(mine=True,silent=True)
    for url in lis:
        page=MyUtils.Chrome(mine=True)
        page.get(url)
        time.sleep(4)
        title=page.title()
        page.close()

        MyUtils.hotkey('win')
        MyUtils.typein('edge')
        MyUtils.hotkey('enter')
        time.sleep(2)
        MyUtils.hotkey('alt','a')
        MyUtils.copyto(url)
        MyUtils.hotkey('ctrl','v')
        MyUtils.hotkey('enter')
        # 等待网页加载时间
        time.sleep(6)
        MyUtils.getpics(1,f'./CC98/{title}/1')
        MyUtils.hotkey('ctrl','w')



# 今日之事，所作所为，所行所历，与神迹何干？
# 诸天之上，谁立于九霄云巅？