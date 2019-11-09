# -*- coding:utf-8 -*-
# 文件 ：数据去重.py
# IED ：PyCharm
# 时间 ：2019/11/5 0005 13:23
# 版本 ：V1.0
import os
import datetime

filename = '微信号/' + (datetime.datetime.now()+datetime.timedelta(days=-1)).strftime('%Y-%m-%d') + '.txt'
print(filename)


def process():
    """数据去重"""
    # 获取当前目录
    path = os.getcwd()
    print(path)
    # 返回指定目录下所有文件
    files = os.listdir(path + r'/微信号/')
    # 筛选指定文件
    files = [i for i in files if filename not in i]

    # 打开昨天文档去重
    new_text = open(filename, 'r')
    new_text = list(set([i.replace('\n', '') for i in new_text]))

    # 读取旧文件等待去重
    text = []
    for file in files:
        file = r'微信号/' + file
        n_text = open(file, 'r')
        i = [i.replace('\n', '') for i in n_text.readlines()]
        text += i

    # 清空昨日文件
    with open(filename, 'w') as f:
        f.seek(0)
        f.truncate()

    # 数据去重
    for p in new_text:
        if p not in text:
            continue
        with open(filename, 'a+') as f:
            f.write(p)
            f.write('\n')
    print('数据清洗完成!')


if __name__ == '__main__':
    process()