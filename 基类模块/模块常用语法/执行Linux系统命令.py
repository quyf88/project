# -*- coding:utf-8 -*-
# 文件 ：123.py
# IED ：PyCharm
# 时间 ：2020/3/5 0005 23:23
# 版本 ：V1.0
import os
import datetime


def shell():
    """
    执行Linux系统命令
    :return:
    """
    # 读取系统内存文件
    with open('meminfo', 'r') as f:
        contents = f.readlines()
        contents = [i.strip().replace(' ', '').split(':') for i in contents]

    MemTotal = [int(i[1].replace('kB', '')) for i in contents if i[0] == 'MemTotal'][0]  # 系统内存
    MemFree = [int(i[1].replace('kB', '')) for i in contents if i[0] == 'MemFree'][0]  # 可用内存

    if MemFree < int(MemTotal*0.3):
        print(f'系统内存：{MemTotal} 可用内存：{MemFree}')
        print('可用内存低于系统内存30%,清理内存缓存数据!')
        os.system('echo 3 > /proc/sys/vm/drop_caches')


# 十分钟执行一次shell命令
new_time = (datetime.datetime.now()+datetime.timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')
print(new_time)
start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(start_time)
if new_time > start_time:
    shell()




