# -*- coding: utf-8 -*-
# @Time    : 2019/8/23 15:53
# @Author  : project
# @File    : 123.py
# @Software: PyCharm



import json
import requests

proxies = json.loads(requests.get('http://47.102.109.169:4006/getProxy/?dataTag=vps&num=1&verify=1033383881').text)[0]

print(proxies)