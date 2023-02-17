import MyUtils
commission='latest -WYJ'

if __name__ == '__main__':
    # 持续推送到github
    b = True
    while True:
        f = MyUtils.txt(MyUtils.projectpath('txt.txt'))
        if b:
            f.add(' ')
        else:
            f.l = f.l[:-1]
            f.save()
        b = not b
        MyUtils.delog(b)
        push=r"git push main origin:main"
        push=r"git push"
        MyUtils.CMD(f'cd d:;cd {MyUtils.projectpath()};git add .;git commit -m "{commission}";'+push, silent=True)
        MyUtils.log('已提交并推送。')
        while not MyUtils.now().time().hour in list(range(10, 24)):
            MyUtils.sleep(60 * 5)
        MyUtils.sleep(5 * 60)
