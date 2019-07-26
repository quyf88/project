# coding=utf-8
# 作者    ： Administrator
# 文件    ：appium_server.py
# IED    ：PyCharm
# 创建时间 ：2019/6/21 19:38
import os
import subprocess
from time import ctime
import multiprocessing  # 导入多进程模块

"""多线程启动appium_server"""


class AppiumServer:

    def appium_start(port, devi_port):
        a = os.popen('netstat -ano | findstr "%s" ' % port)
        t1 = a.read()
        if "LISTENING" in t1:
            print("appium服务已经启动：%s" % t1)
        else:
            # 启动appium服务  /b是不打开cmd命令窗口
            # start /b appium -a 127.0.0.1 -p 4740 -U 127.0.0.1:62001 --no-reset
            cmd = "start appium -a 127.0.0.1 -p {} -U 127.0.0.1:{} --no-reset".format(port, devi_port)
            print('%s at %s' % (cmd, ctime()))
            # 启动服务
            subprocess.Popen(cmd, shell=True)

    # 构建appium进程组
    appium_process = []
    # 加载appium进程
    for i in range(2):
        port = 4730 + 5 * i
        devi_port = 62025 + i
        # target指向方法，args指向参数，且必须是一个元组的形式
        appium = multiprocessing.Process(target=appium_start, args=(port, devi_port))
        # 将进程从变量appium加载到进程内
        appium_process.append(appium)

    def run(self):
        # 并发启动appium服务，for循环开启多个appium服务，join主进程等待子进程结束
        for appium in self.appium_process:
            appium.start()

        for appium in self.appium_process:
            appium.join()


if __name__ == '__main__':
    a = AppiumServer()
    a.run()


