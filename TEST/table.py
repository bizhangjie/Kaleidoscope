# 导入 csv 库
import MyUtils

r=MyUtils.table(MyUtils.desktoppath('sample.csv'),init=[1,2,3])
print(r.l)
print(r.d)
r.add((0,0,0))
r.add((1,1,1))