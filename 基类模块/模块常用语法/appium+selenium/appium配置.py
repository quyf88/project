from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class WeChatSpider:
    def __init__(self):
        self.desired_caps = {
            "platformName": "Android",
            "deviceName": "127.0.0.1:62001",
            "appPackage": "com.tencent.mm",
            "appActivity": ".ui.LauncherUI",
            'noReset': True  # 获取登录状态
        }
        self.driver_server = 'http://127.0.0.1:4723/wd/hub'
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


"""
adb connect 127.0.0.1:62001  # 连接设备
adb devices  # 查看连接设备    
adb shell /system/bin/screencap -p /sdcard/screenshot.png  # 截图命令
adb pull /sdcard/screenshot.png D:\download  # 保存
adb shell input tap x y  # 点击
adb shell input swipe x1 y1 x2 y2  # 翻页
"""