# -*- coding:utf-8 -*-
# 文件 ：spider.py
# IED ：PyCharm
# 时间 ：2020/2/13 0013 21:30
# 版本 ：V1.0
import os
import re
import csv
import json
import time
import requests
from lxml import etree
from retrying import retry
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class Spider:
    def __init__(self):
        self.headers = {'User-Agent': str(UserAgent().random),
                        'Cookie': 'safedog-flow-item=8B365A1B4F48E2B0C88026FAF62B83DF; UM_distinctid=1703db623ed216-00af6cc0a9ebe2-67e153a-100200-1703db623ee5cc; CNZZDATA1309589=cnzz_eid%3D1916040425-1581598490-http%253A%252F%252Fwww.yanglee.com%252F%26ntime%3D1581598490',
                        # 必须加上此参数 不然获取不到信息
                        'referer': 'http://www.yanglee.com/Product/Index.aspx'}
        chrome_options = Options()
        desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
        desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        prefs = {"profile.managed_default_content_settings.images": 2}  # 1 加载图片 2不加载图片,加快访问速度
        chrome_options.add_experimental_option("prefs", prefs)
        # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.wait = WebDriverWait(self.driver, 60, 1)  # 设置隐式等待时间
        self.driver.maximize_window()  # 窗口最大化

        self.count = 1

    # @retry(stop_max_attempt_number=5)
    def get_id(self):
        """获取信托产品id"""
        for i in range(298, 304):
            print(f'获取第{i}页数据')
            url = f'http://www.yanglee.com/Action/ProductAJAX.ashx?mode=statistics&pageSize=40&pageIndex={i}&conditionStr=producttype%3A1&start_released=&end_released=&orderStr=1&ascStr=ulup&_=1581599843718'
            res = requests.get(url, headers=self.headers, timeout=30)
            content = json.loads(res.text)
            results = content['result']
            for result in results:
                Title = result['Title']
                ID = result['ID']
                # print(Title, ID, '写入成功!')
                with open('a.txt', 'a+', encoding='utf-8') as f:
                    f.write(f'{Title},{ID}')
                    f.write('\n')
            print(f'第{i}页数据保存成功')

    def selenium_get(self, url):
        # 限定页面加载时间最大为100秒
        self.driver.set_page_load_timeout(100)
        try:
            self.driver.get(url)
            return True
        except:
            print(u'页面加载超时!')
            # 当页面加载时间超过设定时间，通过执行Javascript来停止载，然后继续执行后续操作
            self.driver.execute_script('window.stop()')
            # 保存错误记录
            with open('错误记录.txt', 'a+', encoding='utf-8') as f:
                f.write(url)
                f.write('\n')
            return False

    def get_detail(self):
        """获取产品详细信息"""
        for i in self.read_id():
            url = f'http://www.yanglee.com/Product/Detail.aspx?id={i}'
            print(url)
            if not self.selenium_get(url):
                continue
            html = etree.HTML(self.driver.page_source)
            # 基础信息
            oview = html.xpath('//div[@id="procon1"]/table/tbody/tr/td/text()')
            oview = ' '.join(oview)
            try:
                # 产品名称
                name = re.findall(r'产品名称(.*?)产品类型', oview)[0].replace(' ', '')

                # 产品类型
                types = re.findall(r'产品类型(.*?)产品状态', oview)[0].replace(' ', '')
                # 产品状态
                status = re.findall(r'产品状态(.*?)发行机构', oview)[0].replace(' ', '')
                # 发行机构
                agency = re.findall(r'发行机构(.*?)投资门槛', oview)[0].replace(' ', '')
                # 投资门槛
                threshold = re.findall(r'投资门槛(.*?)发行地', oview)[0].replace(' ', '')
                # 发行地
                issued = re.findall(r'发行地(.*?)收益分配方式', oview)[0].replace(' ', '')
                # 收益分配方式
                allocation = re.findall(r'收益分配方式(.*?)发行时间', oview)[0].replace(' ', '')
                # 发行时间
                publish = re.findall(r'发行时间(.*?)发行规模', oview)[0].replace(' ', '')
                # 发行规模
                scale = re.findall(r'发行规模(.*?)成立时间', oview)[0].replace(' ', '')
                # 成立时间
                established = re.findall(r'成立时间(.*?)成立规模', oview)[0].replace(' ', '')
                # 成立规模
                shed_scale = re.findall(r'成立规模(.*?)产品期限', oview)[0].replace(' ', '')
                # 产品期限
                Product_term = re.findall(r'产品期限(.*?)期限类型', oview)[0].replace(' ', '')
                # 期限类型
                term_type = re.findall(r'期限类型(.*?)预计收益', oview)[0].replace(' ', '')
                # 预计收益
                income = re.findall(r'预计收益(.*?)收益类型', oview)[0].replace(' ', '')
                # 收益类型
                income_type = re.findall(r'收益类型(.*?)投资方式', oview)[0].replace(' ', '')
                # 投资方式
                investment = re.findall(r'投资方式(.*?)资金托管行', oview)[0].replace(' ', '')
                # 资金托管行
                CustodyBank = re.findall(r'资金托管行(.*?)投资领域', oview)[0].replace(' ', '')
                # 投资领域
                field = re.findall(r'投资领域(.*?)投资项目所在地', oview)[0].replace(' ', '')
                # 投资项目所在地
                location = re.findall(r'投资项目所在地(.*?)产品特点', oview)[0].replace(' ', '')
                # 产品特点
                Features = html.xpath('//*[@id="procon1"]/table/tbody/tr[11]/td[2]/p/text()')
                # 其他相关信息
                related = html.xpath('//*[@id="procon1"]/table/tbody/tr[12]/td[2]/p/text()')
                # print(f'产品特点：{Features} 其他相关信息：{related}')

                # 融资方
                Financiers = html.xpath('//*[@id="t3"]/p/text()')
                Financiers = Financiers[0] if Financiers else ''
                # print(f'融资方：{Financiers}')
                # 资金用途
                funds = html.xpath('//*[@id="t4"]/p/text()')
                funds = funds[0] if funds else ''
                # print(f'资金用途：{funds}')
                # 还款来源
                repayment = html.xpath('//*[@id="t5"]/p/text()')
                repayment = repayment[0] if repayment else ''
                # print(f'还款来源：{repayment}')
                # 风控措施
                measures = html.xpath('//*[@id="t6"]/p/text()')
                measures = measures[0] if measures else ''
                # print(f'风控措施：{measures}')
                # 资产管理人
                Assetmanager = html.xpath('//*[@id="t7"]/p/text()')
                Assetmanager = Assetmanager[0] if Assetmanager else ''
            except:
                with open('错误记录.txt', 'a+', encoding='utf-8') as f:
                    f.write(url)
                    f.write('\n')
                continue
            # print(f'资产管理人：{Assetmanager}')
            data = [[name, types, status, agency, threshold, issued, allocation, publish, scale, established,
                     shed_scale, Product_term, term_type, income, income_type, investment, CustodyBank, field,
                     location, Features, related, Financiers, funds, repayment, measures, Assetmanager]]
            data = [[i if i else '无' for i in data[0]]]
            self.save_data(data)

        self.driver.quit()

    def read_id(self):
        """读取产品ID"""
        with open('a.txt', 'r', encoding='utf-8') as f:
            contents = [i.replace('\n', '') for i in f.readlines()]
            for content in contents:
                content = content.split(',')[1]
                yield content

    def save_data(self, data):
        """保存为csv"""
        with open("1.csv", "a+", encoding='utf-8', newline="") as f:
            k = csv.writer(f, delimiter=',')
            with open("1.csv", "r", encoding='utf-8', newline="") as f1:
                reader = csv.reader(f1)
                if not [row for row in reader]:
                    k.writerow(['产品名称', '产品类型', '产品状态', '发行机构', '投资门槛', '发行地', '收益分配方式',
                                '发行时间', '发行规模', '成立时间', '成立规模', '产品期限', '期限类型', '预计收益',
                                '收益类型', '投资方式', '资金托管行', '投资领域', '投资项目所在地	', '产品特点', '其他相关信息',
                                '融资方', '资金用途', '还款来源', '风控措施', '资产管理人'])
                    k.writerows(data)
                else:
                    k.writerows(data)
            print(f'第：{self.count}条数据插入成功!')
            self.count += 1


if __name__ == '__main__':
    spider = Spider()
    # spider.get_id()
    spider.get_detail()
