# -*- coding: utf-8 -*-
# @Time    : 2019/4/28 13:48
# @Author  : project
# @File    : wechat_spider.py
# @Software: PyCharm


from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time


class WeChatSpider:
    def __init__(self):
        self.desired_caps = {
            "platformName": "Android",
            "deviceName": "OS105",
            "appPackage": "com.tencent.mm",
            "appActivity": ".ui.LauncherUI",
            'noReset': True  # 获取登录状态
        }
        self.driver_server = 'http://127.0.0.1:4723/wd/hub'
        print('微信启动...')
        # 启动微信
        self.driver = webdriver.Remote(self.driver_server, self.desired_caps)
        # 设置等待
        self.wait = WebDriverWait(self.driver, 30, 1, AttributeError)
        self.diction = dict()

    def login(self):
        """登录模块"""

        print("-----点击登录-----")
        login = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/e4g')))
        login.click()

        # 输入手机号
        print("-----账号输入-----")
        phone = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/kh')))
        phone.click()
        phone_num = ""
        # phone_num = input('请输入账号：')
        # phone.send_keys(phone_num)
        phone.send_keys(phone_num)

        # 点击下一步
        print("-----点击下一步-----")
        button = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/axt')))
        button.click()

        # 输入密码
        print("-----密码输入-----")
        # pass_w = input('请输入密码：')
        pass_w = ""
        # presence_of_element_located 元素加载出，传入定位元组，如(By.ID, 'p')
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/kh')))
        password.send_keys(pass_w)

        # 点击登录
        print("-----登录中-----")
        login = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/axt')))
        login.click()

        print("-----关闭通讯录弹窗-----")
        # WebDriverWait 10秒内每隔2秒运行一次直到找到元素 规定时间内找不到则报错 element_to_be_clickable 元素可点击
        tip = WebDriverWait(self.driver, 10, 2).until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/az9')))
        tip.click()

    def craw_friend(self):
        """获取好友朋友圈"""
        while True:
            print("-----点击发现-----")
            tab = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@resource-id="com.tencent.mm:id/bq"]/android.widget.LinearLayout/android.widget.RelativeLayout[3]')))
            print('已经找到发现按钮')
            tab.click()

            print('-----点击朋友圈-----')
            try:
                friends = WebDriverWait(self.driver, 5, 1).until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@resource-id="android:id/list"]/android.widget.LinearLayout[1]')))
                friends.click()
                time.sleep(1)

            except Exception:
                continue

            break
        # 开始爬取朋友圈
        temp = dict()
        count = 0
        self.driver.swipe(500, 1700, 500, 1050, 2000)  # 定位第一屏
        while True:
            flag = True
            # 定位数据
            items = self.driver.find_elements_by_id('com.tencent.mm:id/ejc')
            for item in items:
                try:
                    temp['content'] = item.get_attribute('text')
                    if temp['content'] in self.diction.values():
                        temp.clear()
                        continue
                    else:
                        self.diction['content%s' % count] = temp['content']
                        count += 1
                        temp.clear()
                except Exception as e:
                    print(e)

            self.driver.swipe(500, 1800, 500, 200, 2000)  # 向上滑动一屏

            try:
                self.driver.find_element_by_id('com.tencent.mm:id/ahy')  # 判断是否到达底部
                print('获取该用户朋友圈完毕')
                flag = False
            except Exception:
                pass

            if flag is False:
                break

    def data_save(self):
        for i in self.diction.values():
            with open("data.csv", "a+", encoding="utf-8") as f:
                f.write(i + "\n")


if __name__ == '__main__':
    wechat = WeChatSpider()
    wechat.login()
    wechat.craw_friend()
    wechat.data_save()
