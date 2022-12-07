import MyUtils

if __name__ == '__main__':
    f=MyUtils.txt(MyUtils.projectpath('./browser/bili.txt'))
    MyUtils.openedge(f.l[:10])