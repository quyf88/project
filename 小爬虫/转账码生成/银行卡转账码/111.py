# -*- coding:utf-8 -*-
# 文件 ：111.py
# IED ：PyCharm
# 时间 ：2020/4/27 0027 15:48
# 版本 ：V1.0
import os

print(os.path.abspath(__file__))  # 当前文件绝对路径
PATH = os.getcwd()  # 文件路径


from urllib.parse import unquote, quote

print(quote('https://77700152.h5app.alipay.com/index.html&url=/card-creation/index'))
a = 'https://ds.alipay.com/?from=mobilecodec&scheme=alipays%3A%2F%2Fplatformapi%2Fstartapp%3FappId%3D20000200%26actionType%3DtoCard%26sourceId=bill%26cardNo=6228480848862792670%26bankAccount=%E7%94%B0%E6%A1%82%E7%91%9E%0A%26money=99999%26amount=%26bankMark=ABC%26bankName=%E6%8B%9B%E5%95%86%E9%93%B6%E8%A1%8C%26cardNoHidden=true%26cardChannel=HISTORY_CARD%26orderSource=from'

print(unquote(a))

print(unquote('alipays://platformapi/startapp?appId=60000010&amp;url=%2Fwww%2Ftransfer_card%2Fcard-list.htm&amp;canPullDown=NO&amp;allowsBounceVertical=NO&amp;nbupdate=syncforce&amp;nbversion=0.50.1907291615.51'))
