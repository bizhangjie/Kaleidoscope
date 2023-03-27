import MyUtils
url='https://mp.weixin.qq.com/s/ftN4kg6pnUEgK5DmH2Qv-g'
if __name__ == '__main__':
    page=MyUtils.Chrome(url,mine=False,silent=False)
    # page.extendtofull()
    page.fullscreen(
        path=MyUtils.cachepath('fullscreen/test'),
       cutright=220,cuttop=0,clip=True,clipinterval=2)
    page.quit()
