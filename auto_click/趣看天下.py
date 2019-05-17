# -*- coding: utf-8 -*-
# @Time    : 2019/5/17 13:38
# @Author  : project
# @File    : 趣看天下.py
# @Software: PyCharm
import time
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from appium.webdriver.connectiontype import ConnectionType
from selenium.webdriver.support import expected_conditions as EC
"""新闻自动点击"""


class News:
    def __init__(self):
        self.desired_caps = {
            "platformName": "Android",
            "deviceName": "OS105",
            "appPackage": "com.yanhui.qktx",
            "appActivity": ".activity.MainActivity",
            "noReset": True
        }
        self.driver_server = 'http://127.0.0.1:4723/wd/hub'
        print('APP启动...')
        # 启动APP
        self.driver = webdriver.Remote(self.driver_server, self.desired_caps)
        # 设置等待
        self.wait = WebDriverWait(self.driver, 30, 1)

    def loop_look(self):

        print("切换到热点栏目")
        self.driver.swipe(800, 500, 300, 500, 500)
        while True:
            print("读取内容中------")
            news = self.wait.until(EC.presence_of_all_elements_located(
                (By.ID, 'com.yanhui.qktx:id/tv_title')))
            print("读取到内容")
            for new in news:
                time.sleep(1)
                new.click()
                content = self.wait.until(EC.presence_of_element_located((By.ID, 'com.yanhui.qktx:id/web_frame')))
                if content.is_displayed():
                    count = 0
                    while True:
                        fang = True
                        time.sleep(2)
                        self.driver.swipe(500, 1200, 500, 1000, 1000)
                        time.sleep(2)
                        count += 1
                        if count == 20:
                            fang = False
                        if fang is False:
                            self.driver.keyevent(4)
                            break

            print("当前屏幕读取完成")
            print("*" * 50)
            self.driver.swipe(500, 1800, 500, 400, 1000)


if __name__ == '__main__':
    loop = News()
    loop.loop_look()