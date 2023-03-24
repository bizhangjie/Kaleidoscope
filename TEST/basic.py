if 0:
    print(1)
为什么变量名竟然支持中文呢='离谱'
print(为什么变量名竟然支持中文呢)
filelist = [1,2,3]

if len(filelist) > 0:
    first = filelist.pop(0)
    print(first, filelist)
else:
    print('List is empty')