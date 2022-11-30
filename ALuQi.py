import MyUtils

# 规整移动的文件
todolist=[]
# 先预报，人工检查看看对不对
for file in MyUtils.listfile(['./', './璐琪/']):
    if 'Scree' in file or 'SVID' in file:
        filename = MyUtils.filename(file)
        if 'SVID' in filename:
            year, month, day = filename[5:9], filename[9:11], filename[11:13]
        if 'Scre' in filename:
            year, month, day = filename[15:19], filename[20:22], filename[23:25]
        targetdir=f'./璐琪/{year}-{month}-{day}/'
        if not MyUtils.isfile(targetdir + filename):
            todolist.append((file, targetdir+filename))

MyUtils.out(todolist)
#  执行并添加记录
for i in todolist:
    MyUtils.move(i[0],i[1])
    record=MyUtils.rjson(MyUtils.projectpath('./璐琪/record.txt'))
    record.add({MyUtils.filename(i[0]):MyUtils.diskname})
    print({MyUtils.filename(i[0]):MyUtils.diskname})
