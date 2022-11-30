import MyUtils
import YUtils


if __name__ == '__main__':
    YUtils.turntodownloader()
    f=MyUtils.rtxt(MyUtils.projectpath('./browser/youtube.txt'))

    # 提取一个url
    def geturl():
        s='https://www.youtube.com/watch?v='
        for i in f.l:
            if not s in i:
                continue
            # uid=MyUtils.gettail(i,s)
            print(i)
            MyUtils.copyto(i)
            return(i)
    geturl()

    # 等待人工下载

    # 下载完毕，删除记录，移动文件
    def done(i):
        f.delete(i)
        for i in MyUtils.listfile(r'C:\Users\17371\Videos\TubeGet'):
            if '.mp4'in i:
                name=MyUtils.removetail(i,'.mp4')
        for i in MyUtils.listfile(r'C:\Users\17371\Videos\TubeGet'):
            MyUtils.move(i,f'./youtube/{name}/{MyUtils.filename(i)}')

    # done()

