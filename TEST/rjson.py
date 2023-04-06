import MyUtils

f = MyUtils.rjson(MyUtils.cachepath('b'),silent=True)
while True:
    # MyUtils.sleep(5)
    print(f.get())

