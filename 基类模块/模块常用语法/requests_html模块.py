# -*- coding:utf-8 -*-
# 文件 ：requests_html模块.py
# IED ：PyCharm
# 时间 ：2020/3/4 0004 2:17
# 版本 ：V1.0
from requests_html import HTMLSession
"""
requests_html 常用语法
"""


def test():
    url = 'https://by.tuhu.cn/baoyang/VE-AADA3AD/pl1.4T(35TFSI)-n2015.html'
    # 建立Session 用完后一定要关闭 负责容易卡死
    session = HTMLSession()
    # 请求链接 verify=False移除SSL认证后会有警告提示
    # 禁用安全请求警告：
    # from requests.packages.urllib3.exceptions import InsecureRequestWarning
    # requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    r = session.get(url, verify=False)
    # 加载JavaScript，在Chromium里重新加载响应，并用最新获取到的HTML替换掉原来的HTML  首次使用，自动下载chromium
    # https://cncert.github.io/requests-html-doc-cn/#/?id=render 中文文档
    # retries重试三次 wait等待一秒加载数据
    print('加载javascript')
    r.html.render(retries=5, wait=3)
    # xpath 定位元素 first=True返回第一个Element对象 False返回所有对象
    dosage = r.html.xpath('//p[@class="pack_tt2"]', first=True)
    # dosage.text 提取Element对象中的文本
    dosage = dosage.text.strip('（').strip('）')
    # print(r.html.html)  # 打印网页源码
    # 关闭session连接
    session.close()
