# -*- coding:utf-8 -*-
# 文件 ：豌豆IP代理.py
# IED ：PyCharm
# 时间 ：2020/3/14 0014 16:06
# 版本 ：V1.0
'''
在使用requests 时,

* 需要安装 pip install -U 'requests[socks]'

* 提取代理是选择socks5 协议

* 为运行程序的机器添加白名单

一天可以免费获取20个IP
'''
import json
import base64
import requests


class Proxy:
    def __init__(self):
        self.username = '1033383881@qq.com'  # 账号
        self.password = 'chenxiaoli2013'  # 密码

    def base_code(self):
        """账号密码base64加密 构造headers"""
        user_psd = f'{self.username}:{self.password}'
        encodestr = base64.b64encode(user_psd.encode('utf-8'))
        return encodestr.decode()

    def get_proxy_ip(self):
        """请求代理IP 一次返回一个IP地址"""
        url = r'http://api.wandoudl.com/api/ip?app_key=61056a77cc2115e31eb27ca62aec7ecc&pack=0&num=1&xy=1&type=2&lb=\n&mr=2&'
        res = requests.get(url, timeout=10)
        content = json.loads(res.text)
        if content['code'] != 200:
            print(f'代理IP获取失败:\n错误代码：{content["code"]}\nmsg:{content["msg"]}')
            return
        ip = content['data'][0]['ip']
        port = content['data'][0]['port']
        # proxy = f'{ip}:{port}'
        # print(proxy)
        return ip, port

    def censor_ip(self, ip):
        """效验代理是否可用"""
        # 效验请求IP地址 请求此url返回请求的IP地址
        url = "http://whatismyip.akamai.com/"  # 爱尔兰

        # 账号密码base64加密 构造headers
        basic_pwd = self.base_code()
        headers = {
            'Proxy-Authorization': f'Basic {basic_pwd}'
        }
        print(f'代理前IP：{requests.get(url, timeout=10).text}')
        # 代理
        proxy = {
            'http': ip,
            'https': ip
        }
        res = requests.get(url, proxies=proxy, headers=headers, timeout=10)
        print(f'代理后IP：{res.text}')
        return res.text

    def main(self):
        # 从api中提取出代理IP:PORT 一次提取一个
        ip, port = self.get_proxy_ip()
        if not ip:
            return
        ip_port = f'{ip}:{port}'
        res_ip = self.censor_ip(ip_port)
        if ip != res_ip:
            print(f'代理IP验证失败，IP:{ip}不可用')
            return
        print(f'ip:{ip}可用!')
        return ip


if __name__ == '__main__':
    proxy = Proxy()
    for i in range(20):
        print(f'*****第：{i+1}次*****')
        ip = proxy.main()

