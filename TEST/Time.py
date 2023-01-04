import MyUtils


MyUtils.delog(MyUtils.now())
MyUtils.delog(MyUtils.nowstr())
MyUtils.delog('-------------')
Time=MyUtils.Time()
MyUtils.delog(MyUtils.today())
MyUtils.delog(MyUtils.realtime())
MyUtils.delog(Time)
MyUtils.delog(Time.time())
MyUtils.delog(Time.today())
MyUtils.delog(Time.yesterday())
MyUtils.delog('-------------')

MyUtils.delog(MyUtils.Time('2022-12-14'))
MyUtils.delog(MyUtils.Time('2022-12-14').istime('这是一串乱码'))
MyUtils.delog(MyUtils.Time('22:05'))
MyUtils.delog(MyUtils.Time('22:05:01'))
MyUtils.delog(MyUtils.Time('22:05:01.123456').mic())
MyUtils.delog(MyUtils.Time('2023-01-01').counttime(MyUtils.Time()))