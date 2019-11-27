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
    a = '2019-11-25 11:22:59+00:00'  # 数据库中时间数据
    a = a.split('+')[0]  # 数据分割分割分割
    a = datetime.datetime.strptime(a, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=30)
    a = a.strftime('%Y-%m-%d %H:%M:%S')
    tss1 = '2019-11-20 00:00:00'
    # 转为时间数组
    timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")
    print(timeArray)
    # timeArray可以调用tm_year等
    # print(timeArray.tm_year)
    # 转为时间戳 秒级
    timeStamp = int(time.mktime(timeArray))
    print(timeStamp)

    # 当前时间戳
    now_time = int(round(time.time()))
    print(now_time)
    if now_time > timeStamp:
        print('代理到期请及时续费!')


if __name__ == '__main__':

    proxy()
