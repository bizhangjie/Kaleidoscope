import MyUtils

# jso = MyUtils.Json(MyUtils.DesktopPath('ab.txt'))
# jso=MyUtils.RefreshJson(MyUtils.DesktopPath('ab.txt'))
# print(jso.get())

import json

# JSON字符串转换成Python对象
json_str = '{"name": "John", "age": 30}'
python_obj = json.loads(json_str)
print(python_obj)
# Output: {"name": "John", "age": 30}

# Python对象转换成JSON字符串
python_obj = {"name": "John", "age": 30}
json_str = json.dumps(python_obj)
print(json_str)
# Output: {"name": "John", "age": 30}

# 从文件中读取JSON数据
with open(MyUtils.projectpath("data.json"), "r") as file:
    python_obj = json.load(file)
    print(python_obj)

# 将Python对象写入文件
python_obj = {"name": "John", "age": [30,31]}
with open(MyUtils.projectpath("data.json"), "w") as file:
    json.dump(python_obj, file)
