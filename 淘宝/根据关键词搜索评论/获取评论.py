# -*- coding: utf-8 -*-
# @Time    : 2019/7/24 14:49
# @Author  : project
# @File    : 获取评论.py
# @Software: PyCharm

import re
import os
import time
import urllib3
import requests
import configparser
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

urllib3.disable_warnings()


class Spider(object):
    def __init__(self):
        self.cookie = ''
        self.token = ''

        chrome_options = Options()
        desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
        desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        '''设置浏览器是否显示图片'''
        prefs = {"profile.managed_default_content_settings.images": 1}
        chrome_options.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.wait = WebDriverWait(self.driver, 30, 0.5)
        self.driver.maximize_window()

    def login_by_scan(self):
        print("开始登录,请等待页面加载完成后,扫码登录...")
        self.driver.get('https://login.taobao.com/member/login.jhtml?redirectURL=https://www.taobao.com/')
        while True:
            if 'data' in self.driver.current_url:
                print("等待扫码中...")
                time.sleep(5)
            if 'login.taobao.com' not in self.driver.current_url:
                print("登录成功")
                break
            else:
                print("等待扫码中...")
                time.sleep(5)

    def main(self):
        # 获取登入token
        # html = self.driver.page_source.replace(' ', '').replace("'", '"')
        # print(html)
        # try:
        #     self.token = re.findall('tokenValue:"(.*?)"', html, re.I | re.S)[0]
        #     print("获取此商家登陆状态的token成功, token:[{}]".format(self.token))
        # except Exception as ex:
        #     print("获取此商家登陆状态的token失败, 原因:[{}], 请联系管理员!!!".format(ex))
        #     return None
        self.driver.get
        for k in self.driver.get_cookies():
            self.cookie += '{}={}; '.format(k['name'], k['value'])
        print("获取此商家登陆状态的cookie成功, token:[{}]".format(self.cookie))

    def get_data(self):
        url = 'https://aldcdn.tmall.com/recommend.htm?itemId=545020495706&categoryId=50013151&sellerId=704392951&shopId=66674010&brandId=31128&refer=https%3A%2F%2Fs.taobao.com%2Fsearch%3Fq%3D%25E7%25A1%25AC%25E7%259B%2598%26imgfile%3D%26js%3D1%26stats_click%3Dsearch_radio_all%253A1%26initiative_id%3Dstaobaoz_20190724%26ie%3Dutf8&brandSiteId=0&rn=&appId=03054&isVitual3C=false&isMiao=false&count=12&callback=jsonpAld03054'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3710.0 Safari/537.36',

            'cookie': self.cookie
        }

        res1 = requests.get(url, headers=headers)
        html = res1.text
        print(html)
        if '请登录' in html:
            print('获取到的cookie错误，请重新登陆！')
            return



    def run(self):
        self.login_by_scan()
        self.main()
        self.get_data()


if __name__ == '__main__':
    spider = Spider()
    spider.run()