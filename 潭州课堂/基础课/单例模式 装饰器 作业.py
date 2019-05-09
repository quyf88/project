# coding=utf-8
# 作者    ： Administrator
# 文件    ：单例模式 装饰器 作业.py
# IED    ：PyCharm
# 创建时间 ：2019/4/27 16:24


# class SingletonMode:
#     """单例模式"""
#     _instance = None
#
#     def __new__(cls, *args, **kwargs):
#         if cls._instance == None:
#             cls._instance = object.__new__(cls)
#             return cls._instance
#         else:
#             return cls._instance
#
#
# s = SingletonMode()
# d = SingletonMode()
# print(id(s))
# print(id(d))


# class Decorator:
#     """内置装饰器"""
#     def __init__(self, above, below):
#         self.above = above
#         self.below = below
#
#     @property  # 实现类方法的直接调用
#     def poetry(self):
#         content = self.above + self.below
#         return content
#
#     @staticmethod  # 静态方法 实现类属性的直接调用 与实例解绑
#     def static_method():
#         content = above + below
#         return content
#
#     @classmethod  # 类装饰器
#     def class_method(cls):
#         content = above + below
#         return content
#
#
# above = "把君诗卷灯前读，诗尽灯残天未明。"
# below = "眼痛灭灯犹闇坐，逆风吹浪打船声。"
# d = Decorator(above, below)
# print(d.poetry)
# print(d.static_method())
# print(d.class_method())

from datetime import datetime


def run_time(func):
    def new_func(*args, **kwargs):
        start_time = datetime.now()
        print("程序开始时间：{}".format(start_time))
        func(*args, **kwargs)
        end_time = datetime.now()
        print("程序结束时间：{}".format(end_time))
        print("程序执行用时：{}s".format((end_time - start_time)))

    return new_func


@run_time
def type_test(content):
    print("type运行时间")
    for i in range(content):
        type(i)


@run_time
def isinstance_test(content):
    print("isinstance运行时间")
    for i in range(content):
        isinstance(i, int)


a = type_test(10000)
b = isinstance_test(10000)