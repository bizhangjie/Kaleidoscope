import shutil

import MyUtils
# windows新版很傻逼。通过脚本创建的文件夹，末尾如果带上空格，全都不能操作。
# 现在把里面的全部拯救出来，copy 出来
path=r'C:\Users\17371\Pictures\集锦\其它'
path=MyUtils.standarlizedPath(path)
tar=f'{MyUtils.parentpath(path)}/新建文件夹/'
MyUtils.createpath(tar)
for i in MyUtils.listdir(path):
#     复制文件和文件夹
    shutil.copytree(i+' ',tar+MyUtils.filename(i))
# 然后手动重命名path 并且命令行rmdir /s删除删除整个父文件夹
