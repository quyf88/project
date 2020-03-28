# -*- coding:utf-8 -*-
# 文件 ：spider.py
# IED ：PyCharm
# 时间 ：2020/3/1 0001 13:35
# 版本 ：V1.0
import os
import re
import sys
import time
import logging
import requests
import datetime
from retrying import retry
from fake_useragent import UserAgent
from configparser import ConfigParser

print(os.path.abspath(__file__))  # 当前文件绝对路径
PATH = os.getcwd()  # 文件路径


def run_time(func):
    def new_func(*args, **kwargs):
        logger = args[-1]
        start_time = datetime.datetime.now()
        # print("程序开始时间：{}".format(start_time))
        logger.info("程序开始时间：{}".format(start_time))
        res = func(*args, **kwargs)
        end_time = datetime.datetime.now()
        # print("程序结束时间：{}".format(end_time))
        # print("程序执行用时：{}s".format((end_time - start_time)))
        logger.info("程序结束时间：{}".format(end_time))
        logger.info("程序执行用时：{}s".format((end_time - start_time)))
        return res

    return new_func


def log_init():
    # 创建一个日志器
    program = os.path.basename(sys.argv[0])  # 获取程序名
    logger = logging.getLogger(program)
    formatter = logging.Formatter('%(asctime)s | %(name)-6s | %(levelname)-6s| %(message)s')  # 设置日志输出格式
    logger.setLevel(logging.DEBUG)

    # 输出日志至屏幕
    console = logging.StreamHandler()  # 设置日志信息输出至屏幕
    console.setLevel(level=logging.DEBUG)  # 设置日志器输出级别，包括debug < info< warning< error< critical
    console.setFormatter(formatter)  # 设置日志输出格式
    logger.addHandler(console)

    # 输出日志至文件
    # path = os.path.abspath('.') + r'/log/'  # 日志保存路径
    path = PATH + '/log/'
    if not os.path.exists(path):
        os.mkdir(path)
    filename = path + datetime.datetime.now().strftime('%Y-%m-%d') + '.csv'
    fh = logging.FileHandler(filename, encoding='utf-8', mode='a+')  # 设置日志信息保存至文件
    fh.setLevel(logging.DEBUG)  # 设置日志器输出级别
    fh.setFormatter(formatter)  # 设置日志输出格式
    logger.addHandler(fh)

    return logger


class DouYinVersion:
    """抖音版本检测"""
    def __init__(self):
        self.headers = {'User-Agent': str(UserAgent().random)}
        self.ini_name = PATH + '/config.ini'

    @retry(stop_max_attempt_number=5)
    def version(self):
        url = 'https://www.wandoujia.com/apps/7461948'
        rsp = requests.get(url, headers=self.headers, timeout=10)
        content = rsp.content.decode(encoding='UTF-8')
        ver = re.findall(r'<dt>版本</dt><dd>&nbsp;(.*?)</dd>', content)
        if not ver:
            log_init().info('没有找到版本号!')
            os._exit(0)
        return ver[0]

    def red_config(self):
        """
        读取配置文件
        :return: 记录版本号
        """
        cp = ConfigParser()  # 实例化
        cp.read(self.ini_name)  # 读取文件
        version = cp.get('Version', 'wandoujia_version')  # 读取值
        return version

    def set_config(self, new_version):
        """
        修改配置文件
        :return:
        """
        cp = ConfigParser()  # 实例化
        cp.read(self.ini_name)  # 读取文件
        cp.set('Version', 'wandoujia_version', new_version)  # 修改数据
        # 写入新数据
        with open(self.ini_name, 'w') as f:
            cp.write(f)

    def sms_phone(self, phone, content, logger):
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
        logger.info(result)
        if result['Message'] == 'ok':
            logger.info("通知短信发送成功：{}:{}".format(phone, content))
        else:
            logger.error(f"通知短信发送失败：{result['Message']}")
        if result['RemainPoint'] < 5000:
            logger.info("短信余额不足请及时充值!")

    @run_time
    def run(self, logger):
        old_version = self.red_config()
        new_version = self.version()
        # print(old_version, type(old_version))
        # print(new_version, type(new_version))
        logger.info(f'检测到最新版本:{new_version},当前版本:{old_version}')
        if new_version != old_version:
            logger.info('版本已更新!')
            self.set_config(new_version)  # 新版本号写入配置文件
            # self.sms_phone('13730963728', f'抖音版本已更新,最新版本号:{new_version}', logger)  # 发送短信
            time.sleep(1)
            # self.sms_phone('18210836362', f'抖音版本已更新,最新版本号:{new_version}', logger)  # 发送短信
            logger.info('新版本号写入成功!')
        else:
            logger.info('版本没有更新!')


if __name__ == '__main__':
    spider = DouYinVersion()
    logger = log_init()
    spider.run(logger)

