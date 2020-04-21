# -*- coding:utf-8 -*-
# 文件 ：自定义xpath框架.py
# IED ：PyCharm
# 时间 ：2020/4/18 0018 18:44
# 版本 ：V1.0
import os
import chardet
import requests
from lxml import etree
from retrying import retry
from fake_useragent import UserAgent

print(os.path.abspath(__file__))  # 当前文件绝对路径
PATH = os.getcwd()  # 文件路径


class XpathFrame:
    def __init__(self, url, xpath, enconding=None, results=list()):
        self.url = url  # 网页url
        self.xpath = xpath  # xpath语句
        self.enconding = enconding  # 网页编码格式
        self.results = results

    @retry(stop_max_attempt_number=5)
    def _parse_url(self):
        """url请求"""
        count = 0
        headers = {"User-Agent": UserAgent().random}
        while count < 3:
            try:
                response = requests.get(self.url, headers=headers, allow_redirects=False, timeout=10)
                # print(response.content, len(response.text), type(response.text))
                if not response:
                    count += 1
                    continue
                return response.content
            except Exception as e:
                print('出错了')
                print(e)
                return False

    def _if_result_none(self, result):
        """检测是否有数据"""
        print('判断是否有数据')
        if not result:
            return False
        return True

    def _web_encoding(self, content):
        """提取网页编码格式"""
        print('提取网页编码格式')
        if not chardet.detect(content).get('encoding'):
            self.enconding = 'UTF-8'
            return
        self.enconding = chardet.detect(content).get('encoding')

    def _position_xpath(self, html):
        """提取xpath"""
        results = etree.HTML(html).xpath(self.xpath)
        if not results:
            print('没有提取到信息!')
            return False
        for result in results:
            if isinstance(result, str):
                self.results.append(result)
                continue
            if result.text:
                content = result.xpath('.//text()')
                self.results.append(self._data_utilclass(content))
                continue
            self.results.append(self._etree_tostring(result))

    def _data_utilclass(self, content):
        """数据清洗"""
        content_1 = [i.replace('\r\n', '').replace('\t', '').replace(' ', '') for i in content]
        content_2 = [i for i in content_1 if i]
        return content_2

    def _etree_tostring(self, etree_element):
        """lxml.etree对象转换为字符串"""
        html_str = etree.tostring(etree_element, encoding=self.enconding).decode()
        return html_str

    def run(self):
        # 请求数据
        content = self._parse_url()
        if not self._if_result_none(content):
            print('没有数据')
            return False
        # 获取当前网页编码格式
        self._web_encoding(content)
        # 解析数据
        html = content.decode(encoding=self.enconding)
        # 提取xpath定位数据
        self._position_xpath(html)
        return self.results


def main():
    url = 'https://odds.500.com/fenxi/yazhi-921815.shtml'
    xpath = '//div[@id="table_cont"]/table/tr'
    s = XpathFrame(url, xpath)
    result = s.run()
    print(result)


if __name__ == '__main__':
    main()