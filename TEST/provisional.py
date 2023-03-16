# 清除抖音操作盘外部的散乱下载文件
# 先查找不重复的
import MyUtils
import DouyinUtils

for i in MyUtils.listfile('./抖音'):
    if not '.mp4 'in i:
        continue
    fname=MyUtils.filename(i)
    vnum=MyUtils.rmtail(i,'_')
    useruid,author=MyUtils.pieceto