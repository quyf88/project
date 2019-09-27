#!/usr/bin/env python
# author:Administrator
# datetime:2019/9/26 0026 14:10
# software:PyCharm
# project :project

import csv
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
        self.wait = WebDriverWait(self.driver, 5, 1)  # 设置隐式等待时间
        self.driver.maximize_window()  # 窗口最大化

    @retry(stop_max_attempt_number=5)
    def _parse_url(self, url):
        """url请求"""
        while True:
            try:
                response = requests.get(url, headers=self.headers, timeout=5)
            except Exception as e:
                print(e)
                continue
            return response

    def get_model(self):
        """获取所有车型数据"""
        # 所有车型js文件
        url = 'https://car.autohome.com.cn/javascript/NewSpecCompare.js?20131010'
        response = self._parse_url(url)
        # GBK解码
        content = response.content.decode('GBK')
        # 剔除开头和结尾处多余字符 转换为json
        content = content.replace('var listCompare$100= ', '').replace(';', '')
        content = json.loads(content)
        # print(content)
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

    def test(self):
        for u in self.get_model():
            # 品牌ID,品牌首字母,名称,车系名称,车系ID, 车型名称
            che_id, brand_l, brand_n, car_l, model_l, model_n = u
            # 车系参数url
            url = f'https://car.autohome.com.cn/config/series/{18}.html'
            print(url)
            self.driver.get(url)
            # 提取全部车型, 定位全部车型 判断有没有停售车型
            models = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="other-car"]')))
            ActionChains(self.driver).move_to_element(models).perform()  # 鼠标移动至车型列表
            print(models.text)
            if '停售' in models.text:
                print('获取停售车型数据')
                self.get_discontinued_models(model_l)
            break

    def get_discontinued_models(self, model_id):
        """
        提取停售车型年份ID
        model_id ： 车系id
        :return:
        """
        url = f'https://www.autohome.com.cn/{18}/sale.html'
        print(url)
        response = self._parse_url(url)
        print(response.text)
        html = etree.HTML(response.text)
        # 判断是否有更多
        title = html.xpath('//div[@class="title-subcnt-tab"]/ul/li//text()')
        if '更多' in title:
            print(title)
            print('有更多')
        # 年份ID
        titles = html.xpath('//div[@class="title-subcnt-tab"]/ul/li/a/@data-yearid')
        print(titles)

    def get_motor(self):
        """
        获取车型参数信息
        :return:
        """
        for u in self.get_model():
            # 品牌ID,品牌首字母,名称,车系名称,车系ID, 车型名称
            che_id, brand_l, brand_n, car_l, model_l, model_n = u
            # 车系参数url
            url = f'https://car.m.autohome.com.cn/config/series/{model_l}.html'
            print(url)
            self.driver.get(url)
            # time.sleep(3)
            # print(self.driver.page_source)
            try:
                # 车型列表
                title = WebDriverWait(self.driver, 5, 1, AttributeError).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="compare"]/div[2]/div/div')))
                title = [i.text.replace('\n', ' ') for i in title]
                # 发动机型号
                engine_model = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="detail"]/div[2]/div/div[3]/div[1]/div')))
                engine_model = [i.text for i in engine_model]
                # 气缸数
                front_tire = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="detail"]/div[2]/div/div[3]/div[5]/div')))
                front_tire = [i.text for i in front_tire]
                # 气缸排列形式
                Cylinder = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="detail"]/div[2]/div/div[3]/div[4]/div')))
                Cylinder = [i.text for i in Cylinder]
                # 气门数
                rear_tire = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="detail"]/div[2]/div/div[3]/div[6]/div')))
                rear_tire = [i.text for i in rear_tire]
                # 排量
                Displacement = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="detail"]/div[2]/div/div[3]/div[2]/div')))
                Displacement = [i.text for i in Displacement]
                # 环保标准
                Environmental = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="detail"]/div[2]/div/div[3]/div[22]/div')))
                Environmental = [i.text for i in Environmental]
                # 燃料形式
                Energytype = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="detail"]/div[2]/div/div[3]/div[17]/div')))
                Energytype = [i.text for i in Energytype]
                # 燃油标号
                Fuelform = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="detail"]/div[2]/div/div[3]/div[18]/div')))
                Fuelform = [i.text for i in Fuelform]
                # 变速箱
                Gearbox = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="detail"]/div[2]/div/div[1]/div[12]/div')))
                Gearbox = [i.text for i in Gearbox]
                # 上市时间
                market = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="detail"]/div[2]/div/div[1]/div[8]/div')))
                market = [i.text for i in market]
                # 整车质保
                Warranty = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="detail"]/div[2]/div/div[1]/div[21]/div')))
                Warranty = [i.text for i in Warranty]
                # 座位数（个）
                seats = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="detail"]/div[2]/div/div[2]/div[10]/div')))
                seats = [i.text for i in seats]

                motors = zip(title, engine_model, front_tire, Cylinder, rear_tire, Displacement, Environmental, Energytype,
                             Fuelform, Gearbox, market, Warranty, seats)
                motors = [i for i in motors if len(i)]
            except:
                continue

            for motor in motors:
                if not motor[0]:
                    continue
                data = (brand_l, brand_n, car_l, che_id, model_l) + motor
                print(list(data))
                self.scv_data([list(data)])

    def scv_data(self, data):
        """保存为csv"""
        self.count += 1
        with open("1.csv", "a+", encoding='utf-8', newline="") as f:
            k = csv.writer(f, delimiter=',')
            with open("1.csv", "r", encoding='utf-8', newline="") as f1:
                reader = csv.reader(f1)
                if not [row for row in reader]:
                    k.writerow(['品牌索引', '品牌名称', '车系名称', '品牌ID', '车系ID', '汽车型号', '发动机型号', '气缸数', '气缸排列形式', '气门数', '排量',
                                '环保标准', '燃料形式', '燃油标号', '变速箱', '上市时间', '整车质保', '座位数（个）'])
                    k.writerows(data)
                    print('第[{}]条数据插入成功'.format(self.count))
                else:
                    k.writerows(data)
                    print('第[{}]条数据插入成功'.format(self.count))


if __name__ == '__main__':
    spider = Spider()
    spider.test()