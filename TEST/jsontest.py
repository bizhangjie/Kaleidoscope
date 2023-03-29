import MyUtils

js = MyUtils.jsondata('savepage')
js.setdata({
    'baijiahao':{
        'dir': '百家号',
        'cuttop': 90,
        'cutright':490,
    },

})

print(js.get('savepage'))
