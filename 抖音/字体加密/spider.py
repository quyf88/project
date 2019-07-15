# -*- coding: utf-8 -*-
# @Time    : 2019/7/15 10:21
# @Author  : project
# @File    : spider.py
# @Software: PyCharm
import re
import requests
from retrying import retry
from fontTools.ttLib import TTFont
from fake_useragent import UserAgent


class Spider:
    def get_bast_cmap(self):
        """
        字体处理
        :return: 字体加密映射表
        """
        # 读取字体文件
        ttfont = TTFont('iconfont_9eb9a50.woff')
        # 保存成xml文件
        # ttfont.saveXML('iconfont_9eb9a50.xml')
        # 读取映射表 映射网页中的加密的字符串
        bast_cmap = ttfont['cmap'].getBestCmap()

        # hex转为十六进制
        new_bast_cmap = {}
        for key, value in bast_cmap.items():
            new_bast_cmap[hex(key)] = value
        return new_bast_cmap

    def get_num_cmap(self):
        """
        num 和真正数字的映射关系
        :return:
        """
        num_map = {
            'x': '',
            'num_': '1',
            'num_1': '0',
            'num_2': '3',
            'num_3': '2',
            'num_4': '4',
            'num_5': '5',
            'num_6': '6',
            'num_7': '9',
            'num_8': '7',
            'num_9': '8',
        }

        return num_map

    def map_cmap_num(self, get_bast_cmap, get_num_cmap):
        """
        构造最终加密映射表
        :return:
        """
        result = {}
        for key, value in get_bast_cmap().items():
            key = re.sub('0', '&#', key, count=1) + ';'
            result[key] = get_num_cmap()[value]
        return result

    @retry(stop_max_attempt_number=3)
    def get_html(self, url):
        """
        获取网页源码
        :param url:
        :return:
        """
        headers = {"User-Agent": UserAgent().random}
        while True:
            try:
                response = requests.get(url, headers=headers, timeout=3)
            except Exception as e:
                print(e)
                continue
            return response.text

    def replace_num_and_cmap(self, result, response):
        """
        替换网页源代码中的加密字符替换为真正的字符
        :param result: 加密字符映射表
        :param response: 网页源代码
        :return:
        """
        for key, value in result.items():
            if key in response:
                response = re.sub(key, value, response)
        return response

    def save_to_file(self, response):
        """
        保存网页成HTML
        :param response:
        :return:
        """
        with open('douyin.html', 'w', encoding='utf-8') as f:
            f.write(response)
            f.seek()
    def run(self, url):
        # 最终映射关系表
        result = self.map_cmap_num(self.get_bast_cmap, self.get_num_cmap)
        # 请求网页
        response = self.get_html(url)
        # 替换网页中加密字符为真实字符
        response = self.replace_num_and_cmap(result, response)
        # 保存HTML网页 方便提取
        self.save_to_file(response)


if __name__ == '__main__':
    url = 'https://www.iesdouyin.com/share/user/93763913776?u_code=10k31chi7&sec_uid=MS4wLjABAAAAnzRLpvV9w2jXzWhHSsG5D4SoqfYazU1-fvgm4joaHXQ&timestamp=1563157689'
    spider = Spider()
    spider.run(url)