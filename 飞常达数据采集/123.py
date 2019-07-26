# -*- coding: utf-8 -*-
# @Time    : 2019/6/24 11:04
# @Author  : project
# @File    : search_word.py
# @Software: PyCharm



import time
#
# a = chat.Itchat()
# print('等待')
#
# for i in range(2):
#     time.sleep(1)
#     a.SendFriend('哈哈蛋蛋')
from datetime import datetime
# currdate = time.time()
# mailtime1 = datetime.fromtimestamp(currdate).strftime('%H:%M:%S')
# print(mailtime1)

# 范围时间
# d_time = datetime.strptime(str(datetime.now().date()) + '16:30', '%Y-%m-%d%H:%M')
# d_time1 = datetime.strptime(str(datetime.now().date()) + '18:00', '%Y-%m-%d%H:%M')
# print(d_time)
# print(d_time1)
# # 当前时间
# n_time = datetime.now()
#
# # 判断当前时间是否在范围时间内
# if n_time > d_time and n_time < d_time1:
#     print(1)
# else:
#     print(2)

# a = [1,2,3]
# b = [4,5,6]
# c = [7,8,9]
# d = zip(a,b,c)
# print(type(d))
# for i in d:
#     print(list(i))
from datetime import datetime
from dateutil.parser import parse
"""时间计算"""
# a = int((parse('15:16') - parse('23:00')).total_seconds()/60)
# print(a)
# print(24*60 - int(str(a)[1:]))
# a = '+517'
#
# if '+' in a:
#     print(1)
# else:
#     print(2)


# if str(a)[0] == '-':
#     print(24*60 - int(str(a)[1:]))
#     print(24 * 60 - int(str(a)[1:]))
# else:
#     print(2)  365 +37
# print(24*60 - 1254)

"""读取文件"""
# import os
# path = os.path.abspath('.') + r'\log\airport_names.txt'
# with open(path, 'a+', encoding='utf-8')as f:
#     f.seek(0)
#     a = [i.replace('\n', '') for i in f.readlines()]
#     print(a)
#     f.seek(0)
#     f.truncate()
#     print(a)


"""根据文件创建日期 删除文件"""
import os
import time
from datetime import datetime

# class a:
#
#     def update_data(self):
#         path = os.path.abspath('.') + r'\log\config.txt'
#         self.remove_data(path)
#         with open(path, 'a+', encoding='utf-8')as f:
#             f.write('123' + '\n')
#             print('更新航班记录成功!')
#             f.seek(0)
#             flight = [i.replace('\n', '') for i in f.readlines()]
#             print(flight)
#             print('读取已处理航班记录成功!')
#             # 获取文件创建日期
#             filetime = os.path.getctime(path)
#             mailtime = datetime.fromtimestamp(filetime).strftime('%Y-%m-%d')
#             print(filetime, mailtime)
#
#     def remove_data(self, path):
#         if os.path.exists(path):
#             # 获取文件创建日期
#             filetime = os.path.getctime(path)
#             mailtime = datetime.fromtimestamp(filetime).strftime('%Y-%m-%d')
#             print(filetime, mailtime)
#             # 当前系统日期
#             currdate = time.time()
#             mailtime1 = datetime.fromtimestamp(currdate).strftime('%Y-%m-%d')
#
#             # 判断文件创建日期是否等于当前系统日期 如不相等 删除前一天的发送记录
#             if mailtime != mailtime1:
#                 os.remove(path)
#                 print("删除成功")
#                 time.sleep(15)
#
#
# a().update_data()


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
#
# if '9C' in '9C8824':
#     print(1)
# else:
#     print(2)

chen_time = datetime.strptime(str(datetime.now().date()) + '6:00:00', '%Y-%m-%d%H:%M:%S')
start_time = datetime.strptime(str(datetime.now().date()) + '21:00:00', '%Y-%m-%d%H:%M:%S')
end_time = datetime.strptime(str(datetime.now().date()) + '23:59:59', '%Y-%m-%d%H:%M:%S')
now_time = datetime.now()
if now_time > start_time and now_time < end_time:
    print(1)
elif now_time > chen_time and now_time < start_time:
    print(2)
else:
    print(3)