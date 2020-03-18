# -*- coding:utf-8 -*-
# 文件 ：spider.py
# IED ：PyCharm
# 时间 ：2020/3/16 0016 13:59
# 版本 ：V1.0
import os
import json
import datetime
import requests
import pandas as pd
from retrying import retry
from urllib.parse import quote

from ip_proxy import Proxy

print("os.path.abspath(__file__) = ", os.path.abspath(__file__))
PATH = os.getcwd()


class WeiBo:
    def __init__(self, word):
        self.words = word
        self.count = 1  # 记录数据存储数量
        self.proxies = None  # 代理IP
        self.expire_time = None  # 代理IP过期时间
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'
            }  # 请求头

        # self.headers = {
        #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
        #     'Host': 'weibo.com',
        #     'Cookie': 'SINAGLOBAL=4469623337200.637.1574044792390; login_sid_t=b903041d9b098166f2bfcda87cc96e16; cross_origin_proto=SSL; YF-V5-G0=125128c5d7f9f51f96971f11468b5a3f; _s_tentry=www.baidu.com; Apache=1405289944706.576.1583937754638; ULV=1583937754673:4:1:1:1405289944706.576.1583937754638:1581345875669; Ugrow-G0=6fd5dedc9d0f894fec342d051b79679e; UOR=,,login.sina.com.cn; SCF=Aim2CkP5Nrbss-5hxCtnIfHmRLMLqLLxbad_2x_TJsLiSuMgZrpHi-y93f4D7Lu0pbrjAF9yOJXsZzhNpe5jeAM.; SUHB=0k1ygmuQNci1dn; wb_view_log_6098207047=1366*7681; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WhLNNQI_kFFDD8rEnaFL3LD5JpVF0201h-0eh.4Shnf; SUB=_2AkMpMsIndcPxrAVRkfAXzGziaIpH-jya56vRAn7uJhMyAxh87ksfqSVutBF-XHF-LNmn3HArQ71ps0gNPPx2hvKj; WBStorage=42212210b087ca50|undefined; wb_view_log=1366*7681; YF-Page-G0=7f483edf167a381b771295af62b14a27|1584287391|1584287344; webim_unReadCount=%7B%22time%22%3A1584287448958%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D'
        #     }

    def proxy(self):
        """
        调用IP代理
        :return:
        """
        # 判断代理IP是否过期
        new_time = datetime.datetime.now()
        if self.expire_time and new_time < datetime.datetime.strptime(self.expire_time, "%Y-%m-%d %H:%M:%S"):
            # # 当前时间小于代理到期时间证明代理可用
            # if new_time < datetime.datetime.strptime(self.expire_time, "%Y-%m-%d %H:%M:%S"):
            print(f'当前使用代理IP:{self.proxies} 过期时间：{self.expire_time}')
            return
        proxy = Proxy()
        ip_port, expire_time = proxy.main()
        self.headers = proxy.headers
        self.proxies = {
            'http': 'socks5://{}'.format(ip_port),
            'https': 'socks5://{}'.format(ip_port)
        }
        self.expire_time = expire_time

    @retry(stop_max_attempt_number=5)
    def _parse_url(self, url):
        """
        请求模块
        :param url:
        :return:
        """
        try:
            response = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=10).text
        except:
            response = None
        return response

    def _parse_json(self, content):
        """
        解析json数据 提取个人信息资料
        :param content:
        :return:
        """
        cards = content['data']['cards']  # 数据列表
        for card in cards:
            try:
                data = {}
                data['用户id'] = card['mblog']['user']['id']  # 用户id
                data['用户名'] = card['mblog']['user']['screen_name']  # 用户名
                data['微博认证名称'] = card['mblog']['user']['verified_reason']  # 微博认证名称
                sex = card['mblog']['user']['gender']  # 性别
                data['性别'] = '女' if sex == 'f' else '男'
                data['简介'] = card['mblog']['user']['description']  # 简介
                data['粉丝数量'] = card['mblog']['user']['followers_count']  # 粉丝数量
                data['发布微博量'] = card['mblog']['user']['statuses_count']  # 发布微博量
                data['关注量'] = card['mblog']['user']['follow_count']  # 关注量
                data['用户头像'] = card['mblog']['user']['profile_image_url']  # 用户头像
                data['移动端地址'] = card['mblog']['user']['profile_url']  # 移动端地址
                data['关键词'] = self.words

                yield data
            except:
                # print('数据解析错误!')
                continue

    def save_xls(self, data):
        """
        保存数据
        data : 字典格式 必须和表头长度一样
        :return:
        """
        # 判断文件是否存在 如果存在则读取然后插入新数据，不存在则创建一个新DataFrame并添加表头
        file = f'{PATH}/数据/关键词-{self.words}.xlsx'
        Header = ['用户id', '用户名', '微博认证名称', '性别', '简介', '粉丝数量', '发布微博量', '关注量', '用户头像', '移动端地址', '关键词']
        if not os.path.exists(f'{PATH}/数据'):
            os.mkdir(f'{PATH}/数据')
        if not os.path.exists(file):
            # 创建一个新的文件 并写入表头
            df = pd.DataFrame(columns=Header)
        else:
            # 读取现有文件
            df_read = pd.read_excel(file)
            df = pd.DataFrame(df_read)
        # 定义一行新数据 data为一个字典
        new_data = pd.DataFrame(data, index=[1])  # 自定义索引为：1 ，这里也可以不设置index
        # 把定义的新数据添加到原数据最后一行 ignore_index=True,表示不按原来的索引，从0开始自动递增
        df = df.append(new_data, ignore_index=True)
        # 保存数据 sheet_name工作表名 index是否添加索引 header表头
        df.to_excel(file, sheet_name=self.words, index=False, header=True)

    def get_user_id(self):
        """
        根据关键词搜索 获取用户信息
        :return:
        """
        for page in range(1, 100000):
            # 请求数据
            url = f'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D{quote(self.words)}&page_type=searchall&page={str(page)}'
            print(url)
            # 获取代理IP
            # self.proxy()
            # 请求数据
            response = self._parse_url(url)
            if not response:
                print('获取数据失败!切换代理IP')
                self.expire_time = None
                continue
            # 解析存储数据
            content = json.loads(response)
            # 判断是否有数据
            if not content['ok']:
                print(f'content:{content["ok"]},{content["msg"]}')
                print(f'关键词:{self.words}无新数据,切换关键词.')
                print('*'*50)
                return None
            for data in self._parse_json(content):
                try:
                    self.save_xls(data)
                    print(f'第:{self.count}条数据保存成功!')
                    self.count += 1
                except Exception as e:
                    print(e)
                    print(data)
                    continue
            # time.sleep(3)


if __name__ == '__main__':
    words = '珠宝'
    weibo = WeiBo(words)
    weibo.get_user_id()