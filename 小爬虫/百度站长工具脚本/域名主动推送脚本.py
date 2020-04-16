# -*- coding:utf-8 -*-
# 文件 ：域名主动推送脚本.py
# IED ：PyCharm
# 时间 ：2020/4/16 0016 14:18
# 版本 ：V1.0
import os
import requests
from retrying import retry

print(os.path.abspath(__file__))  # 当前文件绝对路径
PATH = os.getcwd()  # 文件路径


class BaiduLinkSubmit:
    def __init__(self, sitemap_file, baidu_token):
        self.sitemap_file = sitemap_file
        self.baidu_token = baidu_token

    def read_sitemap(self):
        for line in open(self.sitemap_file, 'r', encoding='utf-8'):
            if line.replace('\n', ''):
                yield line.replace('\n', '')

    @retry(stop_max_attempt_number=10)
    def submit(self):
        for line in self.read_sitemap():
            url = f'http://data.zz.baidu.com/urls?site={line}&token={self.baidu_token}'
            headers = {
                'Content-Type': 'text/plain'
            }
            r = requests.post(url, headers=headers, data=line, timeout=10)
            data = r.json()
            print(f'推送成功：{line}')
            print('当天剩余的可推送url条数：%s' % data.get('remain', 0))


def main():
    # sitemap.xml的地址
    sitemap_file = 'config/域名.txt'
    # 百度站长平台的准入密匙
    baidu_token = 'Axl6rJaS6DnoMe9M'
    app = BaiduLinkSubmit(sitemap_file, baidu_token)
    app.submit()


if __name__ == '__main__':
    main()