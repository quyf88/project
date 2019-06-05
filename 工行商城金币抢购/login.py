# coding=utf-8
# 作者    ： Administrator
# 文件    ：login.py
# IED    ：PyCharm
# 创建时间 ：2019/6/2 2:06

from selenium import webdriver

# 启动360浏览器
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = r"C:\Users\Administrator\AppData\Roaming\360se6\Application\360se.exe"
chrome_options.add_argument(r'--lang=zh-CN')  # 启动参数
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get('https://login.mall.icbc.com.cn/login?service=https%3A%2F%2Fmall.icbc.com.cn%2Fj_spring_cas_security_check')

