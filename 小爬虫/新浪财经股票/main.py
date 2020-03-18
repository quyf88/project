# coding=utf-8
# 作者    ： Administrator
# 文件    ：main.py
# IED    ：PyCharm
# 创建时间 ：2019/6/19 20:04

import os
import demjson
import logging
import requests
from lxml import etree
from datetime import datetime
import mysql_conn


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
        self.conn = mysql_conn.BaseDao()
        self.conn.del_data()
        # self.log = self.log_init()
        self.headers = {'User-Agent':
                            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'
                    }

    # def log_init(self):
    #     """日志模块"""
    #     path = os.path.abspath('.') + r'\log\run.log'
    #     formatter = logging.Formatter('%(asctime)s | %(name)-6s | %(levelname)-6s| %(message)s')
    #     console = logging.StreamHandler()
    #     console.setLevel(logging.DEBUG)
    #     fh = logging.FileHandler(path, encoding='utf-8', mode='w')
    #     fh.setLevel(logging.DEBUG)
    #     fh.setFormatter(formatter)
    #     console.setFormatter(formatter)
    #     # 如果需要同時需要在終端上輸出，定義一個streamHandler
    #     # print_handler = logging.StreamHandler()  # 往屏幕上输出
    #     # print_handler.setFormatter(formatter)  # 设置屏幕上显示的格式
    #     logger = logging.getLogger("Spider")
    #     # logger.addHandler(print_handler)
    #     logger.setLevel(logging.DEBUG)
    #     logger.addHandler(console)
    #     logger.addHandler(fh)
    #     return logger

    def get_page(self):
        url = 'http://vip.stock.finance.sina.com.cn/mkt/#stock_hs_up'
        response = requests.get(url, headers=self.headers, timeout=3)
        content = response.content.decode('gbk')
        etree_html = etree.HTML(content)

        # 提取数据并处理
        total = etree_html.xpath('//div[@id="list_pages_top2"]/a')  # 总页数

    def run(self):
        for i in range(92):
            url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page={}&num=40&sort=changepercent&asc=0&node=hs_a&symbol=&_s_r_a=init'.format(i)
            response = requests.get(url, headers=self.headers, timeout=3)
            contents = response.content.decode('gbk')
            # demjson 解决json中不带双引号的key的问题
            content_list = demjson.decode(contents)

            data = []
            for content in content_list:
                fields = {}
                # 股票代码
                fields['symbol'] = content['symbol']
                # 名称
                fields['name'] = content['name']
                # 最新价
                # fields['trade'] = str(content['trade'])
                # # 涨跌额
                # fields['pricechange'] = str(content['pricechange'])
                # # 涨跌幅
                # fields['changepercent'] = str(content['changepercent'])
                # # 买入
                # fields['buy'] = str(content['buy'])
                # # 卖出
                # fields['sell'] = str(content['sell'])
                # # 昨收
                # fields['settlement'] = str(content['settlement'])
                # # 今开
                # fields['opens'] = str(content['open'])
                # # 最高
                # fields['high'] = str(content['high'])
                # # 最低
                # fields['low'] = str(content['low'])
                # # 成交量
                # fields['volume'] = str(content['volume'])
                # # 成交额
                # fields['amount'] = str(content['amount'])
                data.append(fields)
            self.sql_save(data)

    def sql_save(self, data):

        for d in data:
            with open('url.txt', 'a+', encoding='utf-8') as f:
                f.write(str(d))
                f.write('\n')
                print("成功写入1")

            # self.conn.add_update_del_seek(d)


if __name__ == '__main__':
    spider = Spider()
    spider.run()