# -*- coding:utf-8 -*-
# 文件 ：效验账号有效期.py
# IED ：PyCharm
# 时间 ：2019/12/13 0013 12:43
# 版本 ：V1.0
import os
import requests
import urllib.request


def proxy():
    url = 'http://www.dongdongmeiche.com/proxy/c237a07a57c44169bd20e18f73ab9e6'
    opener = urllib.request.build_opener()
    try:
        opener.open(url)
        fang = True
    except urllib.error.HTTPError:
        fang = False
    except urllib.error.URLError:
        fang = False
    if not fang:
        print('url validation failed!')
        os._exit(0)
    response = requests.get(url)
    content = response.json()
    code = content['errorcode']
    if code != 10001:
        print(content['context'])
        os._exit(0)
    print(content['context'])


if __name__ == '__main__':
    proxy()

