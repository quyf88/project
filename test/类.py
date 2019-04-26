# -*- coding: utf-8 -*-
# @Time    : 2019/4/24 10:19
# @Author  : Mat
# @Software: PyCharm

class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        result = "矩形长{} 宽{} 面积:{}".format(self.length, self.width, self.length * self.width)
        return result

class Square(Rectangle):
    def __call__(self, *args, **kwargs):
        print("正方形边长为：{}".format(self.length))
        if self.length == self.width:
            print("正方形的面积：{}".format(self.length * self.width))
        else:
            print("这是一个矩形")
            print(super().area())


ar = Square(20, 20)
ar()

