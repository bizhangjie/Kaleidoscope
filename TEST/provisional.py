import MyUtils
f=MyUtils.txt(MyUtils.projectpath('./抖音/AllPieces.txt'))
l1=[]
l2=[]
for i in f.l:
    newi=i.replace('{"disk": -2','{"disk": "-2"')
    l2.append(newi)
f.l=l2
f.save()