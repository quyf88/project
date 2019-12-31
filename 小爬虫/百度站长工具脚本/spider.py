# coding=utf-8
# 作者    ： Administrator
# 文件    ：spider.py
# IED    ：PyCharm
# 创建时间 ：2019/9/28 17:22
import os
import re
import time
import requests
from lxml import etree
from datetime import datetime
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
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
        chrome_options = Options()
        desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
        desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        prefs = {"profile.managed_default_content_settings.images": 1}  # 1 加载图片 2不加载图片,加快访问速度
        chrome_options.add_experimental_option("prefs", prefs)
        # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10, 1)  # 设置隐式等待时间
        self.driver.maximize_window()  # 窗口最大化

        self.overrun = False  # 子域名是否超出上限

    def login_by_scan(self):
        print("开始登录,请等待页面加载完成后,输入账号登录...")
        self.driver.get('https://ziyuan.baidu.com/login/index?u=/site/batchadd')
        input('登录账号：')
        while True:
            if 'login' not in self.driver.current_url:
                print(self.driver.current_url)
                print("登录成功")
                break
            else:
                print("等待登录中...")
                time.sleep(5)

    def add_batches(self, filename, content):
        """
        批量添加子站
        filename : 主域名
        content ： 子域名列表
        :return:
        """
        while True:
            # try:
            # 进入添加子站页面
            self.driver.get("https://ziyuan.baidu.com/site/batchadd")
            # 输入主站url
            master_url = self.driver.find_elements_by_xpath('//div[@class="select-domain-box clearfix"]/input')
            master_url[0].send_keys(filename)
            # 选择主站url
            select_url = self.driver.find_elements_by_xpath('//div[@id="suggest_row1"]')
            print(self.driver.current_url)
            print(select_url[0].text, 123456789)
            if not select_url:
                print('没有此主站记录!')
            select_url[0].click()
            # 子域名输入框
            batches_url = self.driver.find_element_by_xpath('//*[@id="batchaddTextarea"]')
            for bat_url in content:
                print(bat_url.rstrip())
                batches_url.send_keys(bat_url)
            # 确认提交
            submit = self.driver.find_element_by_xpath('//*[@id="batchaddSiteBtn"]')
            submit.click()
            # 弹窗处理
            pop_ups = self.driver.find_element_by_xpath('//div[@id="dialog-foot"]/button[1]')
            pop_ups.click()
            # 图片验证
            self.code()
            # 效验是否添加成功
            if self.validation():
                return
            else:
                continue
            # except:
            #     print("子域名添加成功!")
            #     print('*' * 30)
            #     return

    def code(self):
        """验证码"""
        # 判断是否有弹窗验证
        time.sleep(3)
        print(111122233)
        code = self.driver.find_elements_by_xpath('//div[@class="vcode-body"]/div[1]/div/div[2]/div[2]')
        if not code:
            print(f'code 退出')
            return
        print('提取验证码图片URL')
        html = self.driver.page_source
        html = etree.HTML(html)
        url = html.xpath('//div[@class="vcode-body"]/div[1]/div/div[1]/img/@src')[0]
        print(url)
        input('aaaa')
        print(f'下载验证图片')
        # 下载验证图片
        response = requests.get(url)
        with open('验证码.jpg', 'wb') as f:
            f.write(response.content)


        # 滑动滑块
        ActionChains(self.driver).drag_and_drop_by_offset(code[0], 180, 0).perform()


    def validation(self):
        """
        效验是否添加成功
        :return:
        """
        count = 1
        while True:
            # 是否超出上限
            overrun = self.driver.find_elements_by_xpath('//div[@id="dialog-content"]')
            if overrun:
                if '添加数量超过上限' in overrun[0].text:
                    print('子域名添加超出上限,跳过当前主站!!!')
                    self.overrun = True
                    return True

            # 是否有忽略错误标签
            error = self.driver.find_element_by_css_selector('.console-ingore')
            # print(error.is_displayed())
            if error.is_displayed():
                error.click()
            index_url = 'https://ziyuan.baidu.com/site/index'
            if index_url == self.driver.current_url:
                print("子域名添加成功!")
                print('*' * 30)
                return True
            if count > 3:
                print('子域名添加失败,等待30秒后重试!!!')
                time.sleep(30)
                return False
            time.sleep(2)
            count += 1
            continue

    def read_txt(self):
        """
        读取子域名文件
        :return:
        """
        # 返回指定目录下所有文件
        files = os.listdir('config')
        # 筛选指定文件
        files = [i for i in files if 'txt' in i if 'requirements' not in i]
        print(files)
        for file_name in files:
            (filename, extension) = os.path.splitext(file_name)
            print(filename, extension)
            with open(f'config/{file_name}', 'r') as f:
                lines = f.readlines()
                # lines = [i.rstrip() for i in lines]
                yield filename, lines
                # 判断子域名是否超出上限
                if self.overrun:
                    self.overrun = False
                    continue

    def process_txt(self):
        """
        处理文件 一次提取十个子域名
        :return: 主域名, 子域名
        """
        count = 0
        content = []
        for u in self.read_txt():
            filename, lines = u
            for line in lines:
                content.append(line)
                count += 1
                # 判断子域名是否超出上限
                if self.overrun:
                    break
                if count % 10 == 0:
                    yield filename, content
                    content = []

    @run_time
    def run(self):
        # 登录
        self.login_by_scan()
        # 读取当前处理的主域名和子域名
        for u in self.process_txt():
            filename, content = u
            # print(filename, content)
            # 提交数据
            self.add_batches(filename, content)


if __name__ == '__main__':
    spider = Spider()
    spider.run()


# 邮箱密码quanjie19620814@163.com   najn28158
# 账号密码quanjie19620814@163.com   qq112211
# quanjie19620814@163.com  qq112211