# -*- coding:utf-8 -*-
# 文件 ：google_search.py
# IED ：PyCharm
# 时间 ：2020/4/20 0020 19:59
# 版本 ：V1.0
import csv
import os, sys, time, logging, datetime, random
import requests
from lxml import etree
from urllib.parse import quote_plus
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


print(os.path.abspath(__file__))  # 当前文件绝对路径
PATH = os.getcwd()  # 文件路径


def run_time(func):
    def new_func(*args, **kwargs):
        start_time = datetime.datetime.now()
        log_init().info("Program start time：{}".format(start_time))
        res = func(*args, **kwargs)
        end_time = datetime.datetime.now()
        log_init().info("Program end time：{}".format(end_time))
        log_init().info("Program execution time：{}s".format((end_time - start_time)))
        return res

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
        filename = path + datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
        fh = logging.FileHandler(filename, encoding='utf-8', mode='a+')  # 设置日志信息保存至文件
        # fh.setLevel(logging.DEBUG)  # 设置日志器输出级别
        fh.setFormatter(formatter)  # 设置日志输出格式
        logger.addHandler(fh)
        logger.addHandler(console)

    return logger


class GoogleSearch:
    def __init__(self):
        log_init().info('GoogleSearch start')
        log_init().info('chrome start')

        self.count = 0
        self.FILE_NAME = None

        options = Options()
        # 使用无头模式
        # options.add_argument('headless')
        # options.add_argument('--disable-gpu')
        desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
        desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        prefs = {"profile.managed_default_content_settings.images": 1}  # 1 加载图片 2不加载图片,加快访问速度
        options.add_experimental_option("prefs", prefs)
        # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(chrome_options=options, desired_capabilities=desired_capabilities)

        self.wait = WebDriverWait(self.driver, 15, 1)  # 设置隐式等待时间
        self.driver.maximize_window()  # 窗口最大化
        log_init().info('chrome initialized successfully')

    def keyword_search(self, word, start):
        """关键词搜索"""
        url = f'https://google.com/search?q="{quote_plus(word)}"&filter=0&biw=1366&bih=657&start={start}'
        self.driver.get(url)
        while True:
            if 'www.google.com' not in self.driver.current_url:
                continue
            break

    def machine_verification(self):
        """检测人机验证"""
        if '系统检测到您的计算机网络中存在异常流量' not in self.driver.page_source:
            return False
        recaptcha = self.driver.find_element_by_xpath('//div[@id="recaptcha"]')
        log_init().info('人机验证')
        # print(recaptcha.get_attribute("data-sitekey"))
        return recaptcha.get_attribute("data-sitekey")

    def captcha_api(self, data_sitekey, page_url):
        """打码"""
        api_key = "26899b9d5e27d0328567700e3023e679"
        # key=打码平台秘钥，googlekey=页面data_sitekey，pageurl=当前页面url
        u1 = f"https://2captcha.com/in.php?key={api_key}&method=userrecaptcha&googlekey={data_sitekey}&pageurl={page_url}&json=1&invisible=1"
        r1 = requests.get(u1)
        # print(r1.json())
        rid = r1.json().get("request")
        u2 = f"https://2captcha.com/res.php?key={api_key}&action=get&id={int(rid)}&json=1"
        log_init().info(f'打码中...等待20-30秒')
        time.sleep(25)
        while True:
            r2 = requests.get(u2)
            # print(r2.json())
            if r2.json().get("status") == 1:
                form_tokon = r2.json().get("request")
                break
            time.sleep(5)
        log_init().info('成功获取人机识别码')
        # 提交打码结果
        wirte_tokon_js = f'document.getElementById("g-recaptcha-response").innerHTML="{form_tokon}";'
        submit_js = 'document.getElementById("captcha-form").submit();'
        self.driver.execute_script(wirte_tokon_js)
        time.sleep(1)
        self.driver.execute_script(submit_js)
        log_init().info('人机识别提交成功')

    def add_mosaic_success(self):
        """判断页面是否加载成功"""
        try:
            if self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="SDkEP"]'))):
                # print('人机识别成功!')
                return True
        except:
            return False

    def _position_xpath(self, num):
        """提取xpath"""
        try:
            results = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="rso"]/div')))
        except:
            log_init().info('当前关键词提取完成,切换下一个关键词.')
            return False
        for result in results:
            html = etree.HTML(result.get_attribute('innerHTML'))
            date = html.xpath('//div/div/div/span/span/text()')  # 文章发布时间
            if not date:
                log_init().info('不符合条件跳过')
                continue
            res_url = html.xpath('//div/div[1]/a/@href')  # 文章url
            b = date[0].replace('年', ' ').replace('月', ' ').replace('日', ' ').replace('-', '')
            c = [i for i in b.split(' ') if i]
            c = f'{c[1] c[2] c[0]}'
            self.sav_data([[c, res_url[0]]], int(num))
        return True

    def keep_records(self, content, vali=False):
        """保存获取记录"""
        file_name = f'{PATH}/config/valida.txt'
        if not os.path.exists(file_name):
            fi = open(file_name, 'a')
            fi.close()
        if vali:
            with open(file_name, 'r') as f:
                flight = [i.replace('\n', '') for i in f.readlines()]
                if content in flight:
                    return True
                return False
        else:
            with open(file_name, 'a+') as f:
                f.write(content)
                f.write('\n')

    def red_csv(self):
        """读取配置文件"""
        file = f'{PATH}/config/SAMPLE.csv'
        with open(file, 'r', encoding='UTF-8-sig') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                row = [i for i in row if str(i).replace(' ', '')]
                yield row

    def sav_data(self, data, num):
        """
        保存数据
        :return:
        """
        path = PATH + r'/数据'  # 数据保存路径
        if not os.path.exists(path):
            os.mkdir(path)
        self.FILE_NAME = '{}/rumor{:0>4d}.csv'.format(path, num)
        with open(self.FILE_NAME, "a+", encoding='UTF-8', newline="") as f:
            k = csv.writer(f, delimiter=',')
            with open(self.FILE_NAME, "r", encoding='UTF-8', newline="") as f1:
                reader = csv.reader(f1)
                if not [row for row in reader]:
                    k.writerow(
                        ['dates', 'website'])
                    k.writerows(data)
                else:
                    k.writerows(data)
            self.count += 1
            log_init().info('成功保存一条数据')

    def sav_data_z(self, data):
        """
        保存数据
        :return:
        """
        path = PATH + r'/数据'  # 数据保存路径
        if not os.path.exists(path):
            os.mkdir(path)
        FILE_NAME = f'{path}/results.csv'
        with open(FILE_NAME, "a+", encoding='UTF-8', newline="") as f:
            k = csv.writer(f, delimiter=',')
            with open(FILE_NAME, "r", encoding='UTF-8', newline="") as f1:
                reader = csv.reader(f1)
                if not [row for row in reader]:
                    k.writerow(
                        ['No.', 'label', 'content', 'results_num', 'filename'])
                    k.writerows(data)
                else:
                    k.writerows(data)
            self.count += 1

    def run(self):
        for row in self.red_csv():
            num, label, content = row
            if self.keep_records(content, vali=True):
                log_init().info(f'Skipped!')
                continue
            log_init().info(f'第:{num}关键词数据获取中...')
            for i in range(40):
                log_init().info(f'第：{i+1}页数据获取中...')
                self.keyword_search(content, i*10)   # 搜索

                time.sleep(random.randint(3, 5))
                log_init().info('判断页面是否加载成功')
                if not self.add_mosaic_success():
                    # 检测人机验证
                    recaptcha = self.machine_verification()
                    if recaptcha:  # 是否需要人机验证
                        # input('打码')
                        self.captcha_api(recaptcha, self.driver.current_url)
                        # 判断是否打码成功
                        if not self.add_mosaic_success():
                            continue
                        log_init().info('人机识别成功!')
                # 提取数据
                if not self._position_xpath(num):
                    break

                log_init().info(f'第:{i+1}页数据获取完成随机休眠...')
                time.sleep(random.randint(5, 10))
            self.sav_data_z([[num, label, content, self.count, self.FILE_NAME]])
            self.keep_records(content)
            self.count = 0
            log_init().info(f'第:{num}个关键词获取完成,切换下一个!')


if __name__ == '__main__':
    a = GoogleSearch()
    a.run()