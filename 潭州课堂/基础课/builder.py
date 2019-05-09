# -*- coding: utf-8 -*-
# @Time    : 2019/5/8 9:54
# @Author  : project
# @File    : builder.py
# @Software: PyCharm


def builder(max):
    a, b = 0, 1
    while max > 0:
        a, b = b, a+b
        max -= 1
        yield a
