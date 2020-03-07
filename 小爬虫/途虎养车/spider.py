# -*- coding:utf-8 -*-
# 文件 ：spider.py
# IED ：PyCharm
# 时间 ：2020/3/3 0003 21:01
# 版本 ：V1.0
import os
import json
import time
import requests
import datetime
import pandas as pd
from retrying import retry
from urllib.parse import quote
from fake_useragent import UserAgent
from requests_html import HTMLSession
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Spider:
    def __init__(self):
        self.headers = {'User-Agent': str(UserAgent().random)}
        # chrome_options = Options()
        # desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
        # desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        # prefs = {"profile.managed_default_content_settings.images": 1}  # 1 加载图片 2不加载图片,加快访问速度
        # chrome_options.add_experimental_option("prefs", prefs)
        # # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        # chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # self.driver = webdriver.Chrome(chrome_options=chrome_options)
        # self.wait = WebDriverWait(self.driver, 10, 1)  # 设置隐式等待时间
        # self.driver.maximize_window()  # 窗口最大化
        self.count = 1

    def get_brand(self):
        """
        获取品牌名称，用来拼接车型列表url
        :return:
        """
        url = 'https://by.tuhu.cn/baoyang'
        self.driver.get(url)
        letters = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="div2"]/ul/li')))
        for i in range(1, len(letters)):
            letters[i].click()
            brands = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="CarBrands"]/ul/li')))
            # selenium无法用XPATH直接获取属性值 需要使用.get_attribute('data-brand')
            brands = [i.get_attribute('data-brand') for i in brands]
            print(brands)
            for u in brands:
                with open('品牌名称.txt', 'a+', encoding='utf-8') as f:
                    f.write(u)
                    f.write('\n')

        self.driver.quit()

    @retry(stop_max_attempt_number=3)
    def get_model(self, cond_brand):
        """
        获取车型列表， 用来拼接排量url
        :return:
        """
        url = f'https://item.tuhu.cn/Car/SelOneBrand?callback=__GetCarBrands__&Brand={cond_brand}'
        res = requests.get(url, headers=self.headers, timeout=5)
        content = res.text.replace('__GetCarBrands__(', '').strip(')')
        content = json.loads(content)
        models = content['OneBrand']
        for model in models:
            try:
                first = model['Brand'].split(' ')[0]  # 首字母
                brand = model['Brand'].split(' ')[2]  # 品牌
                BrandType = model['BrandType']  # 车厂
                CarName = model['CarName']  # 型号
                ProductID = model['ProductID']  # 型号ID 获取车型详细信息用
                Tires = model['Tires']  # 轮胎尺寸
                print(f'{first} {brand} {BrandType} {CarName} {ProductID} {Tires}')
                # 首字母 品牌 车厂 型号 型号ID 轮胎尺寸
                yield first, brand, BrandType, CarName, ProductID, Tires
            except Exception as e:
                print(f'解析车型数据错误：{e}')
                continue

    @retry(stop_max_attempt_number=3)
    def get_displacement(self, ProductID):
        """
        获取排量， 用来拼接年份url
        :return:
        """
        url = f'https://item.tuhu.cn/Car/SelectVehicle?callback=__GetCarBrands__&VehicleID={ProductID}'
        res = requests.get(url, headers=self.headers, timeout=5)
        content = res.text.replace('__GetCarBrands__(', '').strip(')')
        content = json.loads(content)
        displas = content['PaiLiang']
        for i in displas:
            displa = i['Value']  # 排量
            yield displa

    @retry(stop_max_attempt_number=3)
    def get_year(self, ProductID, displa):
        """
        获取年份， 用来拼接保养信息url
        :return:
        """
        url = f'https://item.tuhu.cn/Car/SelectVehicle?callback=__GetCarBrands__&VehicleID={ProductID}&PaiLiang={displa}'
        res = requests.get(url, headers=self.headers, timeout=5)
        content = res.text.replace('__GetCarBrands__(', '').strip(')')
        content = json.loads(content)
        years = content['Nian']
        for i in years:
            year = i['Value']  # 年份
            yield year

    def get_maintenance(self, url):
        """
        获取保养信息 机油参数数据
        :return:
        """
        print(f'{url}数据获取中...')
        # 建立Session 当前session用完后一定要关闭 不然打开太多容易被卡死 session.close() 关闭
        session = HTMLSession()
        # 请求链接
        r = session.get(url, verify=True)
        # 加载JavaScript，在Chromium里重新加载响应，并用最新获取到的HTML替换掉原来的HTML  首次使用，自动下载chromium
        # https://cncert.github.io/requests-html-doc-cn/#/?id=render 中文文档
        # retries重试三次 wait等待一秒加载数据
        print('加载javascript')
        try:
            r.html.render(retries=5)
            # 定位机油参数数据
            dosage = r.html.xpath('//p[@class="pack_tt2"]', first=True)
            if dosage:
                dosage = dosage.text.strip('（').strip('）')
            else:
                dosage = '官方暂无数据'
            # print(f'机油容量：{dosage}')
            # 定位机油、机滤型号参数
            engine_model = r.html.xpath('//div[@class="pack_biaoti"]')
            if engine_model:
                engine_model = [i.text for i in engine_model]
                motor_oil = engine_model[0].split('\n')[0]
                level = engine_model[0].split('\n')[1] if len(engine_model[0].split('\n')) > 1 else '暂无数据'
                machine_filter = engine_model[-1]
            else:
                motor_oil = level = machine_filter = '官方暂无数据'
            # 定位价格数据
            prices = r.html.xpath('//div[@class="pck_price"]')
            if prices:
                prices = [i.text for i in prices]
                motor_oil_money = prices[0]
                machine_filter_money = prices[-1]
            else:
                motor_oil_money = machine_filter_money = '官方暂无数据'
            # 关闭建立的session链接
            session.close()
            print(f'关闭建立的session')
            return dosage, motor_oil, motor_oil_money, level, machine_filter, machine_filter_money
        except Exception as e:
            # 关闭建立的session链接
            session.close()
            print(f'{url}数据获取失败 原因：{e}!!!')
            with open('错误记录.txt', 'a+', encoding='utf-8') as f:
                f.write(url)
                f.write('\n')

    def save_xls(self, data):
        """
        保存数据
        data : 字典格式 必须和表头长度一样
        :return:
        """
        path = os.path.abspath('.') + r'/全系车型机油数据.xls'
        if not os.path.exists(path):
            # 创建一个新DataFrame并添加表头
            Header = ['首字母', '品牌', '厂商', '型号', '型号ID', '排量', '年份', '轮胎尺寸', '机油容量',
                      '机油型号', '机油价格', '合成级别', '机滤型号', '机滤价格', '获取时间']
            df = pd.DataFrame(columns=Header)
        else:
            df_read = pd.read_excel(path)
            df = pd.DataFrame(df_read)

        # 定义一行新数据 data为一个字典
        new = pd.DataFrame(data, index=[1])  # 自定义索引为：1 ，这里也可以不设置index

        # 把定义的新数据添加到原数据最后一行 ignore_index=True,表示不按原来的索引，从0开始自动递增
        df = df.append(new, ignore_index=True)

        # 保存数据 sheet_name工作表名 index是否添加索引 header表头
        df.to_excel(path, sheet_name='data', index=False, header=True)

    def record(self, url):
        """
        保存 下载记录
        :return:
        """
        with open('下载记录.txt', 'a+', encoding='utf-8') as f:
            f.write(url)
            f.write('\n')

    def shell(self):
        """
        执行Linux系统命令
        :return:
        """
        # 读取系统内存文件
        with open('/proc/meminfo', 'r') as f:
            contents = f.readlines()
            contents = [i.strip().replace(' ', '').split(':') for i in contents]

        MemTotal = [int(i[1].replace('kB', '')) for i in contents if i[0] == 'MemTotal'][0]  # 系统内存
        MemFree = [int(i[1].replace('kB', '')) for i in contents if i[0] == 'MemFree'][0]  # 可用内存

        if MemFree < int(MemTotal * 0.3):
            print(f'系统内存：{MemTotal} 可用内存：{MemFree}')
            print('可用内存低于系统内存30%,清理内存缓存数据!')
            os.system('echo 3 > /proc/sys/vm/drop_caches')
            return
        print(f'系统内存：{MemTotal} 可用内存：{MemFree}')

    def run(self):
        """
        获取基本参数拼接保养页面url保存
        :return:
        """
        with open('品牌名称.txt', 'r', encoding='utf-8') as f:
            contents = f.readlines()
            contents = [i.strip() for i in contents]
            for model in contents:
                # url编码
                cond_brand = '+'.join(model.split(' ')[:2]) + '+' + quote(model.split(' ')[-1])
                for u in self.get_model(cond_brand):  # 根据品牌获取型号ID
                    # 首字母 品牌 车厂 型号 型号ID 轮胎尺寸
                    first, brand, BrandType, CarName, ProductID, Tires = u
                    for displa in self.get_displacement(ProductID):  # 根据型号ID获取排量信息
                        for year in self.get_year(ProductID, displa):  # 根据型号ID、排量信息 获取年份
                            url = f'https://by.tuhu.cn/baoyang/{ProductID}/pl{displa}-n{year}.html'
                            # 保存请求保养参数的url
                            with open('url.txt', 'a+', encoding='utf-8') as f:
                                f.write(f'{first},{brand},{BrandType},{CarName},{ProductID},{displa},{year},{Tires},{url}')
                                f.write('\n')
                            print(f'第:{self.count} 条数据保存成功!')
                            self.count += 1

    def main(self):
        """
        请求保养页面 获取机油数据
        :return:
        """
        with open('下载记录.txt', 'r', encoding='utf-8') as f:
            contents = f.readlines()
            contents = [i.strip() for i in contents]

        new_time = (datetime.datetime.now() + datetime.timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')
        print(new_time)
        for line in open("url.txt", 'r', encoding='utf-8'):
            # 十分钟调用一次Linux系统命令
            # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # print(start_time)
            # if new_time > start_time:
            #     self.shell()
            #     time.sleep(3)
            #     print(f'清理缓存后系统状态：')
            #     self.shell()
            #     new_time = (datetime.datetime.now() + datetime.timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')

            content = line.split(',')
            first = content[0]
            brand = content[1]
            BrandType = content[2]
            CarName = content[3]
            ProductID = content[4]
            displa = content[5]
            year = content[6]
            Tires = content[7]
            url = content[-1].strip()
            # 判断是否已经下载过
            if url in contents:
                print(f'已下载跳过：{url}')
                continue
            tenance = self.get_maintenance(url)
            if not tenance:
                continue
            dosage, motor_oil, motor_oil_money, level, machine_filter, machine_filter_money = tenance
            data = {'首字母': first, '品牌': brand, '厂商': BrandType, '型号': CarName, '型号ID': ProductID,
                    '排量': displa, '年份': year, '轮胎尺寸': Tires, '机油容量': dosage, '机油型号': motor_oil,
                    '机油价格': motor_oil_money, '合成级别': level, '机滤型号': machine_filter,
                    '机滤价格': machine_filter_money, '获取时间': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            # 数据写入文件
            self.save_xls(data)
            # 保存下载记录
            self.record(url)
            print(f'第:{self.count} 条数据保存成功!')
            self.count += 1


if __name__ == '__main__':
    spider = Spider()
    # spider.run()
    spider.main()

