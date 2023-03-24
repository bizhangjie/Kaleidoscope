import MyUtils
url='https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=vue%20create&oq=npm%2520%25E8%25BF%2590%25E8%25A1%258C&rsv_pq=be31e47500000107&rsv_t=24bcFZui4WK%2Bz1RNiVPW4QBWpGhncTntpOTnL%2BpTNSafrq143dX8ihM4T08&rqlang=cn&rsv_enter=1&rsv_dl=tb&rsv_sug3=13&rsv_sug1=17&rsv_sug7=100&bs=npm%20%E8%BF%90%E8%A1%8C'
if __name__ == '__main__':
    page=MyUtils.Chrome(url,mine=False,silent=False)
    # page.extendtofull()
    page.fullscreen(
        path=MyUtils.cachepath('fullscreen/test'),
       cutright=250,cuttop=100,clip=True)
    page.quit()
