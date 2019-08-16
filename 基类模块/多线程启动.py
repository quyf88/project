# -*- coding: utf-8 -*-
# @Time    : 2019/8/14 8:53
# @Author  : project
# @File    : 多线程启动.py
# @Software: PyCharm
import os
import time
import threading
"""多线程启动"""


def say_hello(num):
    print("启动第[{}]个程序!".format(num))
    os.system('python server{}/spider.py'.format(num))


def main():
    for i in range(1):
        thread = threading.Thread(target=say_hello, args=str(i+1))
        thread.start()
        time.sleep(10)


main()

