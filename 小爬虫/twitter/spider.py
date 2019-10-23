# -*- coding: utf-8 -*-
# @Time    : 2019/9/2 10:40
# @Author  : project
# @File    : spider.py
# @Software: PyCharm
import re
import csv
import time
import pandas as pd
from datetime import datetime
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def run_time(func):
    def new_func(*args, **kwargs):
        start_time = datetime.now()
        print("程序开始时间：{}".format(start_time))
        func(*args, **kwargs)
        end_time = datetime.now()
        print("程序结束时间：{}".format(end_time))
        print("程序执行用时：{}s".format((end_time - start_time)))

    return new_func


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
        prefs = {"profile.managed_default_content_settings.images": 2}  # 1 加载图片 2不加载图片,加快访问速度
        options.add_experimental_option("prefs", prefs)
        # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # self.driver = webdriver.Chrome(chrome_options=options, desired_capabilities=desired_capabilities)
        self.driver = webdriver.Chrome(chrome_options=options)
        self.wait = WebDriverWait(self.driver, 5, 1)  # 设置隐式等待时间
        self.driver.maximize_window()  # 窗口最大化

        self.count = 1

    def read_xls(self):
        """
        读取 表格数据
        :return:
        """
        print('读取配置文件')
        # 加载数据
        df_read = pd.read_excel('config/用户id列表.xlsx')
        df = pd.DataFrame(df_read)
        # 获取指定表头的列数
        ID = 0
        for i in range(len(df.keys())):
            if df.keys()[i] == 'ID':
                ID = i
        for indexs in df.index:
            # 读取指定行列数据 df.ix[行,列]
            data = df.ix[indexs, ID]
            yield data

    def get_basic(self, acc_id):
        """
        获取基本信息: 推文数量、关注数、关注ID列表、粉丝数
        :return:
        """
        url = f'https://twitter.com/{acc_id}'
        self.driver.get(url)
        # 登录账号
        input('账号登录')
        # 发布文章数量
        Twitter_num = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div/main/div/div/div/div[1]/div/div[1]/div/div/div/div/div/div[2]/div/div'))).text
        # print(Twitter_num)
        # 关注人数 关注列表页url
        attention_num = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div/main/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div[5]/div[1]/a/span[1]'))).text
        # print(attention_num)
        # attention_url = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div/main/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div[5]/div[1]/a/@href')))
        attention_url = 'https://twitter.com/ashrafghani/following'
        # print(attention_url)
        # 粉丝
        fan = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div/main/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div[5]/div[2]/a/span[1]/span'))).text
        # print(fan)
        print(f'账号：{acc_id}, 发布推特数量：{Twitter_num}, 关注人数：{attention_num}, 粉丝：{fan}')

        # 获取关注ID列表
        self.driver.get(attention_url)
        time.sleep(3)
        # 获取body的高度，滑到底部
        scroll = "window.scrollTo(0,document.body.scrollHeight)"
        self.driver.execute_script(scroll)

        attentions_id = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="react-root"]/div/div/div/main/div/div/div/div[1]/div/div[2]/section/div/div/div/div')))
        attentions_id = [i.text for i in attentions_id if i.text]

        attention_id = []
        for i in attentions_id:
            i = i.split('\n')
            attention_id.append(i[0])
        # print(f'关注列表：{attention_id}')
        content = [acc_id, Twitter_num, attention_num, fan, attention_id]
        return content

    def get_teitter_content(self, Twitter_num):
        """
        获取推特文本内容及相应获赞数量，评论数量，转发数量
        :return:
        """
        url = 'https://twitter.com/ashrafghani'
        self.driver.get(url)
        count = 1

        while True:
            if count >= Twitter_num:
                break
            # 设置休眠时间 防止页面元素加载出错
            time.sleep(2)
            # 推文信息
            tweets = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="react-root"]/div/div/div/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/section/div/div/div/div/div/article/div/div[2]/div[2]')))
            if not tweets:
                continue
            tweets = [i.text.split('\n') for i in tweets if i.text]
            # print(tweets, len(tweets))  # 列表镶嵌列表
            yield tweets
            # 滚动屏幕
            scroll = "window.scrollTo(0,document.body.scrollHeight)"
            self.driver.execute_script(scroll)

            count += 1

    def processing(self, tweets):
        """
        数据处理
        tweets 列表镶嵌列表
        :return:
        """
        for tweet in tweets:
            content = tweet[4]
            comment = tweet[-3]
            forward = tweet[-2]
            like = tweet[-1]
            yield content, comment, forward, like

    def save_data(self, data):
        """保存为csv"""
        with open("twitter.csv", "a+", encoding='utf-8', newline="") as f:
            k = csv.writer(f, delimiter=',')
            with open("twitter.csv", "r", encoding='utf-8', newline="") as f1:
                reader = csv.reader(f1)
                if not [row for row in reader]:
                    k.writerow(['ID', '推文数量', '关注人数', '关注列表', '粉丝数', '推文内容', '评论数', '转发数', '点赞数'])
                    k.writerows(data)
                else:
                    k.writerows(data)
            print(f'第：{self.count}条数据插入成功!')

    def quit(self):
        """
        关闭浏览器
        :return:
        """
        self.driver.quit()

    def run(self):
        for acc_id in self.read_xls():
            # 获取个人基本信息
            acc, Twitter_num, attention_num, fan, attention_id = self.get_basic(acc_id)
            # 推文数量
            Twitter_num = int(''.join(re.findall(r'\d', Twitter_num)))
            # 获取推文信息
            for tweets in self.get_teitter_content(Twitter_num):
                # 提取信息
                for contents in self.processing(tweets):
                    content, comment, forward, like = contents
                    # 数据保存
                    data = [[acc, Twitter_num, attention_num, attention_id, fan, content, comment, forward, like]]
                    self.save_data(data)
                    self.count += 1
        self.quit()


if __name__ == '__main__':
    spider = Spider()
    spider.run()