import MyUtils


def main():
    targetpath=MyUtils.cachepath('/')
    def issame(newname,targetpath):
        if MyUtils.isfile(targetpath+newname):
            f=MyUtils.txt(targetpath+newname)
            MyUtils.delog(f.path)
            if f.l[0]in['内容3']:
                return True
        return False
    print(MyUtils.regeneratename('origin.txt',targetpath,issame=issame))

if __name__ == '__main__':
    main()
