import time

import MyUtils


def fun():
    pass


def main():
    fun()


if __name__ == '__main__':
    # baijiahao=MyUtils.rtxt(MyUtils.projectpath('./browser/baijiahao.txt'))
    # pout=MyUtils.txt('new')
    # page=MyUtils.Chrome(mine=True,silent=True)
    # for i in baijiahao.l:
    #     page.get(i)
    #     page.save(path=f'{MyUtils.userpath("Pictures/集锦/其它/")}')
    #     pout.add(i)
    # page.quit()
    url='http://www.360doc.com/content/22/0207/21/38525498_1016350044.shtml'
    page=MyUtils.Edge(url,silent=True)
    page.set_window_size(800,5000)
    page.driver.get_screenshot_as_file(f'{MyUtils.collectionpath(f"/其它/{page.title()}/")}.png')