import time

import MyUtils


def fun():
    pass


def main():
    fun()


if __name__ == '__main__':
    url='https://mil.sohu.com/a/541435402_121000286'
    # page=MyUtils.Chrome(url,silent=True,mine=True)
    page=MyUtils.Chrome(url,silent=True,mine=False)
    page.save(minsize=False,)