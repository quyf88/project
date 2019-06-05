# coding=utf-8
# 作者    ： Administrator
# 文件    ：login.py
# IED    ：PyCharm
# 创建时间 ：2019/6/2 2:06


from selenium import webdriver


driver = webdriver.Chrome("C:\Program Files (x86)\Chrome\chromedriver.exe")
driver.get('http://www.baidu.com')
print(1)