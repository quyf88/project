#!/usr/bin/env python 
# encoding: utf-8
# @version: v1.0
# @author: xxxx
# @site: 
# @software: PyCharm
# @file: 123.py
# @time: 2019/9/3 16:12

a = -5

from urllib.parse import quote
import string

url = 'https://dwz.cn/Tx7OJ6NO'

print(quote(url, string.digits))