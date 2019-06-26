# -*- coding: utf-8 -*-
# @Time    : 2019/6/24 11:04
# @Author  : project
# @File    : 123.py
# @Software: PyCharm

# a = [1,2,3]
# b = [4,5,6]
# c = [7,8,9]
# d = list(zip(a,b,c))
# print(type(d))
# for i in d:
#     print(list(i))
from datetime import datetime
from dateutil.parser import parse

a = int((parse('22:29') - parse('22:35')).total_seconds()/60)
print(a, type(a))
print(24*60 - int(str(a)[1:]))

# if str(a)[0] == '-':
#     print(24*60 - int(str(a)[1:]))
#     print(24 * 60 - int(str(a)[1:]))
# else:
#     print(2)  365 +37
# print(24*60 - 1254)
# import os
# path = os.path.abspath('.') + r'\log\airport_names.txt'
# with open(path, 'a+', encoding='utf-8')as f:
#     f.seek(0)
#     a = [i.replace('\n', '') for i in f.readlines()]
#     print(a)
#     f.seek(0)
#     f.truncate()
#     print(a)
import os
import time
import datetime
# filePath = os.path.abspath('.') + r'\log\send_sms.txt'
# if os.path.exists(filePath):
#     print(1)
# else:
#     print(2)
# filetime = os.path.getctime(filePath)
# print(filetime)
# mailtime = datetime.datetime.fromtimestamp(filetime).strftime('%Y-%m-%d')  # 格式化时间
# currdate = time.time()  # 当前时间
# mailtime1 = datetime.datetime.fromtimestamp(currdate).strftime('%Y-%m-%d')
#
# print(mailtime1)
# a = mailtime
# b = mailtime1
# if a == b:
#     os.remove(filePath)
#     print(1)
# else:
#     print(2)

# for i in range(5):
#     print(i)

# import os
#
# a = os.system("adb devices")

# output = str(a).replace('\r', '').split('\n')
# # 剔除列表中空字符串
# output = list(filter(None, output))
# if not len(output) > 1:
#     print("读取设备信息失败,自动重启中...")
#
# # 连接设备列表
# devices = [i.split('\t') for i in output[1:]]
# # 读取成功列表
# success = [i[0] for i in devices if i[1] == 'device']
# for i in success:
#     print("设备连接成功：[{}]".format(i))
#

