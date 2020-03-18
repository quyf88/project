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
        self.log = self.log_init()
        print('*'*15, '程序启动', '*'*15)
        # self.log.info('程序启动')
        self.headers = {'user-agent': str(UserAgent().random),
                        'cookie': 'user_key=074763ddf768fd23112dac389cd5b827_1567324072; auto_login=; _fbp=fb.1.1567608952522.1674628427; language_viewer=tw; contents_id=80697; redirect=; sns_redirect=; net_session=M9FF2gHrylFUSS9NK%2BtYRwn81bbTnsKEVUw4t8NIOGQWXlhWTGbrqm7B5GZpbV3ai9oZLV1WQmGov5SYlPbt%2BF6BCd8SW5U6hdVSd%2Fcu6oxp5vJH0vcci4KIvwjEG0WIajmC0H%2B2HxDjBhTXU46M188eVS1O8DReAMrMQi7roP43gCJe2lJD9dc%2Bo5gO2xdpNXltYwe3EWJPauJQ52fgt4lCQjzGm1MOoXpeWhTxIQGPHI4xXK0sEYRt9pfD938wrI7ZiCdd6qQr6XsGkEK0DtVNUcHZS2piqJRNe%2Bf%2BbvIVMDlSKLd5GwzDfqOBxRZIdPM9E2G7vWUeU4RvyJoGJqZ9NR5qOz37xIxM9iV0blZ62L9bbDTdSZgibfLW4nK9zMs5BPrEnGgw%2F6tilHle%2BItmW0AHqgRMPV9ul0YWqWFUE5xyci8buh357ZYftpDxceO5HYuDHYo1L423i9EMykmroChT56TkF1Fm4TTydJJQadsQLJDRXxQEhPQAwBVn896dxXoaST5qQtBMI%2F%2Bx94MLmDJGx19bIuJcFMpdaCA%3D8f536d6fc43b0504c24b8bfea14c2f217a9d5233; save_id=%24dspwb20190808%40outlook.com; auto_key=36c56e3f130c2410299010b3d8f31f68; social_group=; language=tw; adult_check=1; auth_key=eff065cff73e8ecfa319e6471b923665; UTC=0; private_mode=error; giftbox_today_access=1; _ga=GA1.2.260280443.1567608951; _gid=GA1.2.1593371888.1567608951; contents=80697; user_idx=6396591; p_id=; ci_cookie=a51b24164720f4c769983ade59a6a89f; view_count=7; cdn_service2=; cdn_speed2='
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
        self.wait = WebDriverWait(self.driver, 60, 1)  # 设置隐式等待时间
        self.driver.maximize_window()  # 窗口最大化

        # 当前漫画文件夹路径
        self.comic_path = None
        # 更新的章节数
        self.num = None
        # 漫画章节路径
        self.chapter_path = None

    def log_init(self):
        """日志模块"""
        path = os.path.abspath('.') + r'\log\spider.log'
        formatter = logging.Formatter('%(asctime)s | %(name)-6s | %(levelname)-6s| %(message)s')
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        fh = logging.FileHandler(path, encoding='utf-8', mode='a+')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        console.setFormatter(formatter)
        # 如果需要同時需要在終端上輸出，定義一個streamHandler
        # print_handler = logging.StreamHandler()  # 往屏幕上输出
        # print_handler.setFormatter(formatter)  # 设置屏幕上显示的格式
        logger = logging.getLogger("spider")
        # logger.addHandler(print_handler)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(console)
        logger.addHandler(fh)
        return logger

    def login(self):
        count = 1
        self.log.info('账号登录')
        while True:
            url = 'https://www.toptoon.net'
            self.driver.get(url)
            login = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="topmenu_mini"]/span[1]')))
            if login.text != '登入':
                continue
            login.click()
            # 账号密码
            # print('输入账号')
            self.log.info('验证账号')
            user_id = self.wait.until(EC.presence_of_element_located((By.ID, 'user_id')))
            user_id.send_keys('dspwb20190808@outlook.com')
            # print('输入密码')
            self.log.info('验证密码')
            user_pw = self.driver.find_element_by_id('user_pw')
            user_pw.send_keys('Ddqqw333e123@#!!U')
            time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="alert_data"]/div[6]/span').click()
            # print('账号登录中...')
            self.log.info('账号登录中...')
            if count > 3:
                # print('账号登录失败,联系开发者!')
                self.log.info('账号登录失败,联系开发者!')
                self.driver.quit()
                os._exit(0)
            try:
                self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="mypage_data"]/table/tbody/tr/td/div[1]/div/p')))
            except:
                # print('登录失败,重试!!!')
                self.log.info('登录失败,重试!!!')
                count += 1
                continue
            print('登录成功')
            self.log.info('登录成功')
            # print('*'*15)
            # self.log.info('*'*15)
            return

    def read_url(self):
        """
        读取配置文件
        :return:
        """
        with open('config/2.txt', 'r', encoding='utf-8') as f:
            for i in f.readlines():
                url = i.split()[0]
                yield url

    def get_image_page(self, url):
        """
        获取漫画信息
        :return:
        """
        while True:
            self.driver.get(url)
            # 文章名
            article_name = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tab1_board > div > div:nth-child(1)'))).text
            # print('文章名：{}'.format(article_name))
            self.log.info('文章名：{}'.format(article_name))
            # 总章数
            total = self.driver.find_elements_by_css_selector('.filtr-item')
            # print('总章数：{}'.format(len(total)))
            self.log.info('总章数：{}'.format(len(total)))
            if not total:
                self.log.info('章节获取失败!!!刷新页面!!!')
                continue
            # 文章简介
            summary = self.driver.find_element_by_xpath('//*[@id="tab1_board"]/div/div[2]').text
            summary = summary.replace('\n', '').replace(' ', '')
            # print('文章简介：{}'.format(summary))
            self.log.info('文章简介：{}'.format(summary))
            data = [url, article_name, str(len(total)), summary]
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
        self.comic_path = path
        if not os.path.exists(path):
            os.mkdir(path)
            self.num = int(total)
            # print('{}：首次获取 共：{} 条 下载图片中...'.format(article_name, total))
            self.log.info('{}：首次获取 共：{} 条 下载图片中...'.format(article_name, total))
        if os.path.exists(path_name):
            with open(path_name, 'r', encoding='utf-8')as f:
                content = f.read().split(',')
                content = [i for i in content if i]
            # print(content[2], total)
            if content[2] == total:
                # print('没有更新')
                self.log.info('没有更新')
                return False
            self.num = int(total) - int(content[2])
            # print('{}：数据更新 {} 条 下载图片中...'.format(article_name, self.num))
            self.log.info('{}：数据更新 {} 条 下载图片中...'.format(article_name, self.num))

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
            readlin = [i.strip() for i in f.readlines()]
            if article_name not in readlin:
                f.write(article_name)
                f.write('\n')

    def chapter_details(self):
        """
        获取章节编号拼接详情页面url
        :return: 详情url
        """
        details = self.driver.find_elements_by_css_selector('.filtr-item')
        # 首次获取翻转列表 更新不翻转
        if len(details) == self.num:
            details = list(reversed(details))
        for i in range(self.num):
            # 获取章节标签源码
            html = details[i].get_attribute('innerHTML')
            # print(html)
            # 判断是否免费
            # 提取金额
            coupon = re.findall(r'&nbsp;(.*?)&nbsp;</span>', html)
            # print(coupon)
            # 滑动滚动条到某个指定的元素
            js4 = "arguments[0].scrollIntoView();"
            # 将下拉滑动条滑动到当前div区域
            self.driver.execute_script(js4, details[i])
            if ('免費' not in coupon) and ('收藏中' not in coupon):
                # 购买章节
                if not self.buy_comics(details[i]):
                    # print('当前章节购买失败!')
                    self.log.info('当前章节购买失败!')
                    continue
            # 提取章节ID 拼接详情url
            id = re.findall(r'episode_click(.*?),', html, re.S | re.M)
            if not id:
                continue
            id = ''.join(re.findall(r'(\d)', id[0]))
            # 第几章
            chapter = re.findall(r'第(.*?)話', html)
            # print('第{}話'.format(chapter[0]))
            self.log.info('第{}話'.format(chapter[0]))

            url = 'https://www.toptoon.net/comic/episode_view?episode_idx=' + str(id)
            self.store_url([url, '第' + str(chapter[0]) + '話'])
            print(url, '第' + str(chapter[0]) + '話')

        # print(details_url)
        # return details_url

    def store_url(self, data):
        """
        存储当前漫画章节url和章节名
        :return:
        """
        with open(self.comic_path + '/2.txt', 'a+', encoding='UTF-8') as f:
            for i in data:
                f.write(i)
                f.write(',')
            f.write('\n')
        with open(self.comic_path + '/update_url.txt', 'a', encoding='UTF-8') as f:
            for i in data:
                f.write(i)
                f.write(',')
            f.write('\n')

    def buy_comics(self, detail):
        """
        购买章节
        detail 购买的章节对象
        :return:
        """
        count = 1
        while True:
            # 打印当前页面iframe
            # print(self.driver.window_handles)
            # # 获取当前窗口句柄
            # print(self.driver.current_window_handle)
            # 点击关闭
            time.sleep(5)
            close = self.driver.find_elements_by_css_selector('#close')
            # print('关闭按钮：{}'.format(close))
            if close:
                close[0].click()
            # 点击弹出购买窗口
            # 滑动滚动条到某个指定的元素
            # print(detail)
            js4 = "arguments[0].scrollIntoView();"
            # 将下拉滑动条滑动到当前div区域
            self.driver.execute_script(js4, detail)

            detail.click()
            # 判断窗口是否弹出
            buys = WebDriverWait(self.driver, 10, 1, AttributeError).until(
                        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="alert_data"]/div[3]/table/tbody/tr')))
            if not buys:
                if count >= 3:
                    # print('购买失败!')
                    self.log.info('购买失败!')
                    return False
                count += 1
                continue
            # 点击购买当前章节
            if len(buys) < 1:
                buys[0].click()
            buys[1].click()
            # 确认购买
            enter = self.driver.find_element_by_css_selector('#p_btn_2').click()
            # print('全部购买完成!')
            self.log.info('全部购买完成!')
            self.driver.refresh()
            return True
            # print(enter.text)
            # if enter.text == '確認':
            #     enter.click()
            #     return True

    @retry(stop_max_attempt_number=5)
    def get_image_url(self, content):
        """
        根据漫画章节url地址 获取图片URL地址列表 收费章节需添加cookie 才可请求成功
        :return: 文件夹名称,图片url列表
        """
        # 效验IP
        # res = requests.get("http://httpbin.org/ip", headers=self.headers, proxies=self.proxies, verify=False, timeout=10).json()
        # ip = str(res['origin']).split(',')
        # print('代理添加成功IP：{}'.format(ip))
        # url = 'https://toptoon.net/comic/episode_view?episode_idx=27356'
        # 提取项目文件夹名称
        # response = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=10).text

        # 请求章节页面返回页面源码
        # print('提取详情图片url...')
        self.log.info('提取详情图片url...')
        response = requests.get(content[0], headers=self.headers, timeout=15).text
        # XPATH 定位 图片地址
        result = etree.HTML(response)
        image_url_list = result.xpath('//*[@id="viewer_body"]/div/div[1]/div')
        url_list = []
        for i in image_url_list:
            image_url = 'http:' + i.xpath('./img/@src')[0]
            url_list.append(image_url)
            # print('成功提取详情url:{}'.format(image_url))
        self.save_details_url(url_list, content[1])
        return url_list

    def save_details_url(self, data, chapter):
        """
        保存图片详情url
        :return:
        """
        self.chapter_path = self.comic_path + '/' + chapter
        if not os.path.exists(self.chapter_path):
            os.mkdir(self.chapter_path)
        with open(self.chapter_path + '/2.txt', 'a+', encoding='UTF-8') as f:
            for i in data:
                f.write(i)
                f.write('\n')

    @retry(stop_max_attempt_number=5)
    def get_image(self, i, image_url):
        """
        根据图片真实url地址下载图片 不用添加cooike 容易请求出错需多重试几次，或添加代理
        :return:
        """
        # GUI 打印此项会提示语法错误
        # print(image_url)
        while True:
            try:
                response = requests.get(image_url, headers=self.headers, timeout=15)
                if response.status_code != 200:
                    self.log.info('下载失败：错误代码 {}'.format(response.status_code))
                    continue
                # print(response.status_code)
            except:
                continue
            image_path = self.chapter_path + '/' + str(i+1) + '.jpg'
            with open(image_path, 'wb') as image_content:
                image_content.write(response.content)
                # print('图片 {} 保存成功!'.format(i+1))
                self.log.info('图片 {} 保存成功!'.format(i+1))
            return

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
            self.chapter_details()
            with open(self.comic_path + '/update_url.txt', 'r', encoding='UTF-8') as f:
                contents = [i.split(',') for i in f.readlines()]
            for content in contents:
                # 获取图片url
                url_list = self.get_image_url(content)
                self.log.info('{} 图片开始下载 共 {} 张...'.format(content[1], len(url_list)))
                # 下载图片
                for i in range(len(url_list)):
                    self.get_image(i, url_list[i])
                self.log.info('{} 图片下载完成...'.format(content[1]))
                # 更新记录输出至表格控件
                content = [data[1], content[1], content[0]]
                # print(content)
                self.log.info('content:{}'.format(content))
                # self.log.info('*' * 50)
                print('*' * 50, '\n')
            os.remove(self.comic_path + '/update_url.txt')
        print('*' * 50, '\n')
        # self.log.info('*' * 50)
        self.log.info('End of program execution')
        # print('End of program execution')


if __name__ == '__main__':
    spider = Spider()
    spider.run()

# https://www.toptoon.net/#contents_80755
# dspwb20190808@outlook.com
# Ddqqw333e123@#!!U