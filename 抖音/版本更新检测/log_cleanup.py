# -*- coding:utf-8 -*-
# 文件 ：定时清理日志脚本.py
# IED ：PyCharm
# 时间 ：2020/3/6 0006 11:45
# 版本 ：V1.0
import os
import sys
import logging
import datetime


# PATH = os.path.abspath('.') + r'/'
PATH = '/DouYinVersion/'


def log_init():
    # 创建一个日志器
    program = os.path.basename(sys.argv[0])  # 获取程序名
    logger = logging.getLogger(program)
    formatter = logging.Formatter('%(asctime)s | %(name)-3s | %(levelname)-6s| %(message)s')  # 设置日志输出格式
    logger.setLevel(logging.DEBUG)

    # 输出日志至屏幕
    console = logging.StreamHandler()  # 设置日志信息输出至屏幕
    console.setLevel(level=logging.DEBUG)  # 设置日志器输出级别，包括debug < info< warning< error< critical
    console.setFormatter(formatter)  # 设置日志输出格式
    logger.addHandler(console)

    # 输出日志至文件
    filename = PATH + '日志.log'
    fh = logging.FileHandler(filename, encoding='utf-8', mode='a+')  # 设置日志信息保存至文件
    fh.setLevel(logging.DEBUG)  # 设置日志器输出级别
    fh.setFormatter(formatter)  # 设置日志输出格式
    logger.addHandler(fh)

    return logger


def log_cleanup(days):
    """
    定时删除日志脚本
    days:保留几天数据
    :return:
    """
    log = log_init()
    path = PATH + r'/log/'
    count = 0
    if not os.path.exists(path):
        log.info('没有找到日志目录文件')
        return

    files = os.listdir(path)
    for file in files:
        # 分离文件名
        (filename, extension) = os.path.splitext(file)
        # 文件名转换成时间格式
        file_time = datetime.datetime.strptime(filename, "%Y-%m-%d").strftime("%Y-%m-%d")
        # 当前时间减去几天
        new_time = (datetime.datetime.now()+datetime.timedelta(days=-days)).strftime("%Y-%m-%d")
        # 判断保留几天的数据
        if file_time <= new_time:
            os.remove(path + file)
            log.info(f'删除:{file}成功')
            count += 1
    log.info(f'脚本执行完毕,共删除:{count}份日志文件!')


if __name__ == '__main__':
    log_cleanup(1)
