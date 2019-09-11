# encoding: utf-8
# @Time: 
# @software: PyCharm
# @file: TS流视频保存.py
# @time: 2019/9/11 12:44
import urllib.request, urllib.error, requests
import socket
socket.setdefaulttimeout(5)  # 设置超时时间

"""下载视频保存至指定位置"""
# 方法1
try:
    urllib.request.urlretrieve(url, path)
except socket.timeout:  # 当前进程超时会走下面的流程
    count = 1
    while count <= 3:
        try:
            urllib.request.urlretrieve(url, path)
            break
        except socket.timeout:
            err_info = 'Reloading for %d time' % count if count == 1 else 'Reloading for %d times' % count
            print(err_info)
            count += 1
    if count > 3:
        print("downloading picture fialed!")

# 方法2
import wget
wget.download(url, out=path)