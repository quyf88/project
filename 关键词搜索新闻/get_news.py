# -*- coding: utf-8 -*-
# @Time    : 2019/5/27 9:23
# @Author  : project
# @File    : get_news.py
# @Software: PyCharm


import requests
import platform
import re
from lxml import etree
from urllib.parse import quote


SYSTEM = platform.system()  # 得到系统信息


def get_baidu_news(wd):
    """百度新闻"""
    url = 'https://www.baidu.com/s?ie=utf-8&cl=2&rtt=1&bsst=1&rsv_dl=news_t_sk&tn=news&word=' + quote(wd)
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 '
                      'Safari/537.36 '
    }
    response = requests.get(url, headers=headers)
    content = response.content.decode()
    etree_html = etree.HTML(content)

    # 提取数据并处理
    data = []
    total = etree_html.xpath('//div[@id="header_top_bar"]/span/text()')  # 新闻总条数
    results = etree_html.xpath("//div[@class='result']")
    for result in results:
        fields = {}
        fields['url'] = result.xpath("./h3/a/@href")[0]  # url
        fields['tag'] = ''.join(result.xpath("./div/p/text()")).split()  # 来源 发布日期
        summary = ''.join(result.xpath("./div/text()")).split()  # 新闻摘要
        fields['summary'] = ''.join(summary)
        data.append(fields)

    return total, data


def main():
    wd = input('输入关键词：')
    print(get_baidu_news(wd))


if __name__ == '__main__':
    main()


