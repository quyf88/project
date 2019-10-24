# coding=utf-8
# 作者    ： Administrator
# 文件    ：123.py
# IED    ：PyCharm
# 创建时间 ：2019/10/25 0:17

a = '30.00-100.00'
if '-' in a:
    money = a.split('-')[0]
    print(money)

