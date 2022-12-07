import time

import MyUtils


def fun():
    pass


def main():
    fun()


if __name__ == '__main__':
    url='https://mil.sohu.com/a/541435402_121000286'
    # url='https://pc.yiyouliao.com/msn/article.html?recId=9cea2cf5acc442a399106708789ad5e6_s&infoId=II008LO68G11JQD'
    # page=MyUtils.Chrome(url,silent=True,mine=True)
    page=MyUtils.Chrome(url,silent=True,mine=False)
    # page.set_window_size(1200,3000)
    page.save(minsize=(300,300),scale=200,autodown=True)