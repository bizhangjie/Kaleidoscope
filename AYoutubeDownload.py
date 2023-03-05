import MyUtils
import youtube_dl

import youtube_dl

url = 'https://www.bilibili.com/video/BV1qE411c7yk'

ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
    'outtmpl': '%(title)s.%(ext)s',
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

