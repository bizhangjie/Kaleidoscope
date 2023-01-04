import MyUtils


def main():
    url='https://tg.602.com/bscq/2001/index.html?uid=360xxl-06&suid=01&sourceid=Z05FZpOhk060'
    page=MyUtils.Chrome(url,silent=True)
    page.savevideos(MyUtils.userpath('Pictures'))


if __name__ == '__main__':
    main()
