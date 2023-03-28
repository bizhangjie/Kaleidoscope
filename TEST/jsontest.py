import  MyUtils
js=MyUtils.jsondata(MyUtils.projectpath('data.json'))
js.add({'a':1,'b':2})
js.remove('a')
print(js.get('b'))

