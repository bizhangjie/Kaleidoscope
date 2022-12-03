import MyUtils
ta=MyUtils.Csv(MyUtils.projectpath('抖音/Missing.csv'),create=['uid','disk','author','title'])
for i in MyUtils.rtxt(MyUtils.projectpath('./抖音/Missing.txt')).l:
    d=MyUtils.jsontodict(i)
    uid,d=MyUtils.key(d),MyUtils.value(d)
    for d in d:
        d.update({"uid":uid})
        ta.add(d)
    # break
#     ta.add((i,))
