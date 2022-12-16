import MyUtils

def Douyin():
    ans=[]
    f=MyUtils.txt(MyUtils.projectpath('./抖音/AllPieces.txt'))
    for i in f.l:
        title=MyUtils.jsontodict(i)
        title=MyUtils.value(title)[0]['title']
        for j in ('啊','呢','是','呀','吗','吧','对','你'):
            if j in title:
                ans.append(title)
    ans=list(set(ans))
    MyUtils.out(ans)
Douyin()
