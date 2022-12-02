import BUtils
import MyUtils

VideoSpectrum = BUtils.videospectrum
readytodownload = BUtils.readytodownload \
    # 一个作者一次最多下载的个数
MAX = 799
BUtils.opendownloader()


def main():
    count=0
    while count<5:
        count+=1
        d = readytodownload.get()
        useruid = MyUtils.key(d)
        author = BUtils.uidtoid(useruid)
        vlist = MyUtils.value(d)
        # 使用下载器下载
        for bvid in vlist[:MAX]:
            BUtils.download(bvid, author, useruid)
        BUtils.move(useruid)


if __name__ == '__main__':
    main()
