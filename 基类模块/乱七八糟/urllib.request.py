"""请求数据时添加cookie"""
import urllib.request, http.cookiejar

# 1、网址url  --百度
url = 'http://www.baidu.com'

# 2、创建cookie容器
cj = http.cookiejar.CookieJar()
handle = urllib.request.HTTPCookieProcessor(cj)

# 3、创建1个opener
opener = urllib.request.build_opener(handle)

# 4、给urllib.request安装opener
urllib.request.install_opener(opener)

# 5、使用带有cookie的urllib.request访问网页,发送请求返回结果
response = urllib.request.urlopen(url)
htmldata = response.read()

# 6、设置编码方式
data = htmldata.decode("utf-8")

# 7、打印结果
print(data)

# 8、打印爬去网页的各类信息
print("response的类型:", type(response))
print("请求的url:", response.geturl())
print("响应的信息:", response.info())
print("状态码:", response.getcode())

# 9、爬取数据保存到文件
# fileOb = open('baiduCookie.html', 'w', encoding='utf-8')  # 打开一个文件，没有就新建一个
# fileOb.write(data)
# fileOb.close()

