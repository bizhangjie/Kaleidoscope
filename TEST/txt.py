import MyUtils

a = MyUtils.txt(MyUtils.desktoppath('txtpy.txt'))
print(a.l)
a.set()
a.delete(['1','2','3'])
print(a.l)