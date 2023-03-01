import MyUtils

url ='https://user-images.githubusercontent.com/3739368/103435721-e601c300-4c4d-11eb-800e-b420a55f0680.JPG'
path = MyUtils.cachepath('pagedownload/test/1.png')
# MyUtils.pagedownload(url, path,t=7,silent=False)
# MyUtils.pagedownload(url, path,t=7,silent=False,overwrite=True)
# MyUtils.pagedownload(url, path,t=7,silent=False,redownload=True)
MyUtils.pagedownload(url, path,t=7,silent=False,redownload=True,overwrite=True)

