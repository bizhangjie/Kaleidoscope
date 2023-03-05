import MyUtils

url ='https://www.baidu.com/img/pcdoodle_2a77789e1a67227122be09c5be16fe46.png'
path = MyUtils.cachepath('pagedownload/test/1.png')
# MyUtils.pagedownload(url, path,t=7,silent=False)
# MyUtils.pagedownload(url, path,t=7,silent=False,overwrite=True)
# MyUtils.pagedownload(url, path,t=7,silent=False,redownload=True)
MyUtils.pagedownload(url, path,t=7,silent=True,redownload=True,overwrite=True)
MyUtils.Open(MyUtils.parentpath(path))
