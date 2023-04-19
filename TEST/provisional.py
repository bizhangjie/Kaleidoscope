# 修复allpie,长度过长行直接删
import MyUtils
f=MyUtils.txt(MyUtils.projectpath('./抖音/Allpieces.txt'))
l=f.l
for i in l:
    if i.count('"video')+i.count('"pic')>1:
        f.delete(i)
        print(i)