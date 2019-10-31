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
            "deviceName": "OS105",
            "appPackage": "com.tencent.mm",
            "appActivity": ".ui.LauncherUI",
            'noReset': True  # 获取登录状态
        }
        self.driver_server = 'http://127.0.0.1:4723/wd/hub'
        print('**********程序启动中**********')
        # 启动微信
        self.driver = webdriver.Remote(self.driver_server, self.desired_caps)
        # 设置隐形等待时间
        self.wait = WebDriverWait(self.driver, 10, 1, AttributeError)