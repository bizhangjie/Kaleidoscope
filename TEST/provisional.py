# 修复allpie,长度过长行直接删
import MyUtils
f=MyUtils.txt(MyUtils.projectpath('./抖音/Allpieces.txt'))
l=f.l
d=[]
for i in l:
    if MyUtils.jsontodict(i)==False:
        d.append(i)
f.l=[i for i in l if not i in d]
f.save()