# -*- coding:utf-8 -*-
# 文件 ：计时器.py
# IED ：PyCharm
# 时间 ：2019/10/29 0029 10:40
# 版本 ：V1.0
import time
import datetime

# 当前时间多加一天days=1 、一小时hours=1、一分钟minutes=1
new_time = (datetime.datetime.now() + datetime.timedelta(minutes=20)).strftime('%Y-%m-%d %H:%M:%S')
start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
if new_time < start_time:
    print('超时退出')


def proxy():
    # 字符类型的时间
    tss1 = '2019-11-20 00:00:00'
    # 转为时间数组
    timeArray = time.strptime(tss1, "%Y-%m-%d %H:%M:%S")
    print(timeArray)
    # timeArray可以调用tm_year等
    # print(timeArray.tm_year)
    # 转为时间戳 秒级
    timeStamp = int(time.mktime(timeArray))
    print(timeStamp)

    # 当前时间
    now_time = int(round(time.time()))
    print(now_time)
    if now_time < timeStamp:
        print('代理到期请及时续费!')



proxy()