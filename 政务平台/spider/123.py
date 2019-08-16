# -*- coding: utf-8 -*-
# @Time    : 2019/8/16 11:49
# @Author  : project
# @File    : 123.py
# @Software: PyCharm


import os

path = os.getcwd()
files = os.listdir(path)
files = [i for i in files if '.xlsx' in i]
print(files)

for i in files:
    filename = i
    print(filename)