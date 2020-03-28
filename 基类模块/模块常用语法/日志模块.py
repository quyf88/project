# -*- coding:utf-8 -*-
# 文件 ：日志模块.py
# IED ：PyCharm
# 时间 ：2020/3/2 0002 12:31
# 版本 ：V1.0
import os
import sys
import datetime
import logging
'''
定义一个时间花销装饰器，用于输出各个程序的运行时间，
同时，将结果写出到日志中
'''

PATH = os.getcwd()


def run_time(func):
    def new_func(*args, **kwargs):
        logger = args[-1]
        start_time = datetime.datetime.now()
        print("程序开始时间：{}".format(start_time))
        logger.info("程序开始时间：{}".format(start_time))
        res = func(*args, **kwargs)
        end_time = datetime.datetime.now()
        print("程序结束时间：{}".format(end_time))
        print("程序执行用时：{}s".format((end_time - start_time)))
        logger.info("程序结束时间：{}".format(end_time))
        logger.info("程序执行用时：{}s".format((end_time - start_time)))
        return res

    return new_func


def log_init():
    # 创建一个日志器
    program = os.path.basename(sys.argv[0])  # 获取程序名
    logger = logging.getLogger(program)
    # 判断handler是否有值,(避免出现重复添加的问题)
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s | %(name)-3s | %(levelname)-6s| %(message)s')  # 设置日志输出格式
        logger.setLevel(logging.DEBUG)

        # 输出日志至屏幕
        console = logging.StreamHandler()  # 设置日志信息输出至屏幕
        console.setLevel(level=logging.DEBUG)  # 设置日志器输出级别，包括debug < info< warning< error< critical
        console.setFormatter(formatter)  # 设置日志输出格式

        # 输出日志至文件
        path = PATH + r'/logs/'  # 日志保存路径
        if not os.path.exists(path):
            os.mkdir(path)
        filename = path + 'ip-' + datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
        fh = logging.FileHandler(filename, encoding='utf-8', mode='a+')  # 设置日志信息保存至文件
        # fh.setLevel(logging.DEBUG)  # 设置日志器输出级别
        fh.setFormatter(formatter)  # 设置日志输出格式
        logger.addHandler(fh)
        logger.addHandler(console)

    return logger


@run_time
def calc(logger):
    logger.info('running calc function...')
    for i in range(1000000):
        continue


def main():
    logger = log_init()
    calc(logger)


if __name__ == '__main__':
    main()

