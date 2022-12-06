import time

import MyUtils


def fun():
    pass


def main():
    fun()


if __name__ == '__main__':
    url='https://www.bilibili.com/read/cv5697599?spm_id_from=333.999.0.0'
    page=MyUtils.Chrome(url,silent=True,mine=True)
    page.save(f'./bili/article/{page.title()}')