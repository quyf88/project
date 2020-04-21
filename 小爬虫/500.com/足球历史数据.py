# -*- coding:utf-8 -*-
# 文件 ：足球历史数据.py
# IED ：PyCharm
# 时间 ：2020/4/18 0018 15:18
# 版本 ：V1.0
import os
import requests
from lxml import etree
from retrying import retry
from fake_useragent import UserAgent

from requests_html import HTMLSession

print(os.path.abspath(__file__))  # 当前文件绝对路径
PATH = os.getcwd()  # 文件路径


@retry(stop_max_attempt_number=3)
def caipiao():
    headers = {"User-Agent": UserAgent().random}
    url = 'https://odds.500.com/fenxi/yazhi-921815.shtml'
    res = requests.get(url, headers=headers, timeout=30)
    print(res.status_code)
    # print(res.content.decode('GBK'))
    html = etree.HTML(res.content.decode('GBK'))
    # print(html)
    trs = html.xpath('//div[@id="table_cont"]/table/tr')
    print(trs)
    for tr in trs:
        content = tr.xpath('.//text()')
        content = [i.replace('\r\n', '').replace('\t', '').replace(' ', '') for i in content]
        content = [i for i in content if i]
        print(content)

    # text = [i.replace('\r\n', '').replace('\t', '').replace(' ', '') for i in text]
    # text = [i for i in text if i]
    # print(text)


if __name__ == '__main__':
    caipiao()



    'https://live.500.com/wanchang.php?e=2020-04-02'  # 历史数据