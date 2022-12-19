import time

import MyUtils


def fun():
    pass


def main():
    fun()


if __name__ == '__main__':
    # 持续推送到github
    while True:
        b=True
        f=MyUtils.txt(MyUtils.projectpath('txt.txt'))
        if b:
            f.add(' ')
        else:
            f.l=f.l[:-1]
            f.save()
        b=not b
        MyUtils.CMD(f'cd d:;cd {MyUtils.projectpath()};git add .;git commit -m "latest -WYJ";git push',silent=True)
        MyUtils.log('已提交并推送。')
        while not MyUtils.now().time().hour in list(range(10,24)):
            time.sleep(60*5)
        time.sleep(5*60)