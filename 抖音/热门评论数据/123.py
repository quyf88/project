# coding=utf-8
# 作者    ： Administrator
# 文件    ：123.py
# IED    ：PyCharm
# 创建时间 ：2019/11/10 18:47
from urllib.parse import quote, unquote

url = 'https://www.alipay.com/?appId=60000154&url=%2Fwww%2Findex%2Fdetail.htm%3FbatchNo%3D20191110000750021000170018348542%26token%3DpGeJbKLN%26source%3DqrCode'
print(unquote(url))