# -*- coding:utf-8 -*-
# 文件 ：端口操作脚本.py
# IED ：PyCharm
# 时间 ：2020/2/24 0024 10:59
# 版本 ：V1.0

import os
import time
import socket


class Monitor:
    def __init__(self, port):
        self.port = port

    def net_is_used(self, ip='127.0.0.1'):
        """
        检测端口是否被占用
        :param port: 端口
        :param ip:IP地址
        :return:
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, self.port))
            s.shutdown(2)
            print(f'sorry, {ip}:{self.port} 端口已被占用!')
            return True
        except Exception as e:
            print(f'{ip}:{self.port}端口未启用!')
            print(e)
            return False

    def switch_on(self):
        """启动脚本"""
        # 启动Appium服务
        if self.port == 4723:
            os.system('appium_server.bat')
        elif self.port == 8080:
            os.system('start /min mitmdump -s mitmdump_server.py')
        else:
            print('启动脚本错误!')
            os._exit(0)

    def kill(self):
        """
        根据端口找到PID：netstat -aon|findstr "443"
        根据PID找到程序名：tasklist|findstr "12380"
        杀死进程   # /F 强制终止进程, /T 终止指定的进程和由它启用的子进程, /IM 指定要终止的进程的映像名称
        """
        node = 'taskkill /F /IM node.exe'
        mitmdump = 'taskkill /F /IM mitmdump.exe'
        cmd = 'taskkill /F /IM cmd.exe'
        if self.port == 4723:
            os.system(node)  # 杀死appium进程
            os.system(cmd)  # 关闭命令行窗口
        if self.port == 8080:
            os.system(mitmdump)  # 杀死mitmdump进程
            os.system(cmd)  # 关闭命令行窗口

    def run(self):
        if self.net_is_used():  # 检查端口是否被占用
            self.kill()  # 杀死服务
            time.sleep(3)
        print('启动脚本')
        self.switch_on()  # 启动脚本
        print(f'成功启动：{self.port}端口服务!')


if __name__ == '__main__':
    port = 8080
    Monitor = Monitor(port)
    Monitor.run()
