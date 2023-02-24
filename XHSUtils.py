import MyUtils

# 文件定义
allusers = MyUtils.RefreshJson('D:/Kaleidoscope/抖音/AllUsers.txt')
# specialusers = MyUtils.RefreshJson('D:/Kaleidoscope/抖音/SpecialUsers.txt')
allpieces = MyUtils.RefreshJson('D:/Kaleidoscope/小红书/AllPieces.txt')

readytodownload = MyUtils.cache('D:/Kaleidoscope/小红书/ReadytoDownload.txt',silent=MyUtils.debug)
exceptuser = MyUtils.txt('D:/Kaleidoscope/小红书/FailedUsers.txt')
failed = MyUtils.Json('D:/Kaleidoscope/小红书/FailedPieces.txt')
missing = MyUtils.rjson('D:/Kaleidoscope/小红书/Missing.txt')
expirepiecex=MyUtils.rjson(MyUtils.projectpath('./小红书/ExpiredPieces.txt'))
allusers=MyUtils.txt(MyUtils.projectpath('小红书/AllUsers.txt'))

def main():
    pass

if __name__ == '__main__':
    main()
