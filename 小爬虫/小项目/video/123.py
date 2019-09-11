
# import os
# path = os.getcwd()
#
# cmd = path + '/copy/b video/痴女責め連続射精16発/*.ts 1.mp4'
# print(cmd)
# res = os.popen(r'copy/b X:\project\project\小爬虫\小项目\video\video\痴女責め連続射精16発\*.ts 1.mp4')
# print(res.read())
#
# print(os.sep)

# import os
# print(os.getcwd())
# path="video/MIAA-079/"
# path_list=os.listdir(path)
# path_list=[i for i in path_list if 'ts' in i]
# print(path_list)
# # lambda 剔除
# path_list.sort(key=lambda x: int(x[:-3]))
# path_list = [path + i for i in path_list]
# print(path_list)
# print('+'.join(path_list))
#
# res = os.popen(f'copy/b {path_list} {"1.mp4"}')
# print(res.read())
import subprocess
import os
# path = os.getcwd() + '/video/MIAA-079/'
# os.chdir(path)
#
#
# r = subprocess.Popen(['python', r'merge.py'],  # 需要执行的文件路径
#                                  stdout=subprocess.PIPE,
#                                  stderr=subprocess.STDOUT,
#                                  bufsize=0)
#
# while r.poll() is None:
#     line = str(r.stdout.readline(), encoding='UTF-8')  # TODO 打包时改为GBK
#     line = line.strip()
#     if line:
#         print(line)





# import wget
# count=0
# while count<3: #count的值表示总共要下多少ts文件，要查阅m3u8文件
#     try:
#         result=wget.download("https://cdn.av01.tv/v2/20190529_2/miaa00079/content/file4500-67-v1.ts?hdnea=ip=194.156.230.114~st=1568096216~exp=1568182616~acl=/v2/20190529_2/miaa00079/content/*~hmac=100a1884a5a9c8f1e028cc67ae7f1fa6bb257f2d7589b84f20153ff098bd0022",
#                              out='video/')
#         count=count+1
#     except:
#         continue

# """多进程"""
# from multiprocessing import Pool
#
# # 创建进程池,执行10个任务
# pool = Pool(10)
# for i in range(30):
#     pool.apply_async(run, (i,))
# pool.close()
# pool.join()
import urllib.request, urllib.error, requests


# def user_proxy(proxy_addr, url):
#     import urllib.request
#     proxy = urllib.request.ProxyHandler({'http:': proxy_addr, 'https:': proxy_addr})
#     opener = urllib.request.build_opener(proxy)
#     urllib.request.install_opener(opener)
#     data = urllib.request.urlopen(url).read().decode('utf-8')
#     return data
#
#
# proxy_addr = "58.253.154.35:9999"
# data = user_proxy(proxy_addr, "http://httpbin.org/ip")
# print(data)
# print(len(data))


# import urllib.request
# url = 'http://httpbin.org/ip'
# proxies = {'http:': '195.9.162.186:8080'}
# proxy_support = urllib.request.ProxyHandler(proxies)
# # 创建opener
# opener = urllib.request.build_opener(proxy_support)
# # 安装opener，此后调用urlopen()时都会使用安装过的opener对象
# urllib.request.install_opener(opener)
# response = urllib.request.urlopen(url)
# html = response.read().decode('utf-8')
# print(html)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0'}
proxies = {
    "https": "http://103.111.55.58:3128",
}
url = 'https://www.baidu.com/'
response = requests.get(url, headers=headers, proxies=proxies, timeout=15)
# status_code 请求返回状态码
code = response.status_code
print(code)
# 查看本机ip，查看代理是否起作用
res = requests.get("http://httpbin.org/ip", headers=headers, proxies=proxies, verify=False, timeout=3)
print(res.text)


