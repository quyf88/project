# -*- coding: utf-8 -*-
# @Time    : 2019/6/19 16:12
# @Author  : project
# @File    : adb_server.py
# @Software: PyCharm

import subprocess


def run():
    cmd = "adb devices"  # 查询连接设备列表
    while True:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        if len(output.split()) < 5:
            print("读取设备信息失败,自动重启中...")
            cmd1 = 'adb connect 127.0.0.1:62001'  # 手动启动设备
            subprocess.Popen(cmd1, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
            print("设备重启成功,信息读取中...")
            continue
        if output.split()[5].decode() == 'device':
            result = output.split()[4].decode()
            print("读取到设备：[{}]正常运行中".format(result))
            return result
        else:
            print("请检查设备是否打开")

        break




