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
from lxml import etree
import configparser
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
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
        self.comments_page = 0  # 评价页数
        chrome_options = Options()
        desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
        desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        '''设置浏览器是否显示图片'''
        prefs = {"profile.managed_default_content_settings.images": 1}
        chrome_options.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.wait = WebDriverWait(self.driver, 8, 0.5)
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
        for k in self.driver.get_cookies():
            self.cookie += '{}={}; '.format(k['name'], k['value'])
        print("获取此商家登陆状态的cookie成功, token:[{}]".format(self.cookie))

    def get_comments_page(self):
        """
        获取评论数量
        :return:
        """
        url = 'https://detail.tmall.com/item.htm?spm=a230r.1.14.41.63337042DAfSJS&id=521322201495&ns=1&abbucket=8'
        print(url)
        self.driver.get(url)
        # 获取当前商品名称
        product_name = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="tb-detail-hd"]/h1'))).text
        # 屏幕向下滑动
        self.driver.execute_script("window.scrollBy(0,800)")
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//ul[@id="J_TabBar"]/li[2]'))).click()
        time.sleep(3)
        # 当前商品评论总数
        comments_num = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="J_TabBarBox"]/ul/li[2]/a/em'))).text

        # 评论总页数
        self.comments_page = int(int(comments_num) / 20 - 1)
        print('商品：{} 累计评价：{} 共{}页'.format(product_name, self.comments_page, comments_num))

    def get_comments_html(self):
        """
        获取评论信息 保存为html
        :return:
        """
        comments = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="J_Reviews"]')))
        for _ in range(self.comments_page):
            time.sleep(1)  # 防止请求过快数据加载不出来 不加睡眠数据会有重复现象
            comments_html = comments.get_attribute('innerHTML')
            print('----------第[{}]页评价获取中----------'.format(_+1))
            name = 'html/content' + str(_ + 1) + '.html'
            with open(name, 'w', encoding='utf-8') as f:
                f.write(comments_html)
            # //a[contains(text(), "下一页")] 根据标签文本内容定位标签
            print('下一页')
            time.sleep(1)
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "下一页")]'))).click()

    def deal_html(self):
        """
        从html文件中读取数据 保存至文件
        :return:
        """
        with open('content.html', 'r', encoding='utf-8') as f:
            content = f.read()

        result = etree.HTML(content)
        # 当前商品评论总数
        comments_num = result.xpath('//h4[@class="hd"]/em/text()')[0]
        # 评论总页数
        comments_page = int(int(comments_num) / 20)
        # 评论详情
        comments_con = result.xpath('//div[@class="rate-grid"]/table/tbody/tr')
        for comments in comments_con:
            content = comments.xpath('.//div[@class="tm-rate-fulltxt"]//text()')
            # 购买商品
            product_spec = comments.xpath('.//div[@class="rate-sku"]//text()')
            product_spec = ''.join(product_spec)
            # 评论时间
            rate_time = comments.xpath('.//div[@class="tm-rate-date"]//text()')
            rate_time = ''.join(rate_time)
            # 用户名
            user_name = comments.xpath('.//div[@class="rate-user-info"]//text()')
            user_name = ''.join(user_name)
            print(content, product_spec, user_name, rate_time)

    def run(self):
        # self.login_by_scan()
        # self.main()
        self.get_comments_page()
        self.get_comments_html()


if __name__ == '__main__':
    spider = Spider()
    spider.run()


