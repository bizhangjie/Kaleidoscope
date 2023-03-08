import MyUtils


def main():
    page=MyUtils.Chrome('https://gitee.com/report/china-open-source-2022',silent=False)
    page.fullscreen(path=MyUtils.cachepath('fullscreen'),clip=True,clipinterval=0.4)
if __name__ == '__main__':
    page=MyUtils.Chrome('https://zhuanlan.zhihu.com/p/607537547',mine=True)
    page.set_window_size(1000,2000)
    page.fullscreen(
        path='D:\Kaleidoscope\self\MANUAL 文档 收藏 AUTO\网页集锦\知乎\607537547谁再不愿意被AI绑架下体，我跟谁急',
        clip=True,clipinterval=0.7,top=52,bottom=62)
    page.quit()
