# -*- coding:utf-8 -*-
# 文件 ：数据去重.py
# IED ：PyCharm
# 时间 ：2019/11/5 0005 13:23
# 版本 ：V1.0
import os
import datetime

filename = '微信号/' + (datetime.datetime.now()+datetime.timedelta(days=-1)).strftime('%Y-%m-%d') + '.txt'

# 获取当前目录
path = os.getcwd()
print(path)
# 返回指定目录下所有文件
files = os.listdir(path + r'/微信号/')
# 筛选指定文件
files = [i for i in files if filename not in i]

text = []
new_text = open(filename, 'r')
new_text = list(set([i.replace('\n', '') for i in new_text]))
# print(new_text)
for file in files:
    n_text = open(filename, 'r')
    i = [i.replace('\n', '') for i in n_text.readlines()]
    text += i

with open(filename, 'w') as f:
    f.seek(0)
    f.truncate()

for p in new_text:
    if p not in text:
        continue
    with open(filename, 'a+') as f:
        f.write(p)
        f.write('\n')
print('数据清洗完成!')


