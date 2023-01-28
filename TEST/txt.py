import MyUtils

a = MyUtils.txt(MyUtils.cachepath('provisional.md'))
a.add(4)
a.add(5)
a.add(6)
print(a.l)
a.set()
a.delete(['1','2','3'])
print(a.l)