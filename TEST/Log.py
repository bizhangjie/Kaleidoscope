import MyUtils

a = (1, 2)
MyUtils.delog([1, 2, *a])
MyUtils.log([1, 2, *a])
MyUtils.warn([*a])
MyUtils.tip([*a])
# 生成一个很长的字符串
s=''
for i in range(999):
    s+=f'{i}'
MyUtils.delog(s)
# print(f'\033[5;30m ')