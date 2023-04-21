import pyperclip

import MyUtils

root = MyUtils.projectpath('self/记录 语录 随笔 随想')

def main():
    # 初始化
    interval = 0
    fcount = MyUtils.txt(root + '/count.txt')
    fcache = MyUtils.txt(root + '/cache.txt')
    while True:
        # 先获取总数·
        count = int((fcount.l)[0])

        # 找到对应存储文件
        hun = count // 100
        sname = f'/{hun * 100 + 1}-{hun * 100 + 100}.txt'
        frecord = MyUtils.txt(root + sname)
        pyperclip.copy(frecord.path)

        # 进行增加
        c = ''
        cc = ''
        while not cc[-2:] in ['FE', 'FE', 'ef', 'fe']:
            cc = input('请输入文案，以末尾的FE作为结束：')
            ccc = cc.strip('FE').strip('EF').strip('fe').strip('ef')
            c += '\n' + cc
            if not ccc == cc:
                break
            MyUtils.sleep(interval)
        c = c.strip('FE').strip('EF').strip('fe').strip('ef')
        c = c.replace('\n', '\n\t')
        c = c + '\n'
        if c == c.strip('TEST'):
            frecord.add(MyUtils.nowstr() + str(c))
            count += 1
            fcount.clear()
            fcount.add(count)
            fcount.save()
        MyUtils.log(f'[第{count}条]{MyUtils.nowstr()} 已保存。现在你可以在{frecord.path}查看。')
    MyUtils.delog('Quitting Anote ....')

def calculateOverall():
    fall=MyUtils.txt(root+'/all.txt')
    for i in MyUtils.listfile(root):
        i=MyUtils.filename(i)
        if '-'in i and '.txt' in i:
            f=MyUtils.txt(root+'/'+i)
            fall.l+=f.l
        fall.save()

    MyUtils.look(fall.path)

if __name__ == '__main__':
    main()
    # calculateOverall()
