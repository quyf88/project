# -*- coding: utf-8 -*-
# @Time    : 2019/7/24 10:39
# @Author  : project
# @File    : 视频保存.py
# @Software: PyCharm
import requests


"""
stream 
当把get函数的stream参数设置成True时，它不会立即开始下载，当你使用iter_content或iter_lines遍历内容或访问内容属性时才开始下载。需要注意一点：文件没有下载之前，它也需要保持连接。

iter_content：一块一块的遍历要下载的内容
iter_lines：一行一行的遍历要下载的内容
"""
url = "http://avideo.babybus.com/201903271550/3eaef0e128b0cbe7cde481e6f0b17ebe/storage/video/1/7a8baf3c/1196_540.mp4"
r = requests.get(url, stream=True)
with open('name.mp4', "wb") as mp4:
    for chunk in r.iter_content(chunk_size=1024 * 1024):
        if chunk:
            mp4.write(chunk)
