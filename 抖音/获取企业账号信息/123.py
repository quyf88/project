# -*- coding:utf-8 -*-
# 文件 ：123.py
# IED ：PyCharm
# 时间 ：2019/10/30 0030 16:37
# 版本 ：V1.0

import json


def response(flow):
    url = 'https://aweme-hl.snssdk.com/aweme/v1/discover/search'
    # 筛选出以上面url为开头的url
    print(123)
    print('123')
    if flow.request.url.startswith(url):
        text = flow.response.text
        # 将已编码的json字符串解码为python对象
        data = json.loads(text)
        print(data)
