import MyUtils
# 遍历'D:\Kaleidoscope\self\MANUAL 文档 收藏 AUTO\网页集锦\其它\饱受争议的GitHub Copilot 神操作：自动补全补出了B站CEO的身份证！ - 脉脉\img文件夹并全部根据路径用MyUtils.img方法初始化
for i in MyUtils.listfile('D:\Kaleidoscope\self\MANUAL 文档 收藏 AUTO\网页集锦\其它\饱受争议的GitHub Copilot 神操作：自动补全补出了B站CEO的身份证！ - 脉脉\img'):
    p=MyUtils.img(i)
    MyUtils.delog(i)

