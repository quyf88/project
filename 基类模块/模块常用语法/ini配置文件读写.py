# -*- coding:utf-8 -*-
# 文件 ：ini配置文件读写.py
# IED ：PyCharm
# 时间 ：2020/3/1 0001 17:50
# 版本 ：V1.0
from configparser import ConfigParser

"""
配置文件信息
config.ini
[Version]
version = 10.0.0
"""


def red_config():
    """
    读取配置文件
    :return: 记录版本号
    """
    cp = ConfigParser()  # 实例化
    cp.read('config.ini')  # 读取文件
    version = cp.get('Version', 'version')  # 读取值
    return version


def set_config(new_version):
    """
    修改配置文件
    :return:
    """
    cp = ConfigParser()  # 实例化
    cp.read('config.ini')  # 读取文件
    cp.set('Version', 'version', new_version)  # 修改数据
    # 写入新数据
    with open('config.ini', 'w') as f:
        cp.write(f)

