# 导入 csv 库
import MyUtils

r=MyUtils.table('database/sample.csv')
print(r.l)
print(r.d)
r.add((0,0,0))