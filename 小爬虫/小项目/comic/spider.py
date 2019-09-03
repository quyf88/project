# -*- coding: utf-8 -*-
# @Time    : 2019/9/2 10:40
# @Author  : project
# @File    : spider.py
# @Software: PyCharm
import re
import os
import requests
from lxml import etree
from retrying import retry
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait


class Spider:
    def __init__(self):
        self.headers = {'user-agent': str(UserAgent().random),
                        }
        self.proxies = {
            "http": "http://127.0.0.1:1080",
            "https": "https://127.0.0.1:1080"
            }
        options = Options()
        # 设置代理
        desired_capabilities = webdriver.DesiredCapabilities.INTERNETEXPLORER.copy()
        desired_capabilities['proxy'] = {
            "httpProxy": "https://127.0.0.1:1080",
            "proxyType": "MANUAL",  # 此项不可注释
        }
        # 使用无头模式
        # options.add_argument('headless')
        self.driver = webdriver.Chrome(chrome_options=options, desired_capabilities=desired_capabilities)
        self.wait = WebDriverWait(self.driver, 15, 1)  # 设置隐式等待时间
        self.driver.maximize_window()  # 窗口最大化

    def read_url(self):
        """
        读取配置文件
        :return:
        """
        with open('url.txt', 'r', encoding='utf-8') as f:
            for i in f.readlines():
                url = i.split()[0]
                yield url

    @retry(stop_max_attempt_number=3)
    def get_extract_all_url(self, url):
        """
        提取图片真实url
        :return:
        """
        print('提取详情url...')
        # url = 'https://www.toptoon.net/#contents_80268,7421'
        self.driver.get(url)
        response = self.driver.page_source
        tree = etree.HTML(response)
        div = tree.xpath('//*[@id="viewer_data"]/@src')[0]
        _url = 'https://www.toptoon.net/' + div
        print('成功提取详情url:{}'.format(div))
        return _url

    @retry(stop_max_attempt_number=3)
    def get_image_url(self, url):
        """
        获取图片URL
        :return: 文件夹名称,图片url列表
        """
        # 效验IP
        res = requests.get("http://httpbin.org/ip", headers=self.headers, proxies=self.proxies, verify=False, timeout=10).json()
        ip = str(res['origin']).split(',')
        print('代理添加成功IP：{}'.format(ip))
        # url = 'https://toptoon.net/comic/episode_view?episode_idx=27356'
        # 提取项目文件夹名称
        id = re.findall(r'episode_idx=(.*?)$', url)[0]

        response = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=10).text
        result = etree.HTML(response)
        image_url_list = result.xpath('//*[@id="viewer_body"]/div/div[1]/div')
        url_list = []
        for i in image_url_list:
            image_url = i.xpath('./img/@src')[0]
            url_list.append(image_url)

        return id, url_list

    @retry(stop_max_attempt_number=3)
    def get_image(self, id, url_list):
        """
        下载图片
        :return:
        """
        path = 'image/' + str(id)

        if not os.path.exists(path):
            os.mkdir(path)
        for i in range(len(url_list)):
            url = 'http:' + url_list[i]
            # print(url)
            response = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=10)
            # print(response.status_code)
            image_path = path + '/' + str(i) + '.png'
            with open(image_path, 'wb') as image_content:
                image_content.write(response.content)
                print('图片 {} 保存成功!'.format(i+1))

    def run(self):
        for url in self.read_url():
            _url = self.get_extract_all_url(url)
            print(url + '图片下载中...')
            id, url_list = self.get_image_url(_url)
            self.get_image(id, url_list)


if __name__ == '__main__':
    spider = Spider()
    spider.run()


# https://www.toptoon.net/#contents_80755
# dspwb20190808@outlook.com
# Ddqqw333e123@#!!U