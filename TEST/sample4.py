class a():
    def __init__(self,silent=None):
        self.silent=silent
        print('a已构造')
    def checksilent(self,silent=None):
        if silent is None:
            silent=self.silent
        print('silent:',silent)

class b(a):
    def __init__(self,silent=None):
        a.__init__(self,silent=silent)
        print('b已构造')

class c(a):
    def __init__(self,silent=None):
        a.__init__(self,silent=silent)
        print('c已构造')

class d(b,c):
    def __init__(self,silent=self.silent):
        # b.__init__(self,silent=silent)
        # c.__init__(self,silent=silent)
        super().__init__(silent=silent)
        print('d已构造')


d()