# -*- coding:utf-8 -*-
# 文件 ：定时清理日志脚本.py
# IED ：PyCharm
# 时间 ：2020/3/6 0006 11:45
# 版本 ：V1.0
import os
import datetime

PATH = os.path.abspath('.') + r'/log/'


def log_cleanup(days):
    """
    定时删除日志脚本
    days:保留几天数据
    :return:
    """
    count = 0
    if not os.path.exists(PATH):
        print('没有找到日志目录文件')
        return

    files = os.listdir(PATH)
    for file in files:
        # 分离文件名
        (filename, extension) = os.path.splitext(file)
        # 文件名转换成时间格式
        file_time = datetime.datetime.strptime(filename, "%Y-%m-%d").strftime("%Y-%m-%d")
        # 当前时间减去几天
        new_time = (datetime.datetime.now()+datetime.timedelta(days=-days)).strftime("%Y-%m-%d")
        # 判断保留几天的数据
        if file_time <= new_time:
            os.remove(PATH + file)
            print(f'删除:{file}成功')
            count += 1
    print(f'脚本执行完毕,共删除:{count}份日志文件!')


if __name__ == '__main__':
    log_cleanup(0)