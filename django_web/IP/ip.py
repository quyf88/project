#!/usr/bin/env python
# coding=utf-8
import os
import sys
import json
import requests
from retrying import retry
import logging
import datetime
from django.http import HttpResponse

PATH = os.getcwd()


def get_ip(request):
    """获取访问客户端ip地址"""
    ip = None
    proxy_ip = None
    server_name = request.META.get('SERVER_NAME')
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip = request.META.get("HTTP_X_FORWARDED_FOR")
        proxy_ip = request.META.get("REMOTE_ADDR")
    else:
        ip = request.META.get("REMOTE_ADDR")
    # 获取物理地址
    try:
        address = ip_address(ip)
    except:
        address = '获取失败'
    # 写入日志文件
    log_init().info(f'{server_name} {ip} {address}')
    return HttpResponse(ip)


@retry(stop_max_attempt_number=5)
def ip_address(ip):
    """ip地址查询物理地址"""
    url = f'http://api.map.baidu.com/location/ip?ak=VCyE5wE5Wmo19kgLodBkbt0n5obyji5j&ip={ip}&coor=bd09ll'
    rsp = requests.get(url, timeout=10).text
    content = json.loads(rsp)

    # 请求状态 0有数据 1无数据
    status = content['status']
    if status:
        return content['message']
    address = content['content']['address']
    return address


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
