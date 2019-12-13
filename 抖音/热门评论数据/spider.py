# -*- coding:utf-8 -*-
# 文件 ：spider.py
# IED ：PyCharm
# 时间 ：2019/10/31 0031 13:25
# 版本 ：V1.3
# 抖音版本 ：8.8.0
import os
import time
import subprocess
import datetime
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
"""
Appium adb 获取真实appActivity
https://blog.csdn.net/qq_38154948/article/details/90408056
"""


def run_time(func):
    def new_func(*args, **kwargs):
        start_time = datetime.datetime.now()
        print("程序开始时间：{}".format(start_time))
        func(*args, **kwargs)
        end_time = datetime.datetime.now()
        print("程序结束时间：{}".format(end_time))
        print("程序执行用时：{}s".format((end_time - start_time)))

    return new_func


class Spider:
    def __init__(self):
        self.desired_caps = {
              "platformName": "Android",
              "deviceName": "127.0.0.1:62001",
              "appPackage": "com.ss.android.ugc.aweme",
              "appActivity": ".splash.SplashActivity",
              "noReset": "True"
            }
        self.driver_server = 'http://127.0.0.1:4723/wd/hub'
        print('**********程序启动中**********')
        # 启动微信
        self.driver = webdriver.Remote(self.driver_server, self.desired_caps)
        # 设置隐形等待时间
        self.wait = WebDriverWait(self.driver, 100, 1, AttributeError)
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
            # 8.6.0
            # comment = self.wait.until(EC.presence_of_element_located((By.ID, 'com.ss.android.ugc.aweme:id/yj')))
            # 8.7.0
            # comment = self.wait.until(EC.presence_of_element_located((By.ID, 'com.ss.android.ugc.aweme:id/zb')))
            # 8.8.0
            # comment = self.wait.until(EC.presence_of_element_located((By.ID, 'com.ss.android.ugc.aweme:id/zf')))
            # 9.0.0
            # comment = self.wait.until(EC.presence_of_element_located((By.ID, 'com.ss.android.ugc.aweme:id/zt')))
            # 9.1.0
            # comment = self.wait.until(EC.presence_of_element_located((By.ID, 'com.ss.android.ugc.aweme:id/a19')))
            # 9.2.0
            comment = self.wait.until(EC.presence_of_element_located((By.ID, 'com.ss.android.ugc.aweme:id/a3u')))
            comment_num = comment.text
            print(f'评论数量：{comment_num}')
            comment_num = int(float(comment_num.replace('w', ''))) * 1000 if 'w' in comment_num else int(
                int(comment_num) / 10)
            if int(comment_num) < 100:
                self.driver.swipe(200, 1500, 200, 500, 500)
                continue
            comment.click()
            print('刷新评论数据')
            # 判断数据是否刷新出来
            # 8.6.0
            # if not self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.ss.android.ugc.aweme:id/a22'))):
            # 8.7.0
            # if not self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.ss.android.ugc.aweme:id/a2v'))):
            # 8.8.0
            # if not self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.ss.android.ugc.aweme:id/a32'))):
            # 9.0.0
            # if not self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.ss.android.ugc.aweme:id/a3k'))):
            # 9.1.0
            # if not self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.ss.android.ugc.aweme:id/a53'))):
            # 9.2.0
            if not self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.ss.android.ugc.aweme:id/a7k'))):
                self.driver.keyevent(4)
                continue
            new_time = (datetime.datetime.now()+datetime.timedelta(minutes=20)).strftime('%Y-%m-%d %H:%M:%S')
            # print(new_time)
            for i in range(comment_num):
                if (i + 1) % 10 == 0:
                    self.driver.swipe(200, 1200, 200, 1400, 200)
                    time.sleep(0.5)
                    continue
                start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # print(start_time)
                if new_time < start_time:
                    print('超时退出')
                    break
                self.driver.swipe(200, 1700, 200, 500, 100)
            # 下一个视频
            self.driver.keyevent(4)
            time.sleep(2)
            self.driver.swipe(200, 1700, 200, 500, 500)
            print('*' * 25)


def proxy():
    tss1 = '2019-12-4 00:00:00'
    timeArray = time.strptime(tss1, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    now_time = int(round(time.time()))
    if now_time < timeStamp:
        print('代理到期请及时续费')
        os._exit(0)
    print('代理效验成功!')


# def adb_devices():
#     """读取设备列表"""
#     get_cmd = "adb devices"  # 查询连接设备列表
#     count = 0
#     try:
#         while True:
#             # 连接设备
#             if count > 2:
#                 print("读取设备信息失败,请检查设备是否成功启动")
#                 break
#             # 读取连接设备信息
#             p = subprocess.Popen(get_cmd, stdout=subprocess.PIPE,
#                                  stderr=subprocess.PIPE,
#                                  stdin=subprocess.PIPE, shell=True)
#
#             (output, err) = p.communicate()
#             # 分割多条信息为列表
#             output = output.decode().replace('\r', '').split('\n')
#             # 剔除列表中空字符串
#             output = list(filter(None, output))
#             if not len(output) > 1:
#                 print("读取设备信息失败,自动重启中...")
#                 count += 1
#                 os.popen('adb connect 127.0.0.1:62001')
#                 continue
#             # 连接设备列表
#             devices = [i.split('\t') for i in output[1:]]
#             # 读取成功列表
#             success = [i[0] for i in devices if i[1] == 'device']
#             for i in success:
#                 print("设备连接成功：[{}]".format(i))
#             return success
#     except:
#         print('读取设备信息失败,请检查设备是否成功启动!')
#         os.popen('adb connect 127.0.0.1:62001')


@run_time
def main():
    while True:
        try:
            proxy()
            # adb_devices()
            spider = Spider()
            spider.slide()
        except:
            continue


if __name__ == '__main__':
    main()
