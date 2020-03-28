#!/usr/bin/env python
# coding=utf-8
import os
import sys
import logging
import datetime
from django.http import HttpResponse

PATH = os.getcwd()


def get_ip(request):
    """获取访问客户端ip地址"""
    username = request.META.get('USERDOMAIN_ROAMINGPROFILE')
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip = request.META.get("HTTP_X_FORWARDED_FOR")
    else:
        ip = request.META.get("REMOTE_ADDR")
    # 写入日志文件
    content = f'{username} {ip}'
    log_init().info(content)
    return HttpResponse(f'用户名：{username} IP地址：{ip}')


def log_init():
    # 创建一个日志器
    program = os.path.basename(sys.argv[0])  # 获取程序名
    logger = logging.getLogger(program)
    # 判断handler是否有值,(避免出现重复添加的问题)
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s | %(name)-3s | %(levelname)-6s| %(message)s')  # 设置日志输出格式
        logger.setLevel(logging.DEBUG)

        # 输出日志至文件
        path = PATH + r'/logs/'  # 日志保存路径
        if not os.path.exists(path):
            os.mkdir(path)
        filename = path + 'ip-' + datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
        fh = logging.FileHandler(filename, encoding='utf-8', mode='a+')  # 设置日志信息保存至文件
        fh.setLevel(logging.DEBUG)  # 设置日志器输出级别
        fh.setFormatter(formatter)  # 设置日志输出格式
        logger.addHandler(fh)

    return logger