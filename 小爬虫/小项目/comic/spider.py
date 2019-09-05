# -*- coding: utf-8 -*-
# @Time    : 2019/9/2 10:40
# @Author  : project
# @File    : spider.py
# @Software: PyCharm
import re
import os
import time
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
        # desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
        # desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        prefs = {"profile.managed_default_content_settings.images": 1}  # 1 加载图片 2不加载图片,加快访问速度
        options.add_experimental_option("prefs", prefs)
        # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(chrome_options=options, desired_capabilities=desired_capabilities)
        self.wait = WebDriverWait(self.driver, 40, 1)  # 设置隐式等待时间
        self.driver.maximize_window()  # 窗口最大化

        self.path_name = None
        self.num = None

    def login(self):
        count = 1
        while True:
            url = 'https://www.toptoon.net'
            self.driver.get(url)
            login = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="topmenu_mini"]/span[1]')))
            if login.text != '登入':
                continue
            login.click()
            # 账号密码
            user_id = self.wait.until(EC.presence_of_element_located((By.ID, 'user_id')))
            user_id.send_keys('1033383881@qq.com')
            user_pw = self.driver.find_element_by_id('user_pw')
            user_pw.send_keys('chenxiaoli2013')
            self.driver.find_element_by_xpath('//*[@id="alert_data"]/div[6]/span').click()
            if count > 3:
                print('账号登录失败,联系开发者!')
                self.driver.quit()
                os._exit(0)
            try:
                self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="mypage_data"]/table/tbody/tr/td/div[1]/div/p')))
            except:
                print('登录失败,重试!!!')
                count += 1
                self.driver.quit()
                continue
            print('登录成功')
            return

    def read_url(self):
        """
        读取配置文件
        :return:
        """
        with open('config/url.txt', 'r', encoding='utf-8') as f:
            for i in f.readlines():
                url = i.split()[0]
                yield url

    def get_image_page(self, url):
        """
        获取漫画信息
        :return:
        """
        self.driver.get(url)
        # 总章数
        total = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="page"]/table[2]/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr/td[1]/div/div')))
        print(len(total))
        total = str(len(total) - 1)
        print('总章数：{}'.format(total))
        # 文章名
        article_name = self.driver.find_element_by_css_selector('#tab1_board > div > div:nth-child(1)').text
        print('文章名：{}'.format(article_name))
        # 文章简介
        summary = self.driver.find_element_by_xpath('//*[@id="tab1_board"]/div/div[2]').text
        summary = summary.replace('\n', '').replace(' ', '')
        print('文章简介：{}'.format(summary))
        data = [url, article_name, total, summary]
        return data

    def validation(self, data):
        """
        效验是否更新
        :return:
        """
        url, article_name, total, summary = data
        # 写入文件
        path = 'image/' + str(article_name)
        path_name = path + '/' + article_name + '.txt'
        self.path_name = path + '/' + article_name
        if not os.path.exists(path):
            os.mkdir(path)
            self.num = int(total)
            print('{}：首次获取 共：{} 条 下载图片中...'.format(article_name, total))
        if os.path.exists(path_name):
            with open(path_name, 'r', encoding='utf-8')as f:
                content = f.read().split(',')
                content = [i for i in content if i]
            print(content[2], total)
            if content[2] == total:
                print('没有更新')
                return False
            self.num = int(total) - int(content[2])
            print('{}：数据更新 {} 条 下载图片中...'.format(article_name, self.num))

        with open(path_name, 'w+', encoding='utf-8') as f:
            for i in data:
                f.write(i)
                f.write(',')
        # 写入更新记录
        self.update_record(article_name)
        return True

    def update_record(self, article_name):
        """
        更新记录
        :return:
        """
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        filename = date + '更新记录.txt'
        with open(filename, 'a+', encoding='utf-8') as f:
            f.seek(0)
            print(article_name, f.read())
            if article_name not in f.readlines():
                f.write(article_name)
                f.write('\n')

    def chapter_details(self):
        """
        获取章节编号拼接详情页面url
        :return: 详情url
        """
        details = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="page"]/table[2]/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr/td[1]/div/div')))
        details_url = []
        for i in range(1, self.num+1):
            # 获取章节标签源码
            html = details[i].get_attribute('innerHTML')
            # print(html)
            # 提取章节ID 拼接详情url
            id = re.findall(r'episode_click(.*?),', html, re.S | re.M)
            # 提取章节
            chapter = re.findall(r'第(.*?)話', html)
            # 提取金额
            coupon = re.findall(r'&nbsp;(.*?)&nbsp;</span>', html)
            if not id:
                continue
            id = ''.join(re.findall(r'(\d)', id[0]))

            url = 'https://www.toptoon.net/comic/episode_view?episode_idx=' + str(id)
            details_url.append(url)
        print(details_url)
        return details_url

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
        print(response)
        return
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
        # res = requests.get("http://httpbin.org/ip", headers=self.headers, proxies=self.proxies, verify=False, timeout=10).json()
        # ip = str(res['origin']).split(',')
        # print('代理添加成功IP：{}'.format(ip))
        # url = 'https://toptoon.net/comic/episode_view?episode_idx=27356'
        # 提取项目文件夹名称
        response = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=10).text
        result = etree.HTML(response)
        image_url_list = result.xpath('//*[@id="viewer_body"]/div/div[1]/div')
        url_list = []
        for i in image_url_list:
            image_url = i.xpath('./img/@src')[0]
            url_list.append(image_url)

        return url_list

    @retry(stop_max_attempt_number=3)
    def get_image(self, url_list):
        """
        下载图片
        :return:
        """
        for i in range(len(url_list)):
            url = 'http:' + url_list[i]
            # print(url)
            response = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=10)
            # print(response.status_code)
            image_path = self.path_name + '/' + str(i) + '.png'
            with open(image_path, 'wb') as image_content:
                image_content.write(response.content)
                print('图片 {} 保存成功!'.format(i+1))

    def run(self):
        self.login()  # 登录
        # 配置文件读取url
        for url in self.read_url():
            # 获取漫画详细信息
            data = self.get_image_page(url)
            # 判断是否更新
            if not self.validation(data):
                continue
            # 提取更新章节url
            details_url = self.chapter_details()
            for new_url in details_url:
                # 获取图片url
                url_list = self.get_image_url(new_url)
                # 下载图片
                self.get_image(url_list)



if __name__ == '__main__':
    spider = Spider()
    spider.run()



# https://www.toptoon.net/#contents_80755
# dspwb20190808@outlook.com
# Ddqqw333e123@#!!U