# -*- coding: utf-8 -*-
# @Time    : 2019/6/19 16:12
# @Author  : project
# @File    : adb_server.py
# @Software: PyCharm

import subprocess


def run():
    get_cmd = "adb devices"  # 查询连接设备列表
    cmds = ['127.0.0.1:62025', '127.0.0.1:62026']
    count = 0
    while cmds:
        # 连接设备
        if count > 2:
            print("读取设备信息失败,请检查设备是否成功启动")
            break

        for cmd in cmds:
            cmd1 = 'adb connect {}'.format(cmd)  # 手动启动设备
            subprocess.Popen(cmd1, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        # 读取连接设备信息
        p = subprocess.Popen(get_cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        output = output.split()

        if len(output) < 5:
            print("读取设备信息失败,自动重启中...")
            count += 1
            continue

        if len(output) >= 7 and output[5].decode() == 'device':
            result = output[4].decode()
            result1 = output[6].decode()
            print("读取到设备：[{}]正常运行中".format(result))
            print("读取到设备：[{}]正常运行中".format(result1))
            break


if __name__ == '__main__':
    run()