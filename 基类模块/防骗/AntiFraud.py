#!/usr/bin/python
# -*- coding: utf-8 -*-
import json, urllib.request
from urllib.parse import urlencode


# ----------------------------------
# IP地址调用示例代码 － 聚合数据
# 在线接口文档：http://www.juhe.cn/docs/1
# 设置IP白名单验证 如果有不付尾款的就把IP地址从白名单删掉 程序就不能正常运行
# ----------------------------------

def main():
    # 配置您申请的APPKey
    appkey = "0d50a627fc695e5239d10504585ee6a2"

    # 1.根据IP/域名查询地址
    request1(appkey, "GET")


# 根据IP/域名查询地址
def request1(appkey, m="GET"):
    url = "http://apis.juhe.cn/ip/ip2addr"
    params = {
        "ip": "8.8.8.8",  # 需要查询的IP地址或域名
        "key": appkey,  # 应用APPKEY(应用详细页查询)
        "dtype": "",  # 返回数据的格式,xml或json，默认json
    }
    params = urlencode(params)
    if m == "GET":
        f = urllib.request.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.request.urlopen(url, params)

    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            # 成功请求
            print(res["result"])
        else:
            # print("%s:%s" % (res["error_code"], res["reason"]))
            if res["error_code"] == 10008:
                print('程序运行错误联系开发者!')
    else:
        print("request api error")


if __name__ == '__main__':
    main()