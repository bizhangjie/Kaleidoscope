import MyUtils

url ='https://v26-web.douyinvod.com/5c4b37728f7ad52505df73a785168435/63c40b71/video/tos/cn/tos-cn-ve-15/oQuABhHzglCBKwpfN9xeAQAOIODJO4Uid4JnsN/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1339&bt=1339&cs=0&ds=3&ft=bvTKJbQQqUWXf_4ZDo0OqY8hFgpiwRhS~jKJQk9cv.0P3-A&mime_type=video_mp4&qs=0&rc=aWZkMzpnNGQ7ODw8ZmkzZEBpajhkNWg6ZnZ1aTMzNGkzM0AwLWNiYS0vXi8xY140MmA1YSMwZzY0cjQwZC5gLS1kLWFzcw%3D%3D&l=20230115211910780E033A813BB0EA4676&btag=10000'
# path = MyUtils.cachepath('pagedownload.png')
path = MyUtils.cachepath('pagedownload')
# path = MyUtils.cachepath('pagedownload.mp4')
MyUtils.pagedownload(url, path,t=7,silent=False)
