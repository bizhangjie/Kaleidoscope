import MyUtils
import XHSUtils

allusers=XHSUtils.allusers

def main():
    pass

if __name__ == '__main__':
    page=MyUtils.Chrome(mine=True)
    for i in allusers.l:
        # 转到网页
        page.get(f'https://www.xiaohongshu.com/user/profile/{i}')

        # 获取用户数据
        author=page.element('//*[@id="app"]/div/div//div[@class="right"]//div[@class="user-name"]/span').text
        des=''
        lis=page.elements('//*[@id="app"]/div/div//div[@class="right"]//div[@class="user-name"]/div')
        for j in lis:
            des+=j.text
        avatorpath=f'./小红书/{author}/avator/'
        newpath=avatorpath+f'{len(MyUtils.listfile(avatorpath))}'

        MyUtils.pagedownload(page.element('//*[@id="app"]/div/div//div[@class="left"]//img').get_attribute('src'),)


        # 获取作品列表
        page.scroll()
        lis1=page.elements('//*[@id="app"]//div[@class="note-column"]//div[@class="note"]')
