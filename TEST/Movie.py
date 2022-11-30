import MyUtils
import moviepy

if __name__ == "__main__":
    moviepy.editor .VideoFileClip(MyUtils.desktoppath('sample.mp4')).audio.write_audiofile(MyUtils.desktoppath('sample.mp3'))

