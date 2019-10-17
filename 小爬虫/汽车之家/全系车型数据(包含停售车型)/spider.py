#!/usr/bin/env python
# author:Administrator
# datetime:2019/9/26 0026 14:10
# software:PyCharm
# project :project
import re
import csv
import time
import json
import requests
import threading
from lxml import etree
from datetime import datetime
from retrying import retry
from fake_useragent import UserAgent
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
        # 获取随机请求头
        self.headers = {"User-Agent": UserAgent().random}
        self.lock = threading.Lock()
        self.count = 0

        chrome_options = Options()
        desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
        desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        prefs = {"profile.managed_default_content_settings.images": 1}  # 1 加载图片 2不加载图片,加快访问速度
        chrome_options.add_experimental_option("prefs", prefs)
        # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.wait = WebDriverWait(self.driver, 100, 1)  # 设置隐式等待时间
        self.driver.maximize_window()  # 窗口最大化

        # 车型id
        self.car_id = None

    @retry(stop_max_attempt_number=30)
    def _parse_url(self, url):
        """url请求"""
        while True:
            try:
                response = requests.get(url, headers=self.headers, timeout=30)
            except Exception as e:
                print(e)
                continue
            return response

    def get_model(self):
        """获取所有车型数据"""
        # 所有车型js文件
        url = 'https://car.autohome.com.cn/javascript/NewSpecCompare.js?20131010'
        response = self._parse_url(url)
        content = response.content.decode('GBK')  # GBK解码
        # 剔除开头和结尾处多余字符 转换为json
        content = content.replace('var listCompare$100= ', '').replace(';', '')
        content = json.loads(content)
        for i in content:
            # 品牌ID,品牌首字母,名称,车系列表
            che_id, brand_l, brand_n, brand_list,  = i['I'], i['L'], i['N'], i['List']
            for q in brand_list:
                # 车系名称,车型列表
                car_l, car_list = q['N'], q['List']
                for t in car_list:
                    # 车型ID, 车型名称
                    model_l = t['I']
                    model_n = t['N']
                    # 品牌ID,品牌首字母,名称,车系名称,车型ID, 车型名称
                    yield che_id, brand_l, brand_n, car_l, model_l, model_n

    def get_model_param(self, model_l, model_n):
        """
        获取车型参数url
        :param model_l: 车型ID
        :param model_n: 车型名称
        :return: 车型参数url
        """
        urls = []

        # 车系参数url
        url = f'https://car.autohome.com.cn/config/series/{model_l}.html'
        self.driver.get(url)

        html = self.driver.page_source
        # 判断当前车型名车是否包含(停售) 或者 当前页面有没有数据,没有数据代表不是在售车型
        if '停售' in model_n or '抱歉，暂无相关数据' in html:
            print(f'{model_l, model_n} 已停售,获取历史数据!')
            urls = self.get_discontinued_models(model_l)
            return urls

        # 提取全部车型, 定位全部车型 判断有没有停售车型
        models = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="other-car"]')))
        ActionChains(self.driver).move_to_element(models).perform()  # 鼠标移动至车型列表
        if '停售' in models.text:
            print('有停售车型,获取停售车型数据')
            urls = self.get_discontinued_models(model_l)
        urls.append(url)
        return urls

    def get_discontinued_models(self, model_id):
        """
        提取停售车型年份ID 拼接车系参数url
        model_id ： 车系id
        :return: 车型详细参数url
        """
        urls = []
        url = f'https://www.autohome.com.cn/{model_id}/sale.html'
        print(url)
        response = self._parse_url(url)
        html = etree.HTML(response.text)
        # 停售车型ID
        years_id = html.xpath('//div[@class="title-subcnt-tab"]/ul/li/a/@data-yearid')
        # 判断是否有更多停售车型
        title = html.xpath('//div[@class="title-subcnt-tab"]/ul/li//text()')
        if '更多' in title:
            more = html.xpath('//li[@data-toggle="overlay"]/div/dl/dd/a/@data-yearid')
            titles = years_id + more
        else:
            titles = years_id
        # 根据年份ID拼接停售车型参数url
        for i in titles:
            _url = f'https://car.autohome.com.cn/config/series/{model_id}-{i}.html'
            urls.append(_url)
        return urls

    def get_motor(self, urls):
        """
        获取车型参数信息
        :return:
        """
        for url in urls:
            # 车系参数url
            print(url)
            self.driver.get(url)
            time.sleep(1)
            try:
                # 车型ID
                self.car_id = re.findall(r'series/(.*?).html', url)[0]
                # 车辆型号
                title = self.driver.find_elements_by_xpath('//*[@id="config_nav"]/table/tbody/tr/td/div[2]/div')
                title = [i.text for i in title]
                nums = len(title)
                # 指导价
                price = self.driver.find_elements_by_xpath('//*[@id="tr_2000"]/td/div')
                price = [price[i].text for i in range(nums)]
                # 上市时间
                market = self.driver.find_elements_by_xpath('//*[@id="tr_4"]/td/div')
                market = [market[i].text for i in range(nums)]
                # 能源类型
                energy = self.driver.find_elements_by_xpath('//*[@id="tr_2"]/td/div')
                energy = [energy[i].text for i in range(nums)]
                # 环保类型
                environmental = self.driver.find_elements_by_xpath('//*[@id="tr_3"]/td/div')
                environmental = [environmental[i].text for i in range(nums)]
                # 最大功率
                max_power = self.driver.find_elements_by_xpath('//*[@id="tr_5"]/td/div')
                max_power = [max_power[i].text for i in range(nums)]
                # 最大扭矩
                max_torque = self.driver.find_elements_by_xpath('//*[@id="tr_6"]/td/div')
                max_torque = [max_torque[i].text for i in range(nums)]
                # 发动机
                engine = self.driver.find_elements_by_xpath('//*[@id="tr_7"]/td/div')
                engine = [engine[i].text for i in range(nums)]
                # 变速箱
                gearbox = self.driver.find_elements_by_xpath('//*[@id="tr_8"]/td/div')
                gearbox = [gearbox[i].text for i in range(nums)]
                # 外观尺寸
                size = self.driver.find_elements_by_xpath('//*[@id="tr_9"]/td/div')
                size = [size[i].text for i in range(nums)]
                # 车身结构
                structure = self.driver.find_elements_by_xpath('//*[@id="tr_10"]/td/div')
                structure = [structure[i].text for i in range(nums)]
                # 最高车速
                max_speed = self.driver.find_elements_by_xpath('//*[@id="tr_11"]/td/div')
                max_speed = [max_speed[i].text for i in range(nums)]
                # 0-100 加速
                accelerate = self.driver.find_elements_by_xpath('//*[@id="tr_12"]/td/div')
                accelerate = [accelerate[i].text for i in range(nums)]
                # 油耗
                fuel = self.driver.find_elements_by_xpath('//*[@id="tr_12"]/td/div')
                fuel = [fuel[i].text for i in range(nums)]
                # 整车质保
                warranty = self.driver.find_elements_by_xpath('//*[@id="tr_17"]/td')
                warranty = [warranty[i].text for i in range(nums)]
                # 发动机型号
                engine_model = self.driver.find_elements_by_xpath('//*[@id="tr_31"]/td/div')
                engine_model = [engine_model[i].text for i in range(nums)]
                # 排量（L）
                displacement = self.driver.find_elements_by_xpath('//*[@id="tr_33"]/td/div')
                displacement = [displacement[i].text for i in range(nums)]
                # 气缸排列形式
                cylinder = self.driver.find_elements_by_xpath('//*[@id="tr_35"]/td/div')
                cylinder = [cylinder[i].text for i in range(nums)]
                # 气缸数
                front_tire = self.driver.find_elements_by_xpath('//*[@id="tr_36"]/td/div')
                front_tire = [front_tire[i].text for i in range(nums)]
                # 气门数
                rear_tire = self.driver.find_elements_by_xpath('//*[@id="tr_37"]/td/div')
                rear_tire = [rear_tire[i].text for i in range(nums)]
            except:
                continue
            contents = zip(title, price, market, energy, environmental, max_power, max_torque, engine, gearbox, size,
                           structure, max_speed, accelerate, fuel, warranty, engine_model, displacement, cylinder,
                           front_tire, rear_tire)
            for cont in contents:
                yield cont

    def scv_data(self, data):
        """保存为csv"""
        self.count += 1
        with open("全系发动机数据.csv", "a+", encoding='utf-8', newline="") as f:
            k = csv.writer(f, delimiter=',')
            with open("全系发动机数据.csv", "r", encoding='utf-8', newline="") as f1:
                reader = csv.reader(f1)
                if not [row for row in reader]:
                    k.writerow(['品牌索引', '品牌ID', '品牌名称', '车系ID', '车系名称', '车型ID', '汽车型号', '指导价', '上市时间', '能源类型',
                                '环保类型', '最大功率', '最大扭矩', '发动机', '变速箱', '外观尺寸', '车身结构', '最高车速', '0-100 加速',
                                '油耗', '整车质保', '发动机型号', '排量（L）', '气缸排列形式', '气缸数', '气门数'])
                    k.writerows(data)
                    print('第[{}]条数据插入成功'.format(self.count))
                else:
                    k.writerows(data)
                    print('第[{}]条数据插入成功'.format(self.count))

    def run(self):
        for u in self.get_model():
            # 品牌ID,品牌首字母,名称,车系名称,车系ID, 车型名称
            che_id, brand_l, brand_n, car_l, model_l, model_n = u
            urls = self.get_model_param(model_l, model_n)
            for content in self.get_motor(urls):
                data = [list((brand_l, che_id, brand_n, model_l, car_l, self.car_id) + content)]
                print(data)
                self.scv_data(data)

        # 关闭浏览器 杀死进程
        self.driver.quit()


if __name__ == '__main__':
    spider = Spider()
    spider.run()