"""
代理添加
设置本地代理 可用Fidder抓python请求包
"""


import requests

proxies = {
    "http": "http://127.0.0.1:8888",
    "https": "http://127.0.0.1:8888",
}

response = requests.get("https://www.baidu.com", verify=False, proxies=proxies)

print(response)
