# -*- coding: utf-8 -*-
# @Time    : 2019/7/3 13:38
# @Author  : project
# @File    : spider.py
# @Software: PyCharm
import csv
import json
import requests
import pandas as pd
from retrying import retry
from fake_useragent import UserAgent


class Spider:
    def __init__(self):
        # 获取随机请求头
        self.headers = {"User-Agent": UserAgent().random}

    @retry(stop_max_attempt_number=3)
    def _parse_url(self, url):
        """请求函数"""
        try:
            response = requests.get(url, headers=self.headers, timeout=3)
        except Exception as e:
            print(e)
            response = None
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
        for i in content:
            # 品牌首字母,名称,车系列表
            brand_l, brand_n, brand_list,  = i['L'], i['N'], i['List']
            for q in brand_list:
                # 车系名称,车型列表
                car_l, car_list = q['N'], q['List']
                for t in car_list:
                    # 车型ID, 车型名称
                    model_l = t['I']
                    model_n = t['N']
                    data = [brand_l, brand_n, car_l, model_n]
                    with open("model.csv", "a+", newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerows(data)
                        print('成功插入一条')
                    # yield brand_l, brand_n, car_l, model_n, model_l

    def get_dealer(self):
        """获取经销商信息"""
        for i in self.get_model():
            data = []
            brand_l, brand_n, car_l, model_n, model_l = i
            # 根据车型ID和区域编码获取经销商信息
            url = 'https://www.autohome.com.cn/ashx/dealer/AjaxDealersBySeriesId.ashx?seriesId={}&cityId=110100'.format(str(model_l))
            response = self._parse_url(url)
            # 无数据跳过
            if not response.json()['result']['list']:
                data.append([brand_l, brand_n, car_l, model_n])
                self.scv_data(data)
                print('暂无经销商信息')
                continue
            # 获取经销商信息 主要取经销商ID 用来获取价格
            contents = response.json()['result']['list']

            for con in contents:
                # dealer['dealerId'] = con['dealerId']  # 经销商ID
                dealerName = con['dealerInfoBaseOut']['dealerName']  # 经销商名称
                countyName = con['dealerInfoBaseOut']['countyName']  # 所在地区
                companySimple = con['dealerInfoBaseOut']['companySimple']  # 简称
                dealerAdd = con['dealerInfoBaseOut']['address']  # 地址
                orderRange = con['dealerInfoBaseOut']['orderRangeTitle']  # 销售区域
                phone = con['yphone']  # 电话
                showPhone = con['dealerInfoBaseOut']['showPhone']  # 400电话
                for u in self.get_price(str(con['dealerId']), str(model_l)):
                    SpecName, OriginalPrice, Price = u
                    data.append([brand_l, brand_n, car_l, model_n, SpecName, OriginalPrice,
                                 Price, dealerName, countyName, companySimple, dealerAdd, orderRange, phone, showPhone])
                self.scv_data(data)

    def get_price(self, dealerId, seriesId):
        """获取价格"""
        url = 'https://dealer.autohome.com.cn/Ajax/GetSpecListByDealer?dealerId={}&seriesId={}'.format(dealerId, seriesId)
        # 根据经销商ID 和 车型ID 获取车型价格
        response = self._parse_url(url)
        # 无数据跳过
        if not response.json()['result']['list']:
            print('暂无经销商信息')
            return
        # 获取经销商信息 主要取经销商ID 用来获取价格
        contents = response.json()['result']['list']
        for con in contents:
            # 汽车型号
            SpecName = con['SpecName']
            # 指导价
            OriginalPrice = con['OriginalPrice']
            # 参考价
            Price = con['Price']
            yield SpecName, OriginalPrice, Price

    def scv_data(self, data):
        """保存为csv"""
        with open("./CVE.csv", "a+", newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerows(data)
            print('成功插入一条')
        # df = pd.DataFrame(data)
        # df.to_csv('testcsv.csv', encoding='utf-8')
        # print('成功插入一条')


if __name__ == '__main__':
    spider = Spider()
    spider.get_model()
    # spider.get_dealer()

    # for i in a:
    #     print(i)