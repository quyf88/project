# -*- coding: utf-8 -*-
# @Time    : 2019/6/19 16:12
# @Author  : project
# @File    : adb_server.py
# @Software: PyCharm

import subprocess


def run():
    get_cmd = "adb devices"  # 查询连接设备列表
    count = 0
    while True:
        # 连接设备
        if count > 2:
            print("读取设备信息失败,请检查设备是否成功启动")
            break
        # 读取连接设备信息
        p = subprocess.Popen(get_cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)

        (output, err) = p.communicate()
        # 分割多条信息为列表
        output = output.decode().replace('\r', '').split('\n')
        # 剔除列表中空字符串
        output = list(filter(None, output))
        if not len(output) > 1:
            print("读取设备信息失败,自动重启中...")
            count += 1
            continue
        # 连接设备列表
        devices = [i.split('\t') for i in output[1:]]
        # 读取成功列表
        success = [i[0] for i in devices if i[1] == 'device']
        for i in success:
            print("设备连接成功：[{}]".format(i))

        break


if __name__ == '__main__':
    run()