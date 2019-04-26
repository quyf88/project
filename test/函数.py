# -*- coding: utf-8 -*-
# @Time    : 2019/4/20 9:31
# @Author  : Mat
# @Software: PyCharm

"""
定义函数 ： def
数据排序： sorted()   正向排序 适用于所有可迭代对象 返回一个新的可迭代对象 对原数据没有影响
         sort()     正向排序 仅适用于list 在原数据基础上修改 效率比sorted高
         reverse    默认参数 False 正向排序  True 反向排序 默认值False
"""


def func(a, b=1):
    if b == 1:
        return sorted(a)  # 正向排序
    else:
        return sorted(a, reverse=True)  # 反向排序


a = [3, 5, 6, 1, 4, 2]
# print(func(a)) # 输出正向排序
# print(func(a, 2)) # 输出反向排序
list1 = func(a)
list2 = func(a, 2)
list3 = list(zip(list1, list2))
print(list3)
