import MyUtils
url='https://v26-web.douyinvod.com/fe924f608eb2c314774c81dd3c1824b5/641d3617/video/tos/cn/tos-cn-ve-15/o8nHAFbnDQdF93jAMJ5yrwjSBBPA1DSfegDiog/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1621&bt=1621&cs=0&ds=3&ft=TgqJHhM3UUmfBbdag02D1YmAo6kItG5pEvq9eFaIOyQO12nz&mime_type=video_mp4&qs=0&rc=aGY5OTQ1NmU2NDs0NGRoZ0BpamtlM2g6ZjtsaTMzNGkzM0AwNGMuXy5gNjMxLzRhYWExYSNwa3BncjRnNi1gLS1kLTBzcw%3D%3D&l=20230324123300D77F62BFA10F8F03318F&btag=8000'

if __name__ == '__main__':
    page = MyUtils.Chrome(url, silent=False,mine=False, mute=True)
    MyUtils.sleep(10)
    page.quit()