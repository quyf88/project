# coding=utf-8
# 作者    ： Administrator
# 文件    ：requests常用语法.py
# IED    ：PyCharm
# 创建时间 ：2019/7/27 15:18
import json
import requests
"""
headers 请求头
proxies 代理
verify  忽略SSL提示
timeout 请求等待时间
"""
proxies = json.loads(requests.get('http://47.102.109.169:4006/getProxy/?dataTag=vps&num=1&verify=412037638').text)[0]
print(proxies)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0'}
# proxies = {
#     "http": "http://127.0.0.1:8888",
#     "https": "http://127.0.0.1:8888",
# }
url = 'https://www.baidu.com'
response = requests.get(url, headers=headers, proxies=proxies, verify=False, timeout=3)
# status_code 请求返回状态码
code = response.status_code
print(code)
# 查看本机ip，查看代理是否起作用
res = requests.get("http://httpbin.org/ip", headers=headers, proxies=proxies, verify=False, timeout=3)
print(res.text)


"""
requests post请求 提交图片
"""
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


# 接口
url = 'http://106.13.108.81:882//api/Baiduyz?token=5866ef7a9c779d6298dcdedc85c049a4'
# 图片
img = './img.jpg'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
    'Referer': url
}
multipart_encoder = MultipartEncoder(
            fields={  # 这里根据需要进行参数格式设置
                    'file': ('1.jpg', open(img, 'rb'), 'image/jpeg'),
                    })
headers['Content-Type'] = multipart_encoder.content_type
# 请求头必须包含Content-Type: multipart/form-data; boundary=${bound}
# 这里也可以自定义boundary
r = requests.post(url, data=multipart_encoder, headers=headers)
print(r.text)
