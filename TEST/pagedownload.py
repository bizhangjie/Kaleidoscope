import MyUtils

url ='https://v26-web.douyinvod.com/9bdfb7d48a976c4b525341a1a03fa003/640f0ba8/video/tos/cn/tos-cn-ve-15c001-alinc2/o4bDfBxRI0VBGpoCeSbnbBv7RFA8QJfACPqHUd/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1932&bt=1932&cs=0&ds=4&ft=GN7rKGVVywhiRF_80mo~ySqTeaAp9RsR6vrKFadHNdo0g3&mime_type=video_mp4&qs=0&rc=ODtpZTlpZTQ2ZTNpNTZmOEBpanh5azg6Zmt5aTMzNGkzM0BhYi5gMjJeNi4xMTYxXl5gYSNrZW9icjRfNTVgLS1kLTBzcw%3D%3D&l=2023031318401550A46E121EFBDC0A5668&btag=8000'
path = MyUtils.cachepath('pagedownload/test/1.mp4')
# MyUtils.pagedownload(url, path,t=7,silent=False)
# MyUtils.pagedownload(url, path,t=7,silent=False,overwrite=True)
# MyUtils.pagedownload(url, path,t=7,silent=False,redownload=True)
MyUtils.pagedownload(url, path,t=7,silent=True,redownload=True,overwrite=True)
MyUtils.Open(MyUtils.parentpath(path))
