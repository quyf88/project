# coding=utf-8
# 作者    ： Administrator
# 文件    ：spider.py
# IED    ：PyCharm
# 创建时间 ：2019/8/22 19:02
import csv
import json
import time
import requests
from fake_useragent import UserAgent


def spider():
    headers = {'User-Agent': str(UserAgent().random),
               # 必须加上此参数 不然获取不到信息
               'referer': 'https://item.jd.com/100006808184.html'}

    for i in range(800, 809):
        url = 'https://www.gtja.com/cos/rest/margin/path/fuzzy.json?jsonpcallback=jQuery183024945537511842475_1566471836497&pageCount=10&pageNum={}&type=1&_=1566471836635'.format(i)
        print('第[{}]页评论 开始爬取'.format(i+1))
        response = requests.get(url, headers=headers)
        # response = requests.get(url, headers=headers, verify=False)
        html = response.content.decode('utf-8')
        html = html.replace('jQuery183024945537511842475_1566471836497(', '').replace(');', '')
        con_json = json.loads(html)
        offsets = con_json['offset']
        for offset in offsets:
            print(offset)


if __name__ == '__main__':
    spider()