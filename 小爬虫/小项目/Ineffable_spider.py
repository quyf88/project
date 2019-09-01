# coding=utf-8
# 作者    ： Administrator
# 文件    ：Ineffable_spider.py
# IED    ：PyCharm
# 创建时间 ：2019/8/31 14:36

import csv
import json
import re
import datetime
import requests
from fake_useragent import UserAgent


class Spider:
    def __init__(self):
        self.headers = {'user-agent': str(UserAgent().random),
                        'authority': 'cdn.av01.tv',
                        'method': 'GET',
                        'scheme': 'https',
                        'accept': '*/*',
                        'origin': 'https://www.av01.tv',
                        'referer': 'https://www.av01.tv/video/26791/ssni-452-%E4%B8%8B%E7%9D%80%E3%83%A2%E3%83%87%E3%83%AB%E3%82%92%E3%81%95%E3%81%9B%E3%82%89%E3%82%8C%E3%81%A6-%E3%83%95%E3%82%A7%E3%83%81%E3%82%BA%E3%83%A09%E3%83%A9%E3%83%B3%E3%82%B8%E3%82%A7%E3%83%AA%E3%83%BCspecial-%E4%B8%89%E4%B8%8A%E6%82%A0%E4%BA%9C',

                        }
        self.proxies = {
            "http": "http://127.0.0.1:1080",
            "https": "https://127.0.0.1:1080"
            }

    def get_m3u8(self):
        res = requests.get("http://httpbin.org/ip", headers=self.headers, proxies=self.proxies, verify=False, timeout=10).json()
        ip = str(res['origin']).split(',')
        print(ip)
        url = 'https://cdn.av01.tv/v2/20190423_2/ssni00452/content/index4500-v1.m3u8?hdnea=ip=5.180.77.47~st=1567340896~exp=1567427296~acl=/v2/20190423_2/ssni00452/content/*~hmac=a8823f45308c2c78ba8ac5e3ba92db8f3250cc323d8b69c81e485b17ef425053'
        response = requests.get(url, headers=self.headers, proxies=self.proxies)
        with open('url.txt', 'w+') as m3u8_content:
            m3u8_content.write(response.text)

    def get_url(self):
        # 提取ts视频的url
        movies_url = []
        _urls = open('url.txt', 'r')
        for line in _urls.readlines():
            if '.ts' in line:
                movies_url.append('https://cdn.av01.tv/v2/20190423_2/ssni00452/content/' + line)
            else:
                continue
        for url in movies_url:
            print(url)
            yield url

    def get_video(self, url):
        num = re.findall(r'file4500-(.*?)-v1', url)[0]
        start = datetime.datetime.now().replace(microsecond=0)
        path = re.findall(r'https://cdn.av01.tv(.*?)$', url)[0]
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
                    'authority': 'cdn.av01.tv',
                    'method': 'GET',
                    'scheme': 'https',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'zh-CN,zh;q=0.8',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   'upgrade-insecure-requests': '1',
                   'path': path,
                   'cookie': '__cfduid=d51d4f8402b30b97115433f1c2a6259861567336744; _ga=GA1.2.589604286.1567336753; _gid=GA1.2.1030744489.1567336753'

        }

        res = requests.get("http://httpbin.org/ip", headers=headers, timeout=10).json()
        ip = str(res['origin']).split(',')
        print(ip)
        while True:
            try:
                response = requests.get(url, headers=headers, proxies=self.proxies)
                print(response.status_code)
                if response.status_code != 200:
                    continue
            except Exception as e:
                print("异常请求：%s" % e.args)
                return
            break
        ts_path = 'video/{}.ts'.format(num)
        with open(ts_path, "wb+") as file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    file.write(chunk)
        end = datetime.datetime.now().replace(microsecond=0)
        print("{} 下载完成 耗时：{}".format(ts_path, end - start))

    def run(self):
        # self.get_m3u8()
        for url in self.get_url():
            self.get_video(url)


if __name__ == '__main__':
    spider = Spider()
    spider.run()