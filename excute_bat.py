import MyUtils
fname=MyUtils.projectpath('screenshots')

string=f'''@echo off\n
python3 {fname}.py\n
pause
'''

# 创建bat文件
ftxt=MyUtils.txt(fname+'.bat')
ftxt.add(string)

# 创建 bat 文件快捷方式
