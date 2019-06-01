# coding=utf-8
# 作者    ： Administrator
# 文件    ：json_modo.py
# IED    ：PyCharm
# 创建时间 ：2019/6/1 12:32
"""
data = { 'name': '诚实可靠小郎君', "age": 18, "feature" : ["高", "富", "帅"] }
在程序中将这个字典转化为json并存入文件内，然后再从这个文件中读取出‘帅’这个字符打印出来
"""
import json

data = {'name': '诚实可靠小郎君', "age": 18, "feature": ["高", "富", "帅"]}

with open('json_modo.txt', 'w+', encoding='utf-8') as f:
    res_json = json.dumps(data, ensure_ascii=False)
    f.write(res_json)
    f.seek(0)
    res_dict = json.loads(f.read())
    print(res_dict['feature'][2])


