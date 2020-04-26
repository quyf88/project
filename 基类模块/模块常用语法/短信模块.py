# -*- coding: utf-8 -*-
# @Time    : 2019/6/19 10:10
# @Author  : project
# @File    : sms_phone.py
# @Software: PyCharm
import os
import sys
import logging
import requests
import datetime


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
    formatter = logging.Formatter('%(asctime)s | %(name)-3s | %(levelname)-6s| %(message)s')  # 设置日志输出格式
    logger.setLevel(logging.DEBUG)

    # 输出日志至屏幕
    console = logging.StreamHandler()  # 设置日志信息输出至屏幕
    console.setLevel(level=logging.DEBUG)  # 设置日志器输出级别，包括debug < info< warning< error< critical
    console.setFormatter(formatter)  # 设置日志输出格式
    logger.addHandler(console)

    # 输出日志至文件
    path = os.path.abspath('.') + r'/log/'  # 日志保存路径
    if not os.path.exists(path):
        os.mkdir(path)
    filename = path + datetime.datetime.now().strftime('%Y-%m-%d') + '.csv'
    fh = logging.FileHandler(filename, encoding='utf-8', mode='a+')  # 设置日志信息保存至文件
    fh.setLevel(logging.DEBUG)  # 设置日志器输出级别
    fh.setFormatter(formatter)  # 设置日志输出格式
    logger.addHandler(fh)

    return logger


@run_time
def sms_phone(phone, content, logger):
    """凯信通短信"""

    url = 'http://sms.kingtto.com:9999/sms.aspx'
    content = '【智能航班】{}'.format(content)
    params = {
        'action': 'send',
        'account': 'hongkegu',
        'password': 'chenxiaoli2013',
        'userid': '4112',
        'mobile': phone,
        'content': content,
        'rt': 'json'
    }

    response = requests.post(url, data=params)
    result = response.json()
    print(result)
    if result['Message'] == 'ok':
        logger.info("通知短信发送成功：{}{}".format(phone, content))
    else:
        print(result['Message'])
        logger.error(f"通知短信发送失败：{result['Message']}")
    if result['RemainPoint'] < 5000:
        logger.info("短信余额不足请及时充值!")


def main():
    logger = log_init()
    sms_phone('18210836362', 'IP账号：ba618b3e3adc4e7c93127546d58502a5 即将到期及时续费!', logger)
    sms_phone('13730963728', 'IP账号：ba618b3e3adc4e7c93127546d58502a5 即将到期及时续费!', logger)


if __name__ == '__main__':
    main()