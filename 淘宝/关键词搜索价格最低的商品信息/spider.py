# -*- coding: utf-8 -*-
# @Time    : 2019/7/24 14:49
# @Author  : project
# @File    : 获取评论.py
# @Software: PyCharm

import os
import re
import csv
import time
import pandas as pd
from selenium import webdriver
from urllib.parse import quote
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Spider(object):
    def __init__(self):
        self.count = 0  # 写入计数

        chrome_options = Options()
        desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
        desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        prefs = {"profile.managed_default_content_settings.images": 1}  # 1 加载图片 2不加载图片,加快访问速度
        chrome_options.add_experimental_option("prefs", prefs)
        # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

        # 设置代理
        # desired_capabilities = webdriver.DesiredCapabilities.INTERNETEXPLORER.copy()
        # desired_capabilities['proxy'] = {
        #     "httpProxy": "https://127.0.0.1:1080",
        #     "proxyType": "MANUAL",  # 此项不可注释
        # }

        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.wait = WebDriverWait(self.driver, 60, 0.5)
        self.driver.maximize_window()

    def login_by_scan(self):
        """
        扫码登录
        :return:
        """
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
        # """
        # 微博登录
        # :return:
        # """
        # self.driver.get('https://login.taobao.com/member/login.jhtml')
        # weibo_username = "18210836362"  # 改成你的微博账号
        # weibo_password = "chenxiaoli2013"  # 改成你的微博密码
        # # 等待 密码登录选项 出现
        # password_login = self.wait.until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, '.qrcode-login > .login-links > .forget-pwd')))
        # password_login.click()
        #
        # # 等待 微博登录选项 出现
        # weibo_login = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.weibo-login')))
        # weibo_login.click()
        #
        # # 等待 微博账号 出现
        # weibo_user = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.username > .W_input')))
        # weibo_user.send_keys(weibo_username)
        #
        # # 等待 微博密码 出现
        # weibo_pwd = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.password > .W_input')))
        # weibo_pwd.send_keys(weibo_password)
        #
        # # 等待 登录按钮 出现
        # submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.btn_tip > a > span')))
        # submit.click()
        # while True:
        #     if 'login.taobao.com' not in self.driver.current_url:
        #         print("登录成功")
        #         # 直到获取到淘宝会员昵称才能确定是登录成功
        #         taobao_name = self.wait.until(EC.presence_of_element_located((
        #             By.CSS_SELECTOR,
        #             '.site-nav-bd > ul.site-nav-bd-l > li#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-user > a.site-nav-login-info-nick ')))
        #         # 输出淘宝昵称
        #         print('账号：{}登录成功'.format(taobao_name.text))
        #         break
        #     else:
        #         print("等待登录中...")
        #         time.sleep(5)
        #         continue

    def read_xls(self):
        """
        读取 XLS表格数据
        :return:
        """
        # 加载数据
        df_read = pd.read_excel('config/查询记录.xlsx')
        df = pd.DataFrame(df_read)
        # 获取指定表头的列数
        content = 0  # 数据列
        for i in range(len(df.keys())):
            if df.keys()[i] == '牌名':
                content = i
        for indexs in df.index:
            # 获取企业信息 查询用
            pre_name = df.ix[indexs, content]
            print(pre_name)
            yield (pre_name)

    def start_search_result(self, keys):

        self.driver.get('https://www.taobao.com/')

        # 给搜索框赋值
        kw = self.driver.find_element_by_id("q")  # q
        kw.send_keys(keys)

        # 模拟点击搜索按钮事件
        iconfont = self.driver.find_element_by_class_name('search-button')
        iconfont.click()

    def search_words(self):
        """
        关键词搜索
        :return:
        """
        count = 0
        for words in self.read_xls():
            # words = '万智牌全军覆灭'
            # sort=price-asc 按照价格从低到高排序
            self.start_search_result(words)
            url = f'https://s.taobao.com/search?q={quote(words)}&sort=price-asc'
            # print(url)
            # self.driver.get(url)
            html = self.driver.page_source
            commodity_id = re.findall(r'data-nid="(.*?)"', html, re.S | re.M)

            time.sleep(5)
            commodity_url = f'https://item.taobao.com/item.htm?ft=t&id={commodity_id[0]}'
            self.driver.get(commodity_url)
            print(commodity_url)

            # 店铺
            shop = self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="J_ShopInfo"]/div/div[1]/div[1]/dl/dd/strong/a'))).text
            # 金额
            money = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="J_StrPrice"]/em[2]'))).text
            if '-' in money:
                money = money.split('-')[0]
            # 标题
            title = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="J_Title"]/h3'))).text
            # 抓取时间
            writertime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(f'牌名:{words} 店名:{shop} 最低价:{money} 分类:{title} 时间:{writertime}')
            self.model_csv([[words, shop, money, title, writertime]])
            time.sleep(5)
            count += 1
            if not count % 10:
                print("程序等待60秒后继续运行：防止操作太快出错")
                time.sleep(30)

    def model_csv(self, data):
        """保存数据"""
        self.count += 1
        with open("demo.csv", "a+", encoding='GBK', newline="") as f:
            k = csv.writer(f, delimiter=',')
            with open("demo.csv", "r", encoding='GBK', newline="") as f1:
                reader = csv.reader(f1)
                if not [row for row in reader]:
                    k.writerow(['牌名', '店名', '最低价', '分类', '抓取时间'])
                    k.writerows(data)
                    print('第[{}]条数据插入成功'.format(self.count))
                else:
                    k.writerows(data)
                    print('第[{}]条数据插入成功'.format(self.count))

    def run(self):
        # self.login_by_scan()
        self.search_words()


if __name__ == '__main__':
    spider = Spider()
    spider.run()



