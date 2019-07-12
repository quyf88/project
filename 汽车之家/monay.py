# -*- coding: utf-8 -*-
# @Time    : 2019/7/3 13:38
# @Author  : project
# @File    : spider.py
# @Software: PyCharm
import re
import csv
import json
import requests
import threading
import pandas as pd
from datetime import datetime
from retrying import retry
from fake_useragent import UserAgent


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
                    yield brand_l, brand_n, car_l, model_n, model_l

    def model_csv(self):
        """保存所有车型数据"""
        data = []
        for i in self.get_model():
            brand_l, brand_n, car_l, model_n, model_l = i
            data.append([brand_l, brand_n, car_l, model_n, model_l, datetime.now()])
        name = ['品牌索引', '品牌名称', '车系名称', '车型', 'ID', '时间']
        df = pd.DataFrame(columns=name, data=data)
        df.to_csv('model.csv', mode='a', encoding='utf-8')
        print('车型数据保存成功')

    def get_car_market(self):
        """
        获取全国车市 主要取cityid
        :return:
        """
        with open('全国车市列表_汽车之家.html', 'r', encoding='GBK') as f:
            content = f.read()
        # re.S 	使 . 匹配包括换行在内的所有字符  re.M 匹配多行
        # 匹配出全国车市信息列表
        car_market = re.findall(r'var pdate =(.*?);', content, re.S | re.M)
        # str 转 json
        market_list = json.loads(car_market[0])
        data = []
        CityId_list = []
        for market in market_list:
            ProvinceFirst = market['ProvinceFirstCharacter']  # 区域代码
            ProvinceName = market['ProvinceName']  # 省
            ProvincePinyin = market['ProvincePinyin']  # 拼音
            ProvinceId = market['ProvinceId']  # ID
            CityList = market['CityList']  # 市列表

            for city in CityList:
                cityid_dict = {}
                # 保存
                # CityFirstCharacter = city['CityFirstCharacter']  # 区域代码
                # CityName = city['CityName']  # 市
                # CityPinyin = city['CityPinyin']  # 拼音
                # CityId = city['CityId']  # ID
                # CityLevel = city['CityLevel']  # 城市级别

                # 调取
                cityid_dict['CityName'] = city['CityName']  # 市
                cityid_dict['CityId'] = city['CityId']  # ID
                cityid_dict['CityLevel'] = city['CityLevel']  # 城市级别
                CityId_list.append(cityid_dict)
        #         data.append([ProvinceFirst, ProvinceName, ProvincePinyin, ProvinceId,
        #                      CityFirstCharacter, CityName, CityPinyin, CityId, CityLevel])
        # self.car_market_scv(data)
        return CityId_list

    def car_market_scv(self, data):
        """
        保存全国车市
        :return:
        """
        self.count += 1
        with open("全国车市.csv", "a+", encoding='utf-8', newline="") as f:
            k = csv.writer(f, delimiter=',')
            with open("全国车市.csv", "r", encoding='utf-8', newline="") as f1:
                reader = csv.reader(f1)
                if not [row for row in reader]:
                    k.writerow(['省级区域代码', '省', '拼音', '省ID', '市级区域代码', '市', '拼音', '市ID', '城市级别'])
                    k.writerows(data)
                    print('第[{}]条数据插入成功'.format(self.count))
                else:
                    k.writerows(data)
                    print('第[{}]条数据插入成功'.format(self.count))

    def get_dealer(self):
        """获取经销商信息"""
        # 车市列表 CityLevel 城市级别 相当于权重值
        count = 1
        cityid_num = 0
        cityid_li = self.get_car_market()
        cityid_list = [i for i in cityid_li if int(i['CityLevel']) == count]

        for model in self.get_model():
            brand_l, brand_n, car_l, model_n, model_l = model
            for i in range(329):
                cityid = cityid_list[cityid_num]['CityId']
                # 根据车型ID和区域编码获取经销商信息
                url = 'https://www.autohome.com.cn/ashx/dealer/AjaxDealersBySeriesId.ashx?seriesId={}&cityId={}'.format(str(model_l), str(cityid))
                print(url)
                response = self._parse_url(url)
                try:
                    if not response.json()['result']['list']:
                        print('**{}** 地区无 **{}** 经销商,切换地区获取'.format(cityid_list[cityid_num]['CityName'], model_n))
                        with open('a.txt', 'a', encoding='utf-8') as f:
                            f.write(str(model_l))
                            f.write('\n')
                            print('插入成功')
                        break
                        # if i + 1 == 329:
                        #     print(brand_l, brand_n, car_l, model_n, '无数据')
                        #     self.scv_data([[brand_l, brand_n, car_l, model_n, '无数据']])
                        #     count = 1
                        #     cityid_num = 0
                        #     cityid_list = [i for i in cityid_li if int(i['CityLevel']) == count]
                        #     break
                        # if len(cityid_list)-1 > cityid_num:
                        #     cityid_num += 1
                        #     continue
                        # if count < 5:
                        #     count += 1
                        #     cityid_num = 0
                        #     cityid_list = [i for i in cityid_li if int(i['CityLevel']) == count]
                        #     continue
                        # else:
                        #     count = 1
                        #     cityid_num = 0
                        #     cityid_list = [i for i in cityid_li if int(i['CityLevel']) == count]
                        #     continue
                except:
                    print('获取信息失败，切换地区获取')
                    break
                # 获取经销商信息 主要取经销商ID 用来获取价格
                contents = response.json()['result']['list'][0]
                print('[{}{}]数据请求中'.format(car_l, model_n))

                data = []
                dealerId = contents['dealerId']  # 经销商ID
                for u in self.get_price(str(dealerId), str(model_l)):
                    SpecName, front_tire, rear_tire = u
                    data.append([brand_l, brand_n, car_l, model_n, SpecName, front_tire, rear_tire, datetime.now()])

                    print('[{} {}]'.format(model_n, SpecName))
                    print(SpecName, front_tire, rear_tire)
                self.scv_data(data)
                break

    def get_price(self, dealerId, seriesId):
        """获取汽车型号ID"""
        url = 'https://dealer.autohome.com.cn/Ajax/GetSpecListByDealer?dealerId={}&seriesId={}'.format(dealerId, seriesId)
        # 根据经销商ID 和 车型ID 获取车型价格
        response = self._parse_url(url)
        # 无数据跳过
        if not response.json()['result']['list']:
            print('暂无经销商信息')
            return
        contents = response.json()['result']['list']
        for con in contents:
            # 汽车型号
            SpecName = con['SpecName']
            # 汽车型号ID 获取车型信息用
            SpecId = con['SpecId']
            front, rear = self.tire_size(SpecId)
            yield SpecName, front, rear

    def tire_size(self, SpecId):
        """获取轮胎尺寸信息"""
        url = 'https://dealer.autohome.com.cn/Price/_SpecConfig?&SpecId={}'.format(SpecId)
        print(url)
        response = self._parse_url(url)
        content = response.text
        # 前轮胎
        pattern = re.compile(r'\s|\n|<td>', re.S)
        front_tire = re.findall(r'<th>前轮胎规格</th>(.*?)</td>', content, re.S | re.M)
        if not len(front_tire):
            return '暂无数据', '暂无数据'
        front_tire = pattern.sub('', front_tire[0])
        # 后轮胎
        rear_tire = re.findall(r'<th>后轮胎规格</th>(.*?)</td>', content, re.S | re.M)[0]
        rear_tire = pattern.sub('', rear_tire)

        return front_tire, rear_tire

    def scv_data(self, data):
        """保存为csv"""
        self.count += 1
        with open("全系轮胎数据.csv", "a+", encoding='utf-8', newline="") as f:
            k = csv.writer(f, delimiter=',')
            with open("全系轮胎数据.csv", "r", encoding='utf-8', newline="") as f1:
                reader = csv.reader(f1)
                if not [row for row in reader]:
                    k.writerow(['品牌索引', '品牌名称', '车系名称', '车型', '汽车型号', '前轮胎规格', '后轮胎规格', '时间'])
                    k.writerows(data)
                    print('第[{}]条数据插入成功'.format(self.count))
                else:
                    k.writerows(data)
                    print('第[{}]条数据插入成功'.format(self.count))

    @run_time
    def run(self):
        # 获取车型数据
        # self.model_csv()
        # 获取所有信息
        self.get_dealer()
        # self.model_csv()


if __name__ == '__main__':
    spider = Spider()
    spider.run()
