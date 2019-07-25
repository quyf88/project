# -*- coding: utf-8 -*-
# @Time    : 2019/7/24 14:49
# @Author  : project
# @File    : 获取评论.py
# @Software: PyCharm

import os
import re
import csv
import time
from lxml import etree
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
        self.cookie = ''
        self.token = ''
        self.count = 0  # 写入计数
        self.commodity_id = []  # 搜索商品ID

        chrome_options = Options()
        desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
        desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        prefs = {"profile.managed_default_content_settings.images": 1}  # 1 加载图片 2不加载图片,加快访问速度
        chrome_options.add_experimental_option("prefs", prefs)
        # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.wait = WebDriverWait(self.driver, 8, 0.5)
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

    def login_by_weibo(self):
        """
        微博登录
        :return:
        """
        weibo_username = "18210836362"  # 改成你的微博账号
        weibo_password = "chenxiaoli2013"  # 改成你的微博密码
        url = 'https://login.taobao.com/member/login.jhtml'
        # 打开网页
        self.driver.get(url)

        # 等待 密码登录选项 出现
        password_login = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.qrcode-login > .login-links > .forget-pwd')))
        password_login.click()

        # 等待 微博登录选项 出现
        weibo_login = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.weibo-login')))
        weibo_login.click()

        # 等待 微博账号 出现
        weibo_user = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.username > .W_input')))
        weibo_user.send_keys(weibo_username)

        # 等待 微博密码 出现
        weibo_pwd = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.password > .W_input')))
        weibo_pwd.send_keys(weibo_password)

        # 等待 登录按钮 出现
        submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.btn_tip > a > span')))
        submit.click()
        # 直到获取到淘宝会员昵称才能确定是登录成功
        taobao_name = self.wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, '.site-nav-bd > ul.site-nav-bd-l > li#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-user > a.site-nav-login-info-nick ')))
        # 输出淘宝昵称
        print('账号：{}登录成功'.format(taobao_name.text))

    def get_cookie(self):
        """
        获取登录 cookie
        :return:
        """
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

    def search_words(self):
        """
        关键词搜索
        :return:
        """
        # words = input('输入关键词：')
        words = '硬盘'
        url = 'https://s.taobao.com/search?q={}&s={}'.format(quote(words), '0')
        self.driver.get(url)
        time.sleep(1)
        html = self.driver.page_source
        # 搜索结果 页数
        page = re.findall(r'共(.*?)页', html, re.S | re.M)
        print('关键词:{} 搜索结果 {} 页'.format(words, page))
        commodity_id = re.findall(r'data-nid="(.*?)"', html, re.S | re.M)
        self.commodity_id = list(set(commodity_id))
        print(len(self.commodity_id), self.commodity_id)
        # TODO
        # # 点击下一页
        # time.sleep(1)
        # url = 'https://s.taobao.com/search?q={}&s={}'.format(quote(words), '44')
        # self.driver.get(url)
        # print('点击下一页')

    def get_comments_page(self):
        """
        获取评论数量
        :return:
        """
        print(type(self.commodity_id))
        for commodity_id in self.commodity_id:
            url = 'https://detail.tmall.com/item.htm?id={}'.format(commodity_id)
            print(url)
            self.driver.get(url)
            time.sleep(1)
            # 获取当前商品名称
            product_name = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="tb-detail-hd"]/h1'))).text
            # 屏幕向下滑动
            self.driver.execute_script("window.scrollBy(0,800)")
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//ul[@id="J_TabBar"]/li[2]'))).click()
            time.sleep(5)
            # 当前商品评论总数
            comments_num = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//ul[@id="J_TabBar"]/li[2]/a/em'))).text

            # 评论总页数
            comments_page = int(int(comments_num) / 20 - 2)
            print('商品：{} 累计评价：{} 共{}页'.format(product_name, comments_num, comments_page))
            # 获取评论信息 保存为html
            self.get_comments_html(commodity_id, comments_page)

    def get_comments_html(self, commodity_id, comments_page):
        """
        获取评论信息 保存为html
        commodity_id 商品ID
        comments_page 评论总页数
        :return:
        """
        time.sleep(3)
        comments = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="J_Reviews"]')))
        for _ in range(comments_page):
            # 防止请求过快数据加载不出来 不加睡眠数据会有重复现象
            time.sleep(3)
            comments_html = comments.get_attribute('innerHTML')
            print('----------第[{}]页评价获取中----------'.format(_+1))
            path = 'html/' + commodity_id + '_' + '.html'
            with open(path, 'w', encoding='utf-8') as f:
                f.write(comments_html)
            self.deal_html()
            # //a[contains(text(), "下一页")] 根据标签文本内容定位标签
            print('----------第[{}]页评价保存成功----------'.format(_ + 1))
            # click 无法点击 切换send_keys(Keys.ENTER)
            to_dn = self.wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "下一页")]')))
            time.sleep(3)
            to_dn.send_keys(Keys.ENTER)

    def deal_html(self):
        """
        从html文件中读取数据 保存至文件
        :return:
        """
        path = os.listdir('html/')
        print(path)
        for name in path:
            with open('html/'+name, 'r', encoding='utf-8') as f:
                content = f.read()

            result = etree.HTML(content)
            # 评论详情
            comments_con = result.xpath('//div[@class="rate-grid"]/table/tbody/tr')
            for comments in comments_con:
                # 评论内容
                content = comments.xpath('.//div[@class="tm-rate-fulltxt"]//text()')[0]
                # 购买商品
                product_spec = comments.xpath('.//div[@class="rate-sku"]//text()')
                product_spec = ''.join(product_spec)
                # 评论时间
                rate_time = comments.xpath('.//div[@class="tm-rate-date"]//text()')
                rate_time = ''.join(rate_time)
                # 用户名
                user_name = comments.xpath('.//div[@class="rate-user-info"]//text()')
                user_name = ''.join(user_name)
                # 商品ID
                commodity_id = name.split('_')[0]
                # 抓取时间
                writertime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print(user_name, product_spec, commodity_id, content, rate_time, writertime)
                data = [user_name, product_spec, commodity_id, content, rate_time, writertime]
                # data = ([[user_name, product_spec, commodity_id, content, rate_time, writertime]])
                self.model_csv(data)

    def model_csv(self, data):
        """保存数据"""
        self.count += 1
        data = ','.join(data)
        with open('a.txt', 'a+', encoding='UTF-8') as f:
            f.write(data + '\n')
        # with open("demo.csv", "a+", encoding='GBK', newline="") as f:
        #     k = csv.writer(f, delimiter=',')
        #     with open("demo.csv", "r", encoding='GBK', newline="") as f1:
        #         reader = csv.reader(f1)
        #         if not [row for row in reader]:
        #             k.writerow(['用户名', '商品型号', '商品ID', '评论内容', '评论时间', '抓取时间'])
        #             k.writerows(data)
        #             print('第[{}]条数据插入成功'.format(self.count))
        #         else:
        #             k.writerows(data)
        #             print('第[{}]条数据插入成功'.format(self.count))

    def run(self):
        # self.login_by_scan()
        # self.main()
        self.login_by_weibo()
        self.search_words()
        self.get_comments_page()


if __name__ == '__main__':
    spider = Spider()
    spider.run()
    # spider.deal_html()


