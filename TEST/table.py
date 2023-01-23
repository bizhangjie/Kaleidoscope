# 导入 csv 库
import MyUtils

# r=MyUtils.table(MyUtils.projectpath('database/sample.csv'), title=["C1","C2","C3","C4"])
r=MyUtils.table(MyUtils.projectpath('database/sample.csv'))
print(r.l)
print(r.d)
r.add((0,0,0))
r.add((1,1,1))