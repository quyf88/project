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
    os.system('python server{}/批量添加子站.py'.format(num))


def main():
    for i in range(1):
        thread = threading.Thread(target=say_hello, args=str(i+1))
        thread.start()
        time.sleep(10)


main()

"""获取评论数据"""
import threading
import requests
from lxml import etree


def demo(i):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
            }
    # for i in range(10):
    #     # 拼接url
    #     url = f'http://www.qiumeimei.com/page/{i+1}' + str(i)
    url = f'http://www.qiumeimei.com/page/' + str(i)

    r = requests.get(url, headers=headers)  # 请求url
    ret = r.content.decode()  # 解析获得字符串类型数据
    result = etree.HTML(ret)  # 转换数据类型为HTML,方便使用xpath

    # xpath 表达式
    img_list = result.xpath("//div[@class='home_main_wrap']/div/div[2]/p/img/@data-lazy-src")

    # 文件存储
    for img in img_list:
        print(img_list)
        img_url = requests.get(img)
        # 命名文件,取文件后十位为文件名
        with open('img/%s' % img[-10:], 'wb') as f:
            f.write(img_url.content)


if __name__ == '__main__':
    # 多线程
    for i in range(1):
        s = threading.Thread(target=demo, args=(i,))
        s.start()
        s.join()