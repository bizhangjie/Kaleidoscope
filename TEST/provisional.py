import MyUtils
import BUtils
count=0
for i in MyUtils.listdir('./bili'):
    if '收藏'in i or 'cache'in i:
        continue
    useruid=MyUtils.gettail(i,'_')
    author=BUtils.uidtoid(useruid)
    for j in MyUtils.listdir(i):
        MyUtils.copyto(f'trying {j}')
        bvid=MyUtils.gettail(j,'_')
        video=BUtils.video(bvid)
        if video.exist==False:
            MyUtils.move(j,MyUtils.projectpath(f'./bili/疑似绝版/{MyUtils.filename(j)}'))
            continue
        if not author in video.authors:
            MyUtils.Open(j)
            MyUtils.Exit(author,video.authors,j)
        title=MyUtils.standarlizedFileName(video.title)
        MyUtils.pout(f'{j}\n./newbili/{author}_{useruid}/{title}_{bvid}')
        MyUtils.move(j,f'./newbili/{author}_{useruid}/{title}_{bvid}')
        count+=1
        # if count>=50:
        #     MyUtils.Exit()