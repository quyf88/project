# -*- coding: utf-8 -*-
# @Time    : 2019/5/24 9:41
# @Author  : project
# @File    : my_logging.py
# @Software: PyCharm

import logging
"""
logging 模块化组件
"""


def create_logging():
    # 创建logger对象
    my_logger = logging.Logger('my_logging')
    # 配置日志输出文件
    mh = logging.FileHandler('my_log.log')
    # 配置日志级别
    mh.setLevel(logging.info)
    # 配置日志输出格式
    fmt = logging.Formatter('时间：%(asctime)s-文件名：%(filename)s-错误信息：%(message)s-行号：%(lineno)d')
    # 添加
    mh.setFormatter(fmt)
    my_logger.addHandler(mh)

    return my_logger


if __name__ == '__main__':
    try:
        a = 1/0
    except Exception as e:
        my_logger = create_logging()
        my_logger.info(e)  # 报错信息
        my_logger.exception(e)  # 详细报错信息 只可在try里应用