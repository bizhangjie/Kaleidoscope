import MyUtils

class a:
    @MyUtils.useState
    def main(self,a,b=0,c=0):
        print(a,b,c)

if __name__ == '__main__':
    ca=a()
    ca.main(a=0,b=1,c=3)
    ca.main(a=0)
    ca.main(a=0,c=3)
    ca.main(a=0,b=1)
    ca.main(b=1,c=3)
    ca.main(0,1,2)
