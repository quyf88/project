# -*- coding: utf-8 -*-
# @Time    : 2019/7/3 13:38
# @Author  : project
# @File    : spider.py
# @Software: PyCharm

import json
import requests
from lxml import etree
from retrying import retry
from fake_useragent import UserAgent


class Spider:
    def __init__(self):
        # 获取随机请求头
        self.headers = {"User-Agent": UserAgent().random}

    @retry(stop_max_attempt_number=3)
    def _parse_url(self, url):
        """请求函数"""
        try:
            response = requests.get(url, headers=self.headers, timeout=3)
        except Exception as e:
            print(e)
            response = None
        return response

    def get_model_list(self):
        """获取所有车型列表"""
        # 所有车型js文件
        url = 'https://car.autohome.com.cn/javascript/NewSpecCompare.js?20131010'
        response = self._parse_url(url)
        # GBK解码
        content = response.content.decode('GBK')
        # 剔除开头和结尾处多余字符 转换为json
        content = content.replace('var listCompare$100= ', '').replace(';', '')
        content = json.loads(content)
        for i in content:
            # 品牌首字母,名称,车系列表
            brand_l, brand_n, brand_list,  = i['L'], i['N'], i['List']
            for q in brand_list:
                # 车系名称,车型列表
                car_l, car_list = q['N'], q['List']
                for t in car_list:
                    # 车型ID, 车型名称
                    model_l = t['I']
                    model_n = t['N']
                    yield brand_l, brand_n, car_l, model_n, model_l


if __name__ == '__main__':
    spider = Spider()
    spider.get_model_list()