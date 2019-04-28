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
            'platformName': 'Android',
            'deviceName': 'OS105',
            'appPackage': 'com.tencent.mm',
            'appActivity': '.ui.LauncherUI'
        }
        self.driver_server = 'http://127.0.0.1:4723/wd/hub'
        print('微信启动...')
        # 启动微信
        self.driver = webdriver.Remote(self.driver_server, self.desired_caps)
        # 设置等待
        self.wait = WebDriverWait(self.driver, 300)

    def login(self):
        """登录模块"""
        print("-----点击登录-----")
        # time.sleep(1)
        login = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/e4g')))
        login.click()

        # 输入手机号
        print("-----账号输入-----")
        phone = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/kh')))
        phone.click()
        phone_num = input('请输入手机号：')
        phone.send_keys(phone_num)

        # 点击下一步
        print("-----点击下一步-----")
        button = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/axt')))
        button.click()

        # 输入密码
        print("-----密码输入-----")
        time.sleep(1)
        pass_w = input('请输入密码：')
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/kh')))

        password.send_keys(pass_w)

        # 点击登录
        print("-----登录中-----")
        login = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/axt')))
        login.click()

        # 通讯录提示
        print("-----关闭通讯录弹窗-----")
        time.sleep(5)  # 视网络情况调整延迟时间 预防加载过慢报错
        tip = self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.tencent.mm:id/az9')))
        tip.click()

    def craw_friend(self):
        """获取好友朋友圈"""
        print("-----点击发现-----")
        tab = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@resource-id="com.tencent.mm:id/bq"]/android.widget.LinearLayout/android.widget.RelativeLayout[3]')))
        print('已经找到发现按钮')
        time.sleep(1)
        tab.click()

        print('-----点击朋友圈-----')
        friends = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@ resource-id="android:id/list"]/android.widget.LinearLayout[1]')))
        friends.click()
        time.sleep(3)

        # while True:
        #     items = self.wait.until(EC.presence_of_all_elements_located(
        #         (By.XPATH, '//*[@resource-id="com.tencent.mm:id/dja"]//*[@class="android.widget.FrameLayout"]')))
        #     self.driver.swipe(300, 1000, 300, 300)
        #     for item in items:
        #         try:
        #             nickname = item.find_element_by_id('com.tencent.mm:id/as6').get_attribute('text')
        #             print(nickname)
        #             content = item.find_element_by_id('com.tencent.mm:id/dkf').get_attribute('text')
        #             print(content)
        #             data = {'nickname': nickname,
        #                     'content': content}
        #             self.collection.update({'nickname': nickname, 'content': content}, {'$set': data}, True)
        #
        #         except:
        #             pass


if __name__ == '__main__':
    wechat = WeChatSpider()
    wechat.login()
    wechat.craw_friend()
