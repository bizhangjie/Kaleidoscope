import MyUtils
root=r'D:\Kaleidoscope\browser\calender'
# for i in range(1,32):
for i in range(10,32):
        MyUtils.delog(f'正在处理{i}号')
        MyUtils.click(f'{root}/{i}.png')
        MyUtils.sleep(1)