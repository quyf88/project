# -*- coding:utf-8 -*-
# 文件 ：123.py
# IED ：PyCharm
# 时间 ：2020/5/8 0008 11:55
# 版本 ：V1.0
import os

print(os.path.abspath(__file__))  # 当前文件绝对路径
PATH = os.getcwd()  # 文件路径

os.remove('config/转推账户信息.txt')