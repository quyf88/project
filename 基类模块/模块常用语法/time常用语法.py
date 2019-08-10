# coding=utf-8
# 作者    ： Administrator
# 文件    ：time常用语法.py
# IED    ：PyCharm
# 创建时间 ：2019/7/27 20:29

import time
import datetime

t = time.time()

print(t)                       #原始时间数据
print(int(t))                  #秒级时间戳
print(int(round(t * 1000)))    #毫秒级时间戳

nowTime = lambda:int(round(t * 1000))
print(nowTime())             #毫秒级时间戳，基于lambda

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

