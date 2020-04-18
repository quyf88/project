# -*- coding:utf-8 -*-
# 文件 ：mitmdump_server.py
# IED ：PyCharm
# 时间 ：2019/10/30 0030 16:37
# 版本 ：V1.0
"""
切换至脚本目录下运行脚本
mitmdump -s mitmdump_server.py
OSError: [WinError 87] 参数错误 : 把print注释掉
"""
import re
import os
import csv
import json
import sys
import logging
import datetime
from configparser import ConfigParser

PATH = os.getcwd()
FILE_NAME = f'{PATH}/config/{datetime.datetime.now().strftime("%Y-%m-%d")}.csv'


def response(flow):
    url = 'https://api.twitter.com/2/timeline/conversation/'
    # 过滤接口和数据
    if flow.request.url.startswith(url) and flow.response.text:
        # print(f'*******************************')
        ID = re.findall(r'conversation/(.*?)\.json', flow.request.url)

        # 获取评论json数据
        text = flow.response.text
        # print(f'抓到的包：{text}')
        # 将已编码的json字符串解码为python对象
        content = json.loads(text)
        # 评论数据字典
        tweets = content['globalObjects']['tweets']
        # 写入配置文件
        status_id = tweets[ID[0]].get('quoted_status_id_str')
        status_id = status_id if status_id else '0'
        set_ini('Version', 'id', ID[0])
        set_ini('Version', 'quoted_id', status_id)
        # 获取评论数据字典的值
        for i in tweets:
            if red_ini('Version', 'id') == str(i) or str(i) == red_ini('Version', 'quoted_id'):
                print(f'重复数据跳过:{i}')
                continue
            # 推特ID
            screen_name = tweets[i].get('entities')
            screen_name = screen_name['user_mentions'][0].get('screen_name') if 'user_mentions' in screen_name else ' '

            ID_url = f'https://mobile.twitter.com/{screen_name}/status/{ID[0]}'
            # 发布时间
            release_date = tweets[ID[0]].get('created_at').split(' ')
            release_date = f'{" ".join(release_date[:3])} {release_date[-1]}'

            created_at = tweets[i].get('created_at')  # 时间
            full_text = tweets[i].get('full_text')  # 内容
            full_text = str(full_text).replace('\n', '')
            retweet_count = tweets[i].get('retweet_count')  # 回复数量
            favorite_count = tweets[i].get('favorite_count')  # 转发数
            reply_count = tweets[i].get('favorite_count')  # 点赞数
            new_time = datetime.datetime.now()
            data = [[ID_url, release_date, full_text, created_at, retweet_count, favorite_count, reply_count, new_time]]
            sav_data(data, ID[0])
            # print('成功写入一条数据!')


def red_ini(section, name):
    """读取ini配置文件"""
    file = PATH + '\config\config.ini'  # 文件路径
    cp = ConfigParser()  # 实例化
    cp.read(file, encoding='utf-8')  # 读取文件
    val = cp.get(section, name)   # 读取数据
    return val


def set_ini(section, name, val):
    """读取、修改 ini配置文件"""
    file = PATH + '\config\config.ini'  # 文件路径
    cp = ConfigParser()  # 实例化
    cp.read(file, encoding='utf-8')  # 读取文件
    cp.set(section, name, val)  # 修改数据
    with open(file, 'w', encoding='utf-8') as f:
        cp.write(f)


def sav_data(data, name):
    """
    保存数据
    :return:
    """
    path = PATH + r'/数据'  # 数据保存路径
    if not os.path.exists(path):
        os.mkdir(path)
    FILE_NAME = f'{path}/{name}.csv'
    with open(FILE_NAME, "a+", encoding='UTF-8', newline="") as f:
        k = csv.writer(f, delimiter=',')
        with open(FILE_NAME, "r", encoding='UTF-8', newline="") as f1:
            reader = csv.reader(f1)
            if not [row for row in reader]:
                k.writerow(
                    ['Twitter ID', '发布日期', '评论', '评论时间', '回复数', '转发数', '点赞数', '获取数据时间'])
                k.writerows(data)
            else:
                k.writerows(data)
