#!/usr/bin/env python 
# encoding: utf-8
# @version: v1.0
# @author: xxxx
# @site: 
# @software: PyCharm
# @file: spider.py
# @time: 2019/9/3 13:01

"""
短链接 转换 ：百度短链接
支付宝 转账接口：需要urlencode  from urllib.parse import quote
https://www.alipay.com/?appId=09999988&actionType=toCard&sourceId=bill&cardNo=银行卡号&bankAccount=银行账户名&money=转账金额&amount=备注&bankMark=银行英文简写&bankName=银行中文名称
查询银行代码
https://ccdcapi.alipay.com/validateAndCacheCardInfo.json?cardNo=填写卡号&cardBinCheck=true
"""
import os
import json
import string
import requests
from urllib.parse import quote  # url编码
from fake_useragent import UserAgent


class Spider:
    def __init__(self):
        self.headers = {'user-agent': str(UserAgent().random)}

    def get_url(self, lang_url):
        """
        长链接转换端链接
        0：正常返回短网址
        -1：短网址生成失败
        -2：长网址不合法
        -3：长网址存在安全隐患
        -4：内部错误
        -5：短网址服务目前不支持该域名
        -6：有效期设置错误
        -7：长网址在安全检测中
        -1xx：Token验证失败
        :param lang_url:
        :return:
        """
        # url 汉字转码  string.printable 跳过ascii码
        lang_url = quote(lang_url, string.printable)

        host = 'https://dwz.cn'
        path = '/admin/v2/create'
        url = host + path
        method = 'POST'
        content_type = 'application/json'
        # 设置Token
        token = '5e5dae6521ca463a43aa1063335e3792'
        # 设置待创建的长网址
        bodys = {'Url': lang_url, 'TermOfValidity': '1-year'}
        # 配置headers
        headers = {'Content-Type': content_type, 'Token': token}
        count = 1
        while True:
            # 发起请求
            response = requests.post(url=url, data=json.dumps(bodys), headers=headers)
            # 读取响应
            response = json.loads(response.text)
            if count > 3:
                print('程序运行错误,请联系开发者!')
                os._exit(0)
            if response['Code']:
                print('错误代码：{} 重试'.format(response['Code']))
                count += 1
                continue

            return response['ShortUrl']

    def code_generate(self, d_url):
        """
        https://www.juhe.cn/box/index/id/296
        二维码生成
        :return:
        """
        # 转码
        d_url = quote(d_url, string.digits)
        url = 'http://apis.juhe.cn/qrcode/api?text={}&el=&bgcolor=&fgcolor=&logo=&w=&m=&lw=&type=2&key=b142a4a659dfa5237bf54a78baf8382f'.format(d_url)


if __name__ == '__main__':
    spider = Spider()
    _url = 'https://www.alipay.com/?appId=09999988&actionType=toCard&sourceId=bill&cardNo=123&bankAccount=哈哈&money=12&amount=&bankMark=ABC&bankName=中国农业银行'
    d_url = spider.get_url(_url)
    spider.code_generate(d_url)