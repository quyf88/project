# -*- coding:utf-8 -*-
# 文件 ：script.py
# IED ：PyCharm
# 时间 ：2020/2/24 0024 10:59
# 版本 ：V1.0

import os
import time
import socket


class Monitor:

    def net_is_used(self, port, ip='127.0.0.1'):
        """
        检测端口是否被占用
        :param port: 端口
        :param ip:IP地址
        :return:
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, port))
            s.shutdown(2)
            # print(f'sorry, {ip}:{port} 端口已被占用!')
            return True
        except Exception as e:
            # print(f'{ip}:{port}端口未启用!')
            print(e)
            return False

    def switch_appium(self):
        """启动Appium服务"""
        print('杀死Appium服务')
        node = 'taskkill /F /IM node.exe'
        cmd = 'taskkill /F /IM cmd.exe'
        os.system(node)
        os.system(cmd)
        print('启动Appium服务')
        os.system('appium_server.bat')
        time.sleep(5)
        if not self.net_is_used(4723):
            print('Appium服务启动失败!')
            os._exit(0)
        print('Appium服务启动成功!')

    def switch_mitmdump(self):
        """启动mitmdump服务"""
        print('杀死mitmdump服务')
        mitmdump = 'taskkill /F /IM mitmdump.exe'
        cmd = 'taskkill /F /IM cmd.exe'
        os.system(mitmdump)
        os.system(cmd)
        print('启动mitmdump服务')
        os.system('start /min mitmdump -s mitmdump_server.py')
        time.sleep(5)
        if not self.net_is_used(8080):
            print('mitmdump服务启动失败!')
            os._exit(0)
        print('mitmdump服务启动成功!')

    def kill(self):
        """
        根据端口找到PID：netstat -aon|findstr "443"
        根据PID找到程序名：tasklist|findstr "12380"
        杀死进程   # /F 强制终止进程, /T 终止指定的进程和由它启用的子进程, /IM 指定要终止的进程的映像名称
        """
        node = 'taskkill /F /IM node.exe'
        mitmdump = 'taskkill /F /IM mitmdump.exe'
        cmd = 'taskkill /F /IM cmd.exe'
        os.system(node)  # 杀死appium进程
        os.system(mitmdump)  # 杀死mitmdump进程
        os.system(cmd)  # 关闭命令行窗口

    def run(self):
        # self.kill()  # 杀死服务
        # time.sleep(3)
        self.switch_appium()  # 启动appium
        self.switch_mitmdump()  # 启动mitmdump


if __name__ == '__main__':
    Monitor = Monitor()
    Monitor.run()
