import MyUtils
url='https://new.qq.com/rain/a/20220519A0AFYF00'
if __name__ == '__main__':
    page=MyUtils.Chrome(url,mine=False,silent=False)
    # page.extendtofull()
    page.fullscreen(
        path=MyUtils.cachepath('fullscreen/test'),
       cutright=220,cuttop=0,clip=True,clipinterval=2)
    page.quit()
