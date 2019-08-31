# coding=utf-8
# 作者    ： Administrator
# 文件    ：123.py
# IED    ：PyCharm
# 创建时间 ：2019/8/31 16:34


from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class WeChatSpider:
    def __init__(self):
        self.desired_caps = {
            "platformName": "Android",
            "deviceName": "FFK0217B11002262",
            "appPackage": "com.tencent.mm",
            "appActivity": ".ui.LauncherUI",
            'noReset': True  # 获取登录状态
        }
        self.driver_server = 'http://127.0.0.1:4730/wd/hub'
        print('**********程序启动中**********')
        # 启动微信
        self.driver = webdriver.Remote(self.driver_server, self.desired_caps)
        # 设置等待
        self.wait = WebDriverWait(self.driver, 5, 1, AttributeError)
        # 获取手机尺寸
        self.driver.get_window_size()
        self.x = self.driver.get_window_size()['width']  # 宽
        self.y = self.driver.get_window_size()['height']  # 长


if __name__ == '__main__':
    WeChatSpider()