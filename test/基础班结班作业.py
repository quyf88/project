# -*- coding: utf-8 -*-
# @Time    : 2019/5/8 12:39
# @Author  : project
# @File    : 基础班结班作业.py
# @Software: PyCharm

"""第一题"""

# def fun():
#     li = []
#     for i in range(5):
#         li.append(lambda x: i ** x)
#     return li
#
#
# gun = fun()
#
# print(gun[0](2))  # 运行结果：16
# print(gun[1](2))  # 运行结果：16
# print(gun[2](2))  # 运行结果：16

# 这三个输出的结果是什么， 并解释原因

# 原因：lambda x: i ** x 为内层嵌套函数，调用时会去外层函数中寻找i变量值，
#       外层循环完之后i的值为4，lambda读取到的i值会一直是4


"""
2、解释什么是闭包，为什么说闭包是函数内与函数外沟通的桥梁？
"""
# 函数里面再定义一个函数，并且内层函数引用外层函数的变量，外层函数返回内层函数的函数体称之为闭包
# 因为在外部可以直接调用函数中嵌套的函数

"""
3、定义一个人类person类，人类具有职业、名字等特点，会吃饭和睡觉，再定义一个学生类去继承人类的特点和功能，
    学生本身还具有学习和自我介绍的功能，并且实例可以直接被调用，调用的时候会去使用类的其中一个方法
"""

# class Person:
#
#     def __init__(self, career, name):
#         self.career = career
#         self.name = name
#
#     def eat(self):
#         print("{}：正在睡觉".format(self.name))
#
#     def sleep(self):
#         print("{}：正在吃饭".format(self.name))
#
#
# class Student(Person):
#
#     def __init__(self, career, name):
#         super().__init__(career, name)
#
#     def learn(self):
#         print("{}：正在学习".format(self.name))
#
#     def presentation(self):
#         print("大家好我是：{} 职业：{}".format(self.name, self.career))
#
#
# if __name__ == '__main__':
#     stu = Student("学生", "小明")
#     stu.eat()
#     stu.sleep()
#     stu.learn()
#     stu.presentation()


"""
# ①打印出列表中的Python

# ②打印出guanxiaotong,luhan，并将他们添加到list_2

# ③打印出nvzhuangdalao，并将nvzhuangdalao添加到到list_2.

# ④print(list_1[2][5][0])会打印出什么？
"""
# list_1 = ['1',
#           ['2', 'nvzhuangdalao', 'Thailander'],
#           ['2', 'Java', 'Python', 'Ruby', 'PHP', ['3', 'zhaoliying', 'guanxiaotong', 'Hi python']],
#           ['2', 'Adam', 'Bart', 'Lisa', ['3', 'luhan', 'wuyifan', 'liyifeng', 'wangbaoqiang']]
#           ]
#
# list_2 = []
# # ①打印出列表中的Python
# print('①打印出列表中的Python')
# print(list_1[2][2])
# print('*' * 50)
#
# # ②打印出guanxiaotong,luhan，并将他们添加到list_2
# print('②打印出guanxiaotong,luhan，并将他们添加到list_2')
# print(list_1[2][5][2])
# list_2.append(list_1[2][5][2])
# print(list_1[3][4][1])
# list_2.append(list_1[3][4][1])
# print(list_2)
# print('*' * 50)
#
# # ③打印出nvzhuangdalao，并将nvzhuangdalao添加到到list_2.
# print('# ③打印出nvzhuangdalao，并将nvzhuangdalao添加到到list_2.')
# print(list_1[1][1])
# list_2.append(list_1[1][1])
# print(list_2)
# print('*' * 50)
#
# print('④print(list_1[2][5][0])会打印出什么？')
# print(list_1[2][5][0])  # ④结果：3

"""
5、设计一个拥有注册和登录功能的小程序，要求：注册完成后提示注册的账号和密码，
    登录成功后，提示欢迎登录，账号或者密码不正确时，返回相应提示。
提示：这题实现的方法比较多，我会根据编写的难度不同酌情给分，遇到不会写的可以用伪代码代替！
"""


class Account:

    def __init__(self, number='admin', password='123456'):
        self.number = number
        self.password = password

    def login(self):
        """注册模块"""
        number = input("注册账号：")
        while True:
            password_1 = input("设置密码：")
            password_2 = input("确认密码：")
            if password_1 != password_2:
                print("两次密码输入不一致，请重新输入")
                continue
            else:
                print("注册成功，账号：{} 密码：{}".format(number, password_2))
                self.number = number
                self.password = password_2
                break
        while True:
            print("*" * 30)
            print("*-----1.账号登录-----*")
            print("*-----2.退出系统-----*")
            print("*" * 30)
            user_input = int(input("请输入:"))

            if user_input == 1:
                self.log_in()
            elif user_input == 2:
                self.out()
            else:
                print("输入错误重新输入")
                continue

    def log_in(self):
        """登录模块"""
        while True:
            number = input("账号：")
            password = input("密码：")
            if number != self.number or password != self.password:
                print("账号或密码错误，请重新输入")
                continue

            print("{}:欢迎登录".format(number))
            print("*" * 30)
            print("*-----1.退出登录-----*")
            print("*-----2.退出系统-----*")
            print("*" * 30)
            user_input = int(input("请输入:"))

            if user_input == 1:
                print("账号退出成功!")
                self.main()
            elif user_input == 2:
                self.out()
                break
            else:
                print("输入错误重新输入")

    def out(self):
        print("退出系统")

    def main(self):
        while True:
            print("*" * 30)
            print("*---用户注册登录系统---*")
            print("*-----1.登录-----*")
            print("*-----2.注册-----*")
            print("*-----3.退出-----*")
            print("*" * 30)
            user_input = int(input("请输入:"))
            if user_input == 1:
                self.log_in()
                break
            elif user_input == 2:
                self.login()
                break
            elif user_input == 3:
                self.out()
                break
            else:
                print("输入错误重新输入")


if __name__ == '__main__':
    login = Account()
    login.main()

















