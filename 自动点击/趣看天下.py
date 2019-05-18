# -*- coding: utf-8 -*-
# @Time    : 2019/5/17 13:38
# @Author  : project
# @File    : 趣看天下.py
# @Software: PyCharm
import time
from datetime import datetime
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from appium.webdriver.connectiontype import ConnectionType
from selenium.webdriver.support import expected_conditions as EC
"""新闻自动点击刷金币"""


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
        self.wait = WebDriverWait(self.driver, 60, 1)

    def run_time(self, func):
        def new_func(*args, **kwargs):
            start_time = datetime.now()
            print("程序开始时间：{}".format(start_time))
            func(*args, **kwargs)
            end_time = datetime.now()
            print("程序结束时间：{}".format(end_time))
            print("程序执行用时：{}s".format((end_time - start_time)))

        return new_func

    @run_time
    def loop_look(self):

        try:
            print("切换到热点栏目")
            self.driver.swipe(800, 500, 300, 500, 500)
            while True:
                print("————————刷新页面中————————")
                news = self.wait.until(EC.presence_of_all_elements_located(
                    (By.ID, 'com.yanhui.qktx:id/tv_title')))
                len_news = 1
                print("获取到：{}条新闻".format(len(news)))
                for new in news:
                    time.sleep(1)
                    print("读取第：{}条新闻中...".format(len_news))
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
                        print("第：{}条新闻读取完毕...".format(len_news))
                    else:
                        continue
                    len_news += 1

                print("当前屏幕读取完成,刷新下一屏")
                print("*" * 50)
                self.driver.swipe(500, 1800, 500, 600, 800)
        except:
            print("退出时间：{}".format(datetime.now()))


if __name__ == '__main__':
    loop = News()
    loop.loop_look()


