# coding=utf-8
# 作者    ： Administrator
# 文件    ：login.py
# IED    ：PyCharm
# 创建时间 ：2019/6/2 2:06
# import time
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
#
# """登录"""
# # 启动360浏览器
# # chrome_options = webdriver.ChromeOptions()
# # chrome_options.binary_location = r"C:\Users\Administrator\AppData\Roaming\360se6\Application\360se.exe"
# # chrome_options.add_argument(r'--lang=zh-CN')  # 启动参数
# # driver = webdriver.Chrome(chrome_options=chrome_options)
# driver = webdriver.Chrome('C:\Program Files (x86)\Chrome\chromedriver.exe')
# driver.get('https://mall.icbc.com.cn/index.html')
#
# print(driver)
# time.sleep(5)
# log = driver.find_element_by_id('userInfo').click()
# print(log)
#

# account = driver.find_element_by_class_name('floors_l_pic')
# account.sendKeys(Keys.PAGE_DOWN)


# def login(login_url, login_name, login_passwd):
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.binary_location = r"C:\Users\Administrator\AppData\Roaming\360se6\Application\360se.exe"
#     chrome_options.add_argument(r'--lang=zh-CN')  # 启动参数
#     driver = webdriver.Chrome(chrome_options=chrome_options)
#     driver.get(login_url)
#     time.sleep(5)
#
#     account = driver.find_element_by_id('logonName')
#     password = driver.find_element_by_id('nloginpwd')
#     submit = driver.find_element_by_id('loginsubmit')
#
#     account.clear()
#     password.clear()
#     account.send_keys(login_name)
#     password.send_keys(login_passwd)
#
#     submit.click()
#     time.sleep(5)
#
#     jd_cookies = driver.get_cookies()
#     driver.close()
#     return jd_cookies
#
#
# if __name__ == '__main__':
#     url = 'https://login.mall.icbc.com.cn/login?service=https%3A%2F%2Fmall.icbc.com.cn%2Fj_spring_cas_security_check'
#     name = input('请输入用户名:\n')
#     password = input('请输入密码:\n')
#     cookies = login(url, name, password)
#     print(cookies)





