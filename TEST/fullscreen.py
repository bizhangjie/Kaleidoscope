import MyUtils
url='https://www.cc98.org/topic/5528435'
if __name__ == '__main__':
    page=MyUtils.Chrome(url,mine=True,silent=False)
    # page.extendtofull()
    page.fullscreen(
        path=MyUtils.cachepath('fullscreen/test.png'),
       top=30,bottom=0,clip=True)
    page.quit()
