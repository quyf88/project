# -*- coding: utf-8 -*-
# @Time    : 2019/5/27 9:23
# @Author  : project
# @File    : get_news.py
# @Software: PyCharm


import re
import time
import requests
import platform
from lxml import etree
from urllib.parse import quote
from retrying import retry
from 关键词搜索新闻.My_SQL import MySql


class SearchNews:
    def __init__(self, words):
        self.words = words
        self.headers = {'User-Agent':
                        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                        ' Chrome/68.0.3440.106 Safari/537.36 '
                        }

    @retry(stop_max_attempt_number=3)  # 如果请求超时让被装饰的函数反复执行三次，三次全部报错才会报错
    def _parse_url(self, url):

        # 随机获取一个请求头
        # headers = GetUserAgent().user_agent_list()
        try:
            response = requests.get(url, headers=self.headers, timeout=3)  # 3秒无响应报错
            result = response.content.decode()
        except:
            result = None

        return result

    def baidu_news(self):
        """百度新闻"""
        url = 'https://www.baidu.com/s?ie=utf-8&cl=2&rtt=1&bsst=1&rsv_dl=news_t_sk&tn=news&word=' + quote(self.words)
        content = self._parse_url(url)
        etree_html = etree.HTML(content)

        # 提取数据并处理
        data = []
        total = etree_html.xpath('//div[@id="header_top_bar"]/span/text()')  # 新闻总条数
        results = etree_html.xpath("//div[@class='result']")
        for result in results:
            fields = {}
            fields['keyword'] = self.words  # 关键词
            fields['url'] = result.xpath("./h3/a/@href")  # url
            tag = ''.join(result.xpath("./div/p/text()")).split()  # 来源 发布日期
            fields['tag'] = ''.join(tag)
            summary = ''.join(result.xpath("./div/text()")).split()  # 新闻摘要
            fields['summary'] = ''.join(summary)
            fields['source'] = '百度新闻'

            data.append(fields)

        return data

    def main(self):
        baidu = self.baidu_news()
        for i in baidu:
            fe = MySql()
            fe.create(i)


if __name__ == '__main__':
    wd = input('输入关键词：')
    news = SearchNews(wd)
    news.main()


