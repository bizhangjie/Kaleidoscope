import MyUtils
# from translate import Translator
# translator= Translator(to_lang="chinese")#指定要翻译成的语言

def main():
    # for j in MyUtils.listfile(r'C:\Users\17371\Desktop\毕设\林杰老师的论文'):
        # if not '.md' or '2Chinese_'in j:
        #     continue
        j=(r'C:\Users\17371\Desktop\毕设\林杰老师\林杰老师浙江大学个人主页.md')
        n=MyUtils.extentionandname(MyUtils.filename(j),exist=False)[0]
        fname=(MyUtils.parentpath(j)+'/2Chinese_'+n+'.md')
        # if MyUtils.isfile(fname):
        #     continue
        fout=MyUtils.txt(fname)
        f=MyUtils.txt(j)
        for i in f.l:
            if len(i)>2:
                fout.l.append(i)
            res=(MyUtils.translate(i,limit=10))
            if not res=='':
                fout.l.append('```\n'+res+'\n```')
        fout.save()

if __name__ == '__main__':
    main()
