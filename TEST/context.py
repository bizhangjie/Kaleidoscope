import MyUtils


def fun():
    def fun1():
        def fun2():
            d=(MyUtils.context(6))
            MyUtils.out(d)
        fun2()
    fun1()


if __name__ == '__main__':
    fun()
