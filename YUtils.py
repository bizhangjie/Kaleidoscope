import MyUtils

# num示例：
(len('2k-cD0Yoohs'))

readytodownload = MyUtils.cache('D:/Kaleidoscope/youtube/readytodownload.txt')

def turntodownloader():
    MyUtils.hotkey('alt','tab')

def quitdownloade():
    MyUtils.hotkey('alt','tab')

def download(uid):
    MyUtils.copyto(uid)
    MyUtils.click(406,268)
