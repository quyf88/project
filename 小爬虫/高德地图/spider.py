# -*- coding:utf-8 -*-
# 文件 ：spider.py
# IED ：PyCharm
# 时间 ：2019/11/27 0027 11:03
# 版本 ：V1.0
"""
根据关键词搜索高德地图定位信息
"""
import csv
import json
import requests

COUNT = 0


def spider(keywords, city):
    # 获取数据页数
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'}
    url = f'https://restapi.amap.com/v3/place/text?keywords={keywords}&city={city}&citylimit=false&output=json&offset=20&page=1&key=d38b95abedd769ddca4f0842efbc3446&extensions=all'
    response = requests.get(url, headers=headers)
    response = response.content.decode('UTF-8')
    response = json.loads(response)
    page = int(int(response['count']) / 20)
    print(f'页数：{page}')

    for i in range(1, page):
        url = f'https://restapi.amap.com/v3/place/text?keywords={keywords}&city={city}&citylimit=false&output=json&offset=20&page={i}&key=d38b95abedd769ddca4f0842efbc3446&extensions=all'
        response = requests.get(url, headers=headers)
        response = response.content.decode('UTF-8')
        response = json.loads(response)
        # 数据列表
        pois = response['pois']

        data = []
        for poi in pois:
            pname = poi['pname']  # 省份
            pname = pname if len(pname) else None

            cityname = poi['cityname']  # 市
            cityname = cityname if len(cityname) else None

            adname = poi['adname']  # 区县
            adname = adname if len(adname) else None

            name = poi['name']  # 店铺名
            name = name if len(name) else None

            address = poi['address']  # 地址
            address = address if len(address) else None

            location = poi['location']  # 坐标
            location = location if len(location) else None

            tel = poi['tel']  # 电话
            tel = tel if len(tel) else None

            print(f'省份:{pname} 市:{cityname} 区县:{adname} 店铺名:{name} 地址:{address} 坐标:{location} 电话:{tel}')
            data.append([pname, cityname, adname, name, address, location, tel])
        scv_data(data, city)


def scv_data(data, city):
    """保存为csv"""
    city = city + '消防设备门店信息'
    with open(f"{city}.csv", "a+", encoding='utf-8', newline="") as f:
        k = csv.writer(f, delimiter=',')
        with open(f"{city}.csv", "r", encoding='utf-8', newline="") as f1:
            reader = csv.reader(f1)
            if not [row for row in reader]:
                k.writerow(['省份', '市', '区县', '店铺名', '地址', '坐标', '电话'])
                k.writerows(data)
            else:
                k.writerows(data)
    global COUNT
    COUNT += 1
    print(f'第[{COUNT}]页数据保存成功')


if __name__ == '__main__':
    keywords = input('关键词：')
    city = input('区域：')
    spider(keywords, city)