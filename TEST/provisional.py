import MyUtils
import BUtils
count=0
for i in MyUtils.listdir('./bili'):
    useruid=MyUtils.gettail(i,'_')
    author=BUtils.uidtoid(useruid)
    for j in MyUtils.listdir(i):
        bvid=MyUtils.gettail(j,'_')
        video=BUtils.video(bvid)
        if not author in video.authors:
            MyUtils.Open(j)
            MyUtils.Exit(author,video.authors,j)
        title=MyUtils.standarlizedFileName(video.title)
        MyUtils.pout(j)
        MyUtils.pout(f'./newbili/{author}_{useruid}/{title}_{bvid}')
        MyUtils.move(j,f'./newbili/{author}_{useruid}/{title}_{bvid}')
        count+=1
        # if count>=50:
        #     MyUtils.Exit()