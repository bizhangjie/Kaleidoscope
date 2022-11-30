import MyUtils
for i in MyUtils.listdir('./bili'):
    if []==MyUtils.listdir(i):
        print(i)
        MyUtils.deletedirandfile(i)