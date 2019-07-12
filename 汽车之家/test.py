# -*- coding: utf-8 -*-
# @Time    : 2019/7/8 14:31
# @Author  : project
# @File    : test.py
# @Software: PyCharm

# #!/usr/bin/env python3
# import asyncio
#
# async def func_normal():
#
#     return 'saad'
#
# async def fun():
#     return 1
#
# loop = asyncio.get_event_loop()
# tasks = [func_normal(), fun()]
# results = loop.run_until_complete(asyncio.gather(*tasks))
# print("func_normal()={}{}".format(*results))
# loop.close()
import re

# a = ['\r\n                                                ', '驻车制动类型', '\r\n                                                ', '电子驻车', '\r\n                                        ', '前轮胎规格', '\r\n                                        ', '225/50 R17', '\r\n                                        ']
#
# for i in a:
#     pattern = re.compile(r'\s|\n|<br>', re.S)
#     # 将匹配到的内容用空替换，即可以达到去除无关内容只留下文本的目的
#     content = pattern.sub('', i)
#     if content:
#         print(len(content), content)

a = '''
'''


# b = re.findall(r'<th>驻车制动类型</th>(.*?)</td>', a, re.S | re.M)[0]
# pattern = re.compile(r'\s|\n|<td>', re.S)
# c = pattern.sub('', b)
# d = re.findall(r'<th>前轮胎规格</th>(.*?)</td>', a, re.S | re.M)[0]
# pattern = re.compile(r'\s|\n|<td>', re.S)
# e = pattern.sub('', d)
#
# a = 'var hq_str_sh600039="四川路桥,3.550,3.540,3.530,3.570,3.530,3.530,3.540,9728967,34527976.000,548800,3.530,327300,3.520,291000,3.510,282900,3.500,45100,3.490,137600,3.540,417400,3.550,696100,3.560,538700,3.570,522000,3.580,2019-07-11,15:00:00,00";'
# b = 'var hq_str_sh600024="";'
#
# print(len(b.split('=')[1]))
a = 'asdfg'
print(int(len(a)))
for i in range(5):

    print(i)