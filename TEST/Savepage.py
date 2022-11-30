import time

import MyUtils


def fun():
    pass


def main():
    fun()


if __name__ == '__main__':
    baijiahao=MyUtils.rtxt(MyUtils.projectpath('./browser/baijiahao.txt'))
    pout=MyUtils.txt('new')
    page=MyUtils.Chrome(mine=True,silent=True)
    for i in baijiahao.l:
        page.get(i)
        page.save(path=f'{MyUtils.userpath("Pictures/集锦/其它/")}')
        pout.add(i)
    page.quit()


    baijiahao=MyUtils.rtxt(MyUtils.projectpath('./browser/baijiahao.txt'))