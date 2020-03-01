# -*- coding:utf-8 -*-
# 文件 ：时区处理.py
# IED ：PyCharm
# 时间 ：2020/3/1 0001 11:04
# 版本 ：V1.0


import pytz  # 时区转换模块
from datetime import datetime

"""
一般系统中，将数据库中的时间统一使用UTC时间，然后在展示之类处理时，转成当地时区
"""


loc_tz = pytz.timezone('Asia/Shanghai')
utc_tz = pytz.timezone('UTC')


def now_dt():
    # 这里先取当前utc时间，然后加上UTC时区，之后转成当前时区
    return datetime.utcnow().replace(tzinfo=utc_tz).astimezone(loc_tz)


def str_2_datetime_by_format(dt_str, dt_format='%Y-%m-%d %H:%M:%S'):
    # 时间格式化输出
    return loc_tz.localize(datetime.strptime(dt_str, dt_format))


def datetime_2_str_by_format(dt, dt_format='%Y-%m-%d %H:%M:%S'):
    # 时间格式化输出
    return dt.astimezone(loc_tz).strftime(dt_format)


if __name__ == '__main__':
    a = now_dt()
    b = datetime_2_str_by_format(a)
    c = datetime_2_str_by_format(a)
    print(a)
    print(b)
    print(c)
    print(f'utc时间：{datetime.utcnow()}')
    print(datetime.utcnow().replace(tzinfo=utc_tz))