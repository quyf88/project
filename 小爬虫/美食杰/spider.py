# -*- coding: utf-8 -*-
# @Time    : 2019/8/16 14:40
# @Author  : project
# @File    : 批量添加子站.py
# @Software: PyCharm
import re
import csv
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Spider:
    def __init__(self):
        print('**********程序启动中**********')
        # selenium无界面模式
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        # keep_alive 设置浏览器连接活跃状态
        # self.driver = webdriver.Chrome(chrome_options=chrome_options, keep_alive=False)
        print('**********程序启动成功**********')
        # 有界面模式
        self.driver = webdriver.Chrome(keep_alive=False)
        # 隐形等待时间
        self.wait = WebDriverWait(self.driver, 10, 0.5)
        # 浏览器窗口最大化
        self.driver.maximize_window()
        # 保存数据
        self.phone = 0
        self.number = 0
        self.rsp = None

    def get_cuisine(self):
        """
        获取菜系
        :return: 全部菜系列表 name + url
        """
        url = 'https://www.meishij.net/china-food/caixi'
        self.driver.get(url)
        html = self.driver.page_source

        # re.S 	使 . 匹配包括换行在内的所有字符  re.M 匹配多行
        # 匹配出全部菜系
        cuisine = re.findall(r'<dt>中华菜系</dt>(.*?)其它菜', html, re.S | re.M)
        cuisine = re.findall(r'<a href="(.*?)</a>', cuisine[0], re.S | re.M)
        cuisine = [i.replace('">', '') for i in cuisine]
        cuisines = []
        for cuisin in cuisine:
            cui = {}
            cui['name'] = re.search(r'[\u4e00-\u9fa5]+', cuisin).group()
            cui['url'] = re.search(r'[^\u4e00-\u9fa5]+', cuisin).group()
            cuisines.append(cui)
        return cuisines

    def get_dishes(self, cuisine):
        """
        根据菜系获取菜品信息
        :return:
        """
        print(cuisine, type(cuisine))
        url = cuisine['url']
        self.driver.get(url)
        dishes = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#listtyle1_list')))
        # get_attribute('innerHTML') 获取指定元素源代码
        response = dishes.get_attribute('innerHTML')
        result = etree.HTML(response)
        dishe_li = result.xpath('//*[@class="listtyle1"]')
        dishes = []
        for dishe in dishe_li:
            dish = {}
            dish['name'] = dishe.xpath('./a/@title')[0]
            dish['url'] = dishe.xpath('./a/@href')[0]
            dishes.append(dish)
        return dishes

    def get_practice(self, dishe):
        """
        获取菜品做法
        :return:
        """
        print(dishe)
        url = dishe['url']
        self.driver.get(url)
        practice = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.cp_body_left')))
        # get_attribute('innerHTML') 获取指定元素源代码
        response = practice.get_attribute('innerHTML')
        result = etree.HTML(response)
        # 用料
        # 简介
        material_con = result.xpath('//*[@class="materials"]//text()')
        material_con = ','.join([i for i in material_con if len(i.replace('\n', '').replace('\r', ''))])
        # 主料
        Ingredients = result.xpath('//*[@class="yl zl clearfix"]//text()')
        Ingredients = ','.join([i.strip() for i in Ingredients if len(i.strip())])
        # 辅料
        Excipient = result.xpath('//*[@class="yl fuliao clearfix"]//text()')
        Excipient = ','.join([i for i in Excipient if len(i.strip().replace('\n', '').replace('\r', ''))])
        # 做法
        step = result.xpath('//*[@class="content clearfix"]//text()')
        step = ','.join([i for i in step if len(i.strip())])
        # 注意事项
        artifice = result.xpath('//*[@class="editnew edit"]/input/@value')
        artifice = [i.replace('\n', '') for i in artifice]
        return material_con, Ingredients, Excipient, step, artifice

    def scv_data(self, data):
        """保存为csv"""
        with open("content.csv", "a+", encoding='utf-8', newline="") as f:
            k = csv.writer(f, delimiter=',')
            with open("content.csv", "r", encoding='utf-8', newline="") as f1:
                reader = csv.reader(f1)
                if not [row for row in reader]:
                    k.writerow(['菜系', '菜品', '简介', '主料', '辅料', '做法', '注意事项'])
                    k.writerows(data)
                else:
                    k.writerows(data)

    def run(self):
        cuisines = self.get_cuisine()
        for cuisine in cuisines:
            dishes = self.get_dishes(cuisine)
            for dishe in dishes:
                print('*'*50)
                print('{} {} 数据获取中!'.format(cuisine['name'], dishe['name']))
                material_con, Ingredients, Excipient, step, artifice = self.get_practice(dishe)
                data = [[cuisine['name'], dishe['name'],material_con, Ingredients, Excipient, step, artifice]]
                self.scv_data(data)
                print('{} {} 数据保存成功!'.format(cuisine['name'], dishe['name']))
                print('*' * 50, '\n')


if __name__ == '__main__':
    spider = Spider()
    spider.run()
