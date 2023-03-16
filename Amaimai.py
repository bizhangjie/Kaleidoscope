import MyUtils


def main():
    url='https://maimai.cn/web/gossip_detail?gid=31615342&egid=4a1d3403d7774a098eac58e683f64d0a&encode_id=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlZ2lkIjoiNGExZDM0MDNkNzc3NGEwOThlYWM1OGU2ODNmNjRkMGEiLCJpZCI6MzE2MTUzNDIsInUiOjIzNTQ1ODI4N30.PJaku8Lx07qvCdVf_yGgb0x1VwvgwRbsmWRnM9cBQ58&from=list'
    page=MyUtils.Chrome(url,mine=False,silent=False)
    savepath=MyUtils.collectionpath('脉脉/')
    page.save(savepath,top=120,bottom=100,titletail='- 脉脉',adjust=54)

if __name__ == '__main__':
    main()
