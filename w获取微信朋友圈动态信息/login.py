# coding=utf-8
# 作者    ： Administrator
# 文件    ：1.py
# IED    ：PyCharm
# 创建时间 ：2019/4/25 20:24

# This sample code uses the Appium python client
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import time

caps = {}
caps["platformName"] = "Android"
caps["deviceName"] = "OS105"
caps["appPackage"] = "com.tencent.mm"
caps["appActivity"] = ".ui.LauncherUI"

driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)

print("-----点击登录-----")
time.sleep(1)
el1 = driver.find_element_by_id("com.tencent.mm:id/e4g")
el1.click()

print("-----账号输入-----")
el2 = driver.find_element_by_id("com.tencent.mm:id/kh")
el2.click()
time.sleep(1)
phone_num = input('请输入手机号：')
el2.send_keys(phone_num)

print("-----下一步-----")
time.sleep(1)
el3 = driver.find_element_by_id("com.tencent.mm:id/axt")
el3.click()

print("-----密码输入-----")
time.sleep(3)
el4 = driver.find_element_by_id("com.tencent.mm:id/kh")
pass_word = input("输入密码：")
el4.send_keys(pass_word)

print("-----登录-----")
time.sleep(1)
el5 = driver.find_element_by_id("com.tencent.mm:id/axt")
el5.click()

print("-----关闭弹窗-----")
time.sleep(10)
el6 = driver.find_element_by_id("com.tencent.mm:id/az9")
el6.click()

print("-----点击发现-----")
time.sleep(10)
el7 = driver.find_element_by_xpath("//android.widget.FrameLayout[@content-desc=\"当前所在页面,与的聊天\"]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout[3]/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.ImageView[1]")
el7.click()

print("-----点击朋友圈-----")
time.sleep(5)
el8 = driver.find_element_by_id("com.tencent.mm:id/aki")
el8.click()

print("-----刷新朋友圈-----")
time.sleep(5)
TouchAction(driver).press(x=728, y=1131).move_to(x=718, y=1620).release().perform()

# driver.quit()
