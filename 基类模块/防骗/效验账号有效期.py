# -*- coding:utf-8 -*-
# 文件 ：效验账号有效期.py
# IED ：PyCharm
# 时间 ：2019/12/13 0013 12:43
# 版本 ：V1.0
import os
import requests


def proxy():
    url = 'http://www.dongdongmeiche.com/proxy/460a23180f3411ea9aec28d2447ab52e'
    response = requests.get(url)
    content = response.json()
    code = content['errorcode']
    if code != 10001:
        print(content['context'])
        os._exit(0)
    print(content['context'])


if __name__ == '__main__':
    proxy()
