# coding=utf-8
# 作者    ： Administrator
# 文件    ：requests常用语法.py
# IED    ：PyCharm
# 创建时间 ：2019/7/27 15:18

import requests
"""
headers 请求头
proxies 代理
verify  忽略SSL提示
timeout 请求等待时间
"""

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0'}
proxies = {
    "http": "http://127.0.0.1:8888",
    "https": "http://127.0.0.1:8888",
}
response = requests.get('url', headers=headers, proxies=proxies, verify=False, timeout=3)
# status_code 请求返回状态码
code = response.status_code