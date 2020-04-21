# -*- coding:utf-8 -*-
# 文件 ：批量添加子站.py
# IED ：PyCharm
# 时间 ：2019/10/23 0023 10:26
# 版本 ：V1.0

import re
import json
import time
import requests
from lxml import etree
from retrying import retry
from datetime import datetime
from multiprocessing import Pool
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


COUNT = 1


class Spider:
    def __init__(self):
        self.headers = {'user-agent': str(UserAgent().random)}
        self.count = 1

    # 如果请求超时让被装饰的函数反复执行三次，三次全部报错才会报错
    @retry(stop_max_attempt_number=5)
    def _parse_url(self, url):
        """
        请求模块
        :param url:
        :return:
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10).text
        except:
            response = None
        return response

    def get_page(self, url):
        """
        获取二级分类商品页数
        :return: 商品列表页数
        """
        response = self._parse_url(url)
        if not response:
            return
        html = etree.HTML(response)
        page = html.xpath('//*[@id="lblPageMsg"]/text()')
        page = re.findall(r'共有 (.*?) 页', page[0])[0]

        return page

    def get_commodity_url(self, page):
        """
        获取商品url列表
        :return:
        """
        for i in range(60001, 70001):
            print(page)
            url = f'http://www.chinaplc.net/plccp_vlist/35-p{i}.html'
            print(url)
            yield url

    def get_commodity(self, url, sort):
        """
        获取商品列表信息
        :return:
        """
        # 请求数据
        response = self._parse_url(url)
        if not response:
            with open('urls.txt', 'a+', encoding='utf-8') as f:
                f.write(url)
                f.write('\n')
            return
        html = etree.HTML(response)
        # 型号
        title = html.xpath('//*[@class="px14"]/text()')
        title = [i.split() for i in title]  # 剔除空格符
        title = [' '.join(i) for i in title]  # 拼接列表
        # print(title, len(title))
        # 详情
        content = html.xpath('//*[@class="f_gray"]/text()')
        # print(content, len(content))
        # 商品页URL
        detail_url = html.xpath('//*[@id="item_7225"]/table/tr/td[3]/ul/li[1]/a/@href')
        detail_url = [f'http://www.chinaplc.net{i}' for i in detail_url]
        # print(detail_url, len(detail_url))

        datas = zip(title, content, detail_url)
        self.save_data(datas, sort)
        # 爬取记录
        self.record(url)
        time.sleep(2)

    def save_data(self, datas, sort):
        """
        数据存储 json
        :return:
        """
        filename = 'PLC.json'
        for data in datas:
            # 添加分类
            data = list(data)
            data.insert(0, sort)
            # print(data, type(data))
            with open(filename, 'a+') as f:
                # ensure_ascii 不适用ascii编码 解决不能显示中文问题
                try:
                    json.dump(data, f, ensure_ascii=False)
                except:
                    continue
                # 插入换行符
                f.write('\n')
                global COUNT
                print(f'第：{COUNT}条数据成功写入!')
                COUNT += 1

    def record(self, data):
        """
        爬取记录
        :return:
        """
        with open('record.txt', 'w', encoding='utf-8') as f:
            f.write(data)

    @run_time
    def run(self):
        # 类目url PLC控制系统 工控机 工业以太网 交换机
        urls = {'PLC控制系统': 'http://www.chinaplc.net/plccp_vlist/35.html',
                }
        for url in urls.values():
            # 字典根据值找键
            sort = list(urls.keys())[list(urls.values()).index(url)]
            print(sort)
            # 获取商品列表页数
            page = self.get_page(url)

            # 创建进程池,执行5个任务
            print('创建进程池')
            pool = Pool(5)
            #  获取商品url列表
            for commodity_url in self.get_commodity_url(page):
                # 启动线程
                pool.apply_async(self.get_commodity, (commodity_url, sort))

            pool.close()
            pool.join()


if __name__ == '__main__':
    spider = Spider()
    spider.run()