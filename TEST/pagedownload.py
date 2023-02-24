import MyUtils

url ='https://www.baidu.com/img/PCfb_5bf082d29588c07f842ccde3f97243ea.png'
path = MyUtils.cachepath('pagedownload/test/1.png')
# MyUtils.pagedownload(url, path,t=7,silent=False)
# MyUtils.pagedownload(url, path,t=7,silent=False,overwrite=True)
# MyUtils.pagedownload(url, path,t=7,silent=False,redownload=True)
MyUtils.pagedownload(url, path,t=7,silent=True,redownload=True,overwrite=True)
