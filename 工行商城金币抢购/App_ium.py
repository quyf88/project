# -*- coding: utf-8 -*-
# @Time    : 2019/6/6 9:58
# @Author  : project
# @File    : App_ium.py
# @Software: PyCharm


# -*- coding: utf-8 -*-
# @Time    : 2019/5/20 10:09
# @Author  : project
# @File    : 中青看点.py
# @Software: PyCharm
import time
import winsound
from datetime import datetime
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
"""融e购商城"""


def run_time(func):
    def new_func(*args, **kwargs):
        start_time = datetime.now()
        print("程序开始时间：{}".format(start_time))
        func(*args, **kwargs)
        end_time = datetime.now()
        print("程序结束时间：{}".format(end_time))
        print("程序执行用时：{}s".format((end_time - start_time)))

    return new_func

desired_caps = {
              "automationName": "uiautomator2",  # 引擎
              "platformName": "Android",
              "deviceName": "127.0.0.1:62001",
              "appPackage": "com.icbc.emallmobile",
              "appActivity": "com.icbc.ui.activiy.WelcomePageActivity",
              "noReset": True,
              "platformVersion": "5.1.1"  # 模拟器版本号
            }
driver_server = 'http://127.0.0.1:4723/wd/hub'
print('APP启动...')
# 启动APP
driver = webdriver.Remote(driver_server, desired_caps)
# 设置等待
wait = WebDriverWait(driver, 30, 0.5)

time.sleep(8)
# 进入工银金行家
secondary_page_xpath = '//*[@resource-id="com.icbc.emallmobile:id/ll_platform"]/android.widget.TableRow[1]/android.widget.LinearLayout[4]'
secondary_page = wait.until(EC.presence_of_element_located((By.XPATH, secondary_page_xpath)))
secondary_page.click()

# 进入邮币馆
postal_hall_id = 'com.icbc.emallmobile:id/sdv_ad'
postal_hall = wait.until(EC.presence_of_element_located((By.ID, postal_hall_id)))
postal_hall.click()
print(driver.contexts)

# 识别webview
time.sleep(8)
for i in driver.contexts:
    if i == 'WEBVIEW_com.icbc.emallmobile':
        while True:
            try:
                driver.switch_to.context(i)
                now = driver.current_context
                print('进入', now)
                break
            except Exception as e:
                print(e)
                continue
        break
    else:
        continue

# 进入商品详情页
commodity_xpath = "//*[@id=\"sale1\"]/ul/li[1]"
secondary_page = wait.until(EC.presence_of_element_located((By.XPATH, commodity_xpath)))
secondary_page.click()

# 切换为原生状态
driver.switch_to.context("NATIVE_APP")
print('进入', driver.current_context)

# 选择商品规格
home_buy_id = "com.icbc.emallmobile:id/comm_right_to_buy_tv"
home_buy = wait.until(EC.presence_of_element_located((By.ID, home_buy_id)))
home_buy.click()
print('点击立即购买')

# 获取所有商品规格
text = '金银套（8克金+30克银*3）'
option_id = "com.icbc.emallmobile:id/radio_color"
option_list = wait.until(EC.presence_of_all_elements_located((By.ID, option_id)))
for option in option_list:
    print(option.get_attribute("text"))
    if option.get_attribute("text") == text:
        option.click()
        break
    else:
        continue

# 立即购买
popup_buy_id = "com.icbc.emallmobile:id/text_sku_gotobuy"
popup_buy = wait.until(EC.presence_of_element_located((By.ID, popup_buy_id)))
popup_buy.click()


# 提交订单 H5
print(driver.contexts)
for i in driver.contexts:
    if i == 'WEBVIEW_com.vphone.launcher':
        while True:
            try:
                driver.switch_to.context(i)
                now = driver.current_context
                print('进入', now)
                break
            except Exception as e:
                print(e)
                continue
        break
    else:
        continue

submit_id = "submit"
submit = wait.until(EC.presence_of_element_located((By.ID, submit_id)))
submit.click()

# 获取当前页面HTML代码
# html = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
# print(html)
