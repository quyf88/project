# -*- coding: utf-8 -*-
# @Time    : 2019/6/19 10:10
# @Author  : project
# @File    : sms_phone.py
# @Software: PyCharm
import os
import logging
import requests


def sms_phone(phone, content):
    """凯信通短信"""
    log = log_init()
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
    if result['Message'] == 'ok':
        log.info("通知短信发送成功：{}{}".format(phone, content))
    else:
        log.error("通知短信发送失败：{}").format(result['message'])
    if result['RemainPoint'] < 5000:
        log.info("短信余额不足请及时充值!")


def log_init():
        """日志模块"""
        path = os.path.abspath('.') + r'\log\send_sms.log'
        formatter = logging.Formatter('%(asctime)s | %(name)-6s | %(levelname)-6s| %(message)s')
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        fh = logging.FileHandler(path, encoding='utf-8', mode='a+')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        console.setFormatter(formatter)
        # 如果需要同時需要在終端上輸出，定義一個streamHandler
        # print_handler = logging.StreamHandler()  # 往屏幕上输出
        # print_handler.setFormatter(formatter)  # 设置屏幕上显示的格式
        logger = logging.getLogger("Spider")
        # logger.addHandler(print_handler)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(console)
        logger.addHandler(fh)
        return logger


if __name__ == '__main__':
    sms_phone('18210836362', '您的验证码为：148625')