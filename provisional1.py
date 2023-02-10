import MyUtils
MyUtils.setrootpath(dname=[-1])

@MyUtils.consume
@MyUtils.listed
def test(*a,**b):
    page=MyUtils.Chrome()
    print(a,b)
test([1,2,3],b=2)