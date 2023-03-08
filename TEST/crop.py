import MyUtils


def main():
    # MyUtils.combineimages(filelist=[MyUtils.cachepath('fullscreen/clipped/basic17.png'),
    #                                 MyUtils.cachepath('fullscreen/clipped/basic16.png')],
    #                       bottom=87,top=54,outputpath=MyUtils.cachepath('fullscreen/basic.png'))
    MyUtils.combineimages(inputpath=MyUtils.cachepath('fullscreen/clipped'),bottom=73,top=52,reverse=True)
if __name__ == '__main__':
    main()
