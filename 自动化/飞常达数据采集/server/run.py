# coding=utf-8
# 作者    ： Administrator
# 文件    ：多线程启动.py
# IED    ：PyCharm
# 创建时间 ：2019/6/22 19:28

import os
import adb_server


def run():
    # 启动设备
    adb_server.run()
    # 启动appium服务 chdir设置文件路径为工作目录 system启动bat脚本
    path = os.path.abspath('.')
    os.chdir(path)
    os.system(path + r'\app_server.bat')


if __name__ == '__main__':
    run()