import MyUtils


def main():
    s1=r'_\d+$'
    s2='basic_0'
    p,_=(MyUtils.research(s1,s2))
    print(p)

if __name__ == '__main__':
    main()
