import MyUtils
global last
last=1.5

last*=3600
sleeptime=90
def main():
    while True:
        stime=MyUtils.Time().s()
        fname=f'{stime}.png'
        fname=MyUtils.standarlizedFileName(fname)
        MyUtils.get_screen((MyUtils.selfpath(f'/屏幕监测/{MyUtils.Now().today()}/{fname}')))

        MyUtils.sleep(sleeptime)
        last-=sleeptime
        if last<=0:
            break

if __name__ == '__main__':
    main()
