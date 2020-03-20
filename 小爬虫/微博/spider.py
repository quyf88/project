# -*- coding:utf-8 -*-
# 文件 ：spider.py
# IED ：PyCharm
# 时间 ：2020/3/16 0016 13:59
# 版本 ：V1.0
import os
import time
import json
import datetime
import requests
import pandas as pd
from retrying import retry
from urllib.parse import quote
from configparser import ConfigParser

from ip_proxy import Proxy

print("os.path.abspath(__file__) = ", os.path.abspath(__file__))
PATH = os.getcwd()


def red_config():
    """
    读取配置文件
    :return: 代理状态
    """
    cp = ConfigParser()  # 实例化
    cp.read(f'{PATH}/config/config.ini', encoding='utf-8')  # 读取文件
    proxy_statu = cp.get('Status', 'proxy')  # 读取值
    return proxy_statu


class WeiBo:
    def __init__(self, word):
        self.fail_num = 0  # 请求失败次错
        self.words = word  # 关键词
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

    def _proxy(self):
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
            if not response:
                return None
            return response
        except:
            return None

    def _get_userid(self, response):
        """
        提取userid 拼接个人信息接口
        :param content:
        :return:
        """
        userid = []
        content = json.loads(response)
        cards = content['data']['cards']  # 数据列表
        for card in cards:
            if card['card_type'] != 11:  # 状态=11返回的是用户数据列表
                continue
            for card_group in card['card_group']:
                userid.append(card_group['user']['id'])  # 用户id

        return userid

    def _verify_response(self, response):
        """
        判断response是否有数据
        :param response:
        :return:True 有数据， False 无数据
        """
        if not response:
            print('获取数据失败!切换IP重试!')
            self.expire_time = None
            self._proxy()
            return False
        return True

    def _verify_json(self, response):
        """
        效验返回的json中是否有数据
        :return:
        """
        content = json.loads(response)
        # content['ok']=1有数据，0没有数据
        if not content['ok']:
            return False
        return True

    def _parse_json(self, res):
        """
        解析个人信息
        :param content:
        :return:
        """
        content = json.loads(res)

        data = {}
        data['用户id'] = content['data']['userInfo']['id']  # userid
        data['用户名'] = content['data']['userInfo']['screen_name']  # 用户名
        # 性别
        sex = content['data']['userInfo']['gender']
        data['性别'] = '女' if sex == 'f' else '男'
        # 微博认证名称
        verified = content['data']['userInfo']['verified']  # 认证状态
        data['微博认证名称'] = '无认证信息' if not verified else content['data']['userInfo']['verified_reason']
        data['简介'] = content['data']['userInfo']['description']  # 简介
        data['粉丝数量'] = content['data']['userInfo']['followers_count']  # 粉丝数量
        data['发布微博量'] = content['data']['userInfo']['statuses_count']  # 发布微博量
        data['关注量'] = content['data']['userInfo']['follow_count']  # 关注量
        data['用户头像'] = content['data']['userInfo']['profile_image_url']  # 用户头像
        data['移动端地址'] = content['data']['userInfo']['profile_url']  # 移动端地址
        data['关键词'] = self.words

        return data

    def _save_xls(self, data):
        """
        保存数据
        data : 字典格式 必须和表头长度一样
        :return:
        """
        # 判断文件是否存在 如果存在则读取然后插入新数据，不存在则创建一个新DataFrame并添加表头
        file = f'{PATH}/数据/关键词-{self.words}.xlsx'
        Header = ['用户id', '用户名', '性别', '微博认证名称', '简介', '粉丝数量', '发布微博量', '关注量', '用户头像', '移动端地址', '关键词']
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

    def run(self):
        """
        根据关键词搜索 获取用户信息
        :return:
        """
        for page in range(1, 100000):
            # 根据关键词获取相匹配的用户信息
            # 数据分类:1综合，3用户，61实时， 62关注， 64视频， 58问答， 21文章，63图片， 87同城， 60热门， 38图片， 32主页
            chanenl = 3
            print(f'第:{page}页数据获取中...')
            url = f'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D{chanenl}%26q%3D{quote(self.words)}&page_type=searchall&page={page}'
            # print(url)
            # 获取代理IP
            # self._proxy()
            # 搜索关键词获取userid
            response = self._parse_url(url)
            # 判断是否请求成功
            if not self._verify_response(response):
                continue
            # 效验返回结果中是否有数据
            if not self._verify_json(response):
                if self.fail_num > 3:
                    self.fail_num = 0  # 初始化错误计数
                    print(f'关键词:[{self.words}]无新数据,切换关键词.')
                    print('*' * 50)
                    return None
                self.fail_num += 1
                continue

            # 解析json数据获取userid列表
            userids = self._get_userid(response)

            # 根据userid获取个人信息
            for userid in userids:
                user_url = f'https://m.weibo.cn/api/container/getIndex?title=%E5%9F%BA%E6%9C%AC%E8%B5%84%E6%96%99&type=uid&value={userid}'
                # print(user_url)
                res = self._parse_url(user_url)  # 请求个人信息接口
                # 判断是否有返回数据
                if not self._verify_response(res):
                    continue
                # 判断返回json中是否有数据
                if not self._verify_json(res):
                    print(f'id:{userid},获取数据失败!')
                    continue
                data = self._parse_json(res)  # 解析
                try:
                    self._save_xls(data)
                    print(f'第:{self.count}条数据保存成功!')
                    self.count += 1
                except Exception as e:
                    print(e)
                    print(data)
                    continue
                time.sleep(1)
            print(f'第:{page}页数据获取完成，切换下一页。')
            print('*'*50)


if __name__ == '__main__':
    words = '时尚博主'
    weibo = WeiBo(words)
    weibo.run()
    # print(red_config())