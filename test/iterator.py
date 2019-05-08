# -*- coding: utf-8 -*-
# @Time    : 2019/5/8 10:00
# @Author  : project
# @File    : iterator.py
# @Software: PyCharm


from test.builder import builder

iter = builder(10)

for i in iter:
    print(i)
