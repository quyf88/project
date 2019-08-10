# coding=utf-8
# 作者    ： Administrator
# 文件    ：设置程序自动运行时间.py
# IED    ：PyCharm
# 创建时间 ：2019/8/10 13:22
import sys
import time

a = int(input('输入程序运行时间:秒'))
print('设置程序运行时间：{}秒 后自动关闭'.format(a))
while True:
    # 程序开始时间戳
    start_time = time.time()
    for i in range(1000):
        time.sleep(1)
        print(i)
        # 当前时间戳
        end_time = time.time()
        # 判断程序运行时间
        blank_time = int(end_time - start_time)
        if blank_time >= a:
            print(int(blank_time))
            print('程序结束')
            sys.exit()


