import MyUtils
import BUtils
count=0
for i in MyUtils.listdir('./bili'):
    useruid=MyUtils.gettail(i,'_')
    author=BUtils.uidtoid(useruid)
    for j in MyUtils.listdir(i):
        bvid=MyUtils.gettail(j,'_')
        video=BUtils.video(bvid)

        count+=1