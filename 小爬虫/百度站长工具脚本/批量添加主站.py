# -*- coding:utf-8 -*-
# 文件 ：批量添加主站.py
# IED ：PyCharm
# 时间 ：2020/4/15 0015 10:31
# 版本 ：V1.0
import os
import sys
import json
import time
import logging
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

print(os.path.abspath(__file__))  # 当前文件绝对路径
PATH = os.getcwd()  # 文件路径


def run_time(func):
    def new_func(*args, **kwargs):
        start_time = datetime.now()
        print("程序开始时间：{}".format(start_time))
        func(*args, **kwargs)
        end_time = datetime.now()
        print("程序结束时间：{}".format(end_time))
        print("程序执行用时：{}s".format((end_time - start_time)))
    return new_func


def log_init():
    # 创建一个日志器
    program = os.path.basename(sys.argv[0])  # 获取程序名
    logger = logging.getLogger(program)
    # 判断handler是否有值,(避免出现重复添加的问题)
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s | %(name)-3s | %(levelname)-6s| %(message)s')  # 设置日志输出格式
        logger.setLevel(logging.DEBUG)

        # 输出日志至屏幕
        console = logging.StreamHandler()  # 设置日志信息输出至屏幕
        console.setLevel(level=logging.DEBUG)  # 设置日志器输出级别，包括debug < info< warning< error< critical
        console.setFormatter(formatter)  # 设置日志输出格式

        # 输出日志至文件
        path = PATH + r'/logs/'  # 日志保存路径
        if not os.path.exists(path):
            os.mkdir(path)
        filename = path + datetime.now().strftime('%Y-%m-%d') + '.log'
        fh = logging.FileHandler(filename, encoding='utf-8', mode='a+')  # 设置日志信息保存至文件
        # fh.setLevel(logging.DEBUG)  # 设置日志器输出级别
        fh.setFormatter(formatter)  # 设置日志输出格式
        logger.addHandler(fh)
        logger.addHandler(console)

    return logger


class Spider:
    def __init__(self):
        self.log = log_init()
        chrome_options = Options()
        desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
        desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        prefs = {"profile.managed_default_content_settings.images": 1}  # 1 加载图片 2不加载图片,加快访问速度
        chrome_options.add_experimental_option("prefs", prefs)
        # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.wait = WebDriverWait(self.driver, 3, 1)  # 设置隐式等待时间
        self.driver.maximize_window()  # 窗口最大化

    def login_by_scan(self):
        self.log.info("开始登录,请等待页面加载完成后,输入账号登录...")
        self.driver.get('https://ziyuan.baidu.com/login/index?u=/site/index#/')
        self.log.info('登录账号：')
        while True:
            if 'login' not in self.driver.current_url:
                self.log.info(self.driver.current_url)
                self.log.info("登录成功")
                return
            else:
                print("等待登录中...")
                time.sleep(5)

    def add_main_site(self, domain):
        """
        添加主站
        domain : 域名
        """
        while True:
            # 把需要添加的域名拼接成url
            url = f'https://ziyuan.baidu.com/site/siteadd?sites=http://{domain}#/'
            self.driver.get(url)
            # 选择协议头
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="protocolSelect"]/span'))).click()
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="protocolSelect"]/div/div[1]'))).click()
            # 下一步
            next_step = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#site-add')))
            next_step.click()

            # 打码
            self.log.info('打码中...')
            # 判断是否有弹窗验证
            time.sleep(2)  # 加2秒等待防止访问太快页面加载不出元素
            code = self.driver.find_elements_by_xpath('//div[@class="vcode-body"]/div[1]/div/div[2]/div[2]')
            if code:
                if not self.code(code[0]):
                    self.log.info('打码失败,重试!')
                    continue

            # 设置站点领域
            self.log.info('设置站点领域')
            # 选择 其他
            a = self.wait.until(EC.presence_of_element_located((By.XPATH, '//label[@for="check24"]')))
            a.click()
            time.sleep(1)
            next_attr = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#sub-attr')))
            next_attr.click()

            # 判断是否有站点领域错误提示
            time.sleep(2)
            if self.driver.find_elements_by_xpath('//*[@id="dialog"]'):
                self.driver.refresh()
                self.wait.until(EC.presence_of_element_located((By.XPATH, '//label[@for="check2"]')))
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#sub-attr'))).click()

            # 提交
            time.sleep(1.5)
            self.log.info('提交')
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#verifySubmit'))).click()
            return True

    def code(self, code):
        """下载验证图片"""
        # print('下载验证图片')
        html = self.driver.page_source  # 获取页面源码
        html = etree.HTML(html)  # 源码转为etree对象
        url = html.xpath('//div[@class="vcode-body"]/div[1]/div/div[1]/img/@src')[0]  # 提取验证码图片url
        # print(url)
        # 判断图片是否存在
        img_file = '验证码.jpg'
        if os.path.exists(img_file):
            os.remove(img_file)
            # print('删除图片成功')
        response = requests.get(url)
        with open('验证码.jpg', 'wb') as f:
            f.write(response.content)
        rsp = self.code_api()
        point = rsp['point']  # 角度
        px = rsp['px']  # 距离
        # print(f'角度:{point}, 距离:{px}')
        # 滑动滑块
        ActionChains(self.driver).drag_and_drop_by_offset(code, px, 0).perform()
        time.sleep(3)
        if self.driver.find_elements_by_xpath('//div[@class="vcode-body"]'):
            return False
        return True

    def code_api(self):
        """调用打码接口获取图片角度"""
        files = {'file': ('img.jpg', open('验证码.jpg', 'rb'), 'image/jpeg', {})}
        values = {'token': "75b5f07a07d552e7f9f9958ac63363d8"}
        r = requests.post('http://106.13.108.81:882/api/Baiduyz', files=files, data=values)
        rsp = json.loads(r.text)
        if '成功找到' not in rsp['msg']:
            self.log.error(rsp['msg'])
            sys.exit()
        return rsp

    def process_txt(self):
        """
        读取域名文件
        :return: 主域名, 子域名
        """
        path = f'{PATH}/config/域名.txt'
        for line in open(path, 'r', encoding='utf-8'):
            if line.replace('\n', ''):
                yield line.replace('\n', '')

    def save_txt(self, domain, status=True):
        """保存记录"""
        if status:
            filename = f'{PATH}/config/{datetime.now().strftime("%Y-%m-%d")}-成功.txt'
        else:
            filename = f'{PATH}/config/{datetime.now().strftime("%Y-%m-%d")}-失败.txt'

        with open(filename, 'a+', encoding='utf-8') as f:
            f.write(f'{domain}\n')

    def main(self):
        for domain in self.process_txt():
            while True:
                try:
                    self.add_main_site(domain)
                    self.log.info(f'主域名:{domain}添加成功!')
                    self.save_txt(domain)
                    time.sleep(1)
                    break
                except Exception as e:
                    self.save_txt(domain, status=False)
                    self.log.error(f'主域名:{domain}添加失败重试')
                    self.log.error(e)
                    self.log.error(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
                    self.log.error(e.__traceback__.tb_lineno)  # 发生异常所在的行数
                    break


if __name__ == '__main__':
    spider = Spider()
    spider.login_by_scan()
    spider.main()
