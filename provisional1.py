import MyUtils

signal='【NaNa】'
target='./newbili/小份夹心呐呐酱w_115065744/'
MyUtils.setrootpath('e')

for i in MyUtils.listdir(MyUtils.projectpath('./bili/疑似绝版')):
    if signal in i:
        fname=MyUtils.filename(i)
        MyUtils.move(i,target+'/'+fname,silent=False)