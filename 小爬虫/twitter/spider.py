# -*- coding: utf-8 -*-
# @Time    : 2019/9/2 10:40
# @Author  : project
# @File    : spider.py
# @Software: PyCharm
import re
import os
import time
import logging
import datetime
import requests
from lxml import etree
from retrying import retry
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Spider:
    def __init__(self):
        print('*'*15, '程序启动', '*'*15)
        self.headers = {'user-agent': str(UserAgent().random)}
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
        desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
        desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        prefs = {"profile.managed_default_content_settings.images": 1}  # 1 加载图片 2不加载图片,加快访问速度
        options.add_experimental_option("prefs", prefs)
        # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # self.driver = webdriver.Chrome(chrome_options=options, desired_capabilities=desired_capabilities)
        self.driver = webdriver.Chrome(chrome_options=options)
        self.wait = WebDriverWait(self.driver, 5, 1)  # 设置隐式等待时间
        self.driver.maximize_window()  # 窗口最大化

    def get_basic(self):
        """
        获取基本信息: 发推数量、关注数、关注ID列表、粉丝数、
        :return:
        """
        url = 'https://twitter.com/ashrafghani'
        self.driver.get(url)
        # 登录账号
        input('账号登录')
        # 发布文章数量
        Twitter_num = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div/main/div/div/div/div[1]/div/div[1]/div/div/div/div/div/div[2]/div/div'))).text
        print(Twitter_num)
        # 关注人数 关注列表页url
        attention_num = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div/main/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div[5]/div[1]/a/span[1]'))).text
        print(attention_num)
        # attention_url = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div/main/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div[5]/div[1]/a/@href')))
        attention_url = 'https://twitter.com/ashrafghani/following'
        print(attention_url)
        # 粉丝
        fan = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div/main/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div[5]/div[2]/a/span[1]/span'))).text
        print(fan)

        print(f'账号：ashrafghani, 发布推特数量：{Twitter_num}, 关注人数：{attention_num}, 粉丝：{fan}')

        # 获取关注ID列表
        self.driver.get(attention_url)
        attention_id = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="react-root"]/div/div/div/main/div/div/div/div[1]/div/div[2]/section/div/div/div/div/div/div/div/div[2]/div[1]/div[1]/a/div/div[1]/div[1]/span/span')))
        attention_id = [i.text for i in attention_id]
        print(attention_id)


if __name__ == '__main__':
    spider = Spider()
    spider.get_basic()