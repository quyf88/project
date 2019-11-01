# -*- coding:utf-8 -*-
# 文件 ：123.py
# IED ：PyCharm
# 时间 ：2019/10/31 0031 13:25
# 版本 ：V1.0
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support import expected_conditions as EC
"""
Appium adb 获取真实appActivity
https://blog.csdn.net/qq_38154948/article/details/90408056
"""


class Spider:
    def __init__(self):
        self.desired_caps = {
            "platformName": "Android",
            "deviceName": "127.0.0.1:62001",
            "appPackage": "com.ss.android.ugc.aweme",
            "appActivity": ".splash.SplashActivity",
            'noReset': True  # 获取登录状态
        }
        self.driver_server = 'http://127.0.0.1:4723/wd/hub'
        print('**********程序启动中**********')
        # 启动微信
        self.driver = webdriver.Remote(self.driver_server, self.desired_caps)
        # 设置隐形等待时间
        self.wait = WebDriverWait(self.driver, 300, 1, AttributeError)
        # 获取手机尺寸
        self.driver.get_window_size()
        self.x = self.driver.get_window_size()['width']  # 宽
        self.y = self.driver.get_window_size()['height']  # 长
        print(self.x, self.y)

    def slide(self):
        """
        滑动
        :return:
        """
        while True:
            print('定位评论按钮')
            comment = self.wait.until(EC.presence_of_element_located((By.ID, 'com.ss.android.ugc.aweme:id/yk')))
            comment.click()
            print('点击评论按钮')
            if not self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.ss.android.ugc.aweme:id/a1v'))):
                self.driver.keyevent(4)
                continue

            titles = self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.ss.android.ugc.aweme:id/title')))
            title = titles[1]
            print(title.text)
            while 3:
                self.driver.swipe(200, 1700, 200, 1000, 1000)


if __name__ == '__main__':
    spider = Spider()
    spider.slide()