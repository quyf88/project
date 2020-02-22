# -*- coding:utf-8 -*-
# 文件 ：spider.py
# IED ：PyCharm
# 时间 ：2019/10/31 0031 13:25
# 版本 ：V1.3
# 抖音版本 ：9.9.0
import os
import time
import datetime
import requests
import threading
import subprocess
import urllib.request
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
        print('**********程序启动中**********')
        # 启动微信
        self.driver = None
        # 设置隐形等待时间
        self.wait = None
        # 获取手机尺寸
        # self.driver.get_window_size()
        # self.x = self.driver.get_window_size()['width']  # 宽
        # self.y = self.driver.get_window_size()['height']  # 长
        # print(self.x, self.y)
        self.one = 'com.ss.android.ugc.aweme:id/a6f'  # 评论数量ID
        self.two = 'com.ss.android.ugc.aweme:id/dj0'  # 评论数据模块ID

    def slide(self):
        """
        滑动
        :return:
        """
        while True:           
            print('定位评论按钮')            
            comment = self.wait.until(EC.presence_of_element_located((By.ID, self.one)))
            comment_num = comment.text
            if '评论' in comment_num:
                # 下一个视频
                self.driver.swipe(200, 1700, 200, 500, 500)
                time.sleep(2)
                continue
            print(f'评论数量：{comment_num}')
            comment_num = int(float(comment_num.replace('w', ''))) * 3000 if 'w' in comment_num else int(
                int(comment_num) / 8)
            # 跳过小于100评论的视频
            if int(comment_num) < 80:
                self.driver.swipe(200, 1500, 200, 500, 300)
                time.sleep(2)
                continue
            comment.click()
            print('刷新评论数据')
            time.sleep(2)
            # 判断数据是否刷新出来
            while True:
                cou = 1
                if not self.driver.find_elements_by_id(self.two):
                    print('刷新评论失败重试！')
                    self.driver.keyevent(4)
                    time.sleep(1.5)
                    self.driver.keyevent(4)
                    time.sleep(1.5)
                    # 同一个视频重试三次失败主动抛出异常重启程序
                    if cou > 2:
                        print('评论数据刷新失败重启!')
                        raise print('主动抛出异常重启!')
                    comment.click()
                    cou += 1
                    continue

                num = 200 if comment_num > 200 else 100
                for i in range(comment_num):
                    # 判断是否到达底部
                    if not (i + 1) % num:
                        # print('判断是否到达底部')
                        time.sleep(2)
                        if self.driver.find_elements_by_xpath(
                                f'//android.support.v7.widget.RecyclerView [@resource-id={self.two}]/android.widget.FrameLayout/android.widget.TextView'):
                            print('到达底部,切换下一个视频')
                            break
                    # 下拉刷新十次后 上刷一次 防止加载不出来
                    if not (i + 1) % 30:
                        self.driver.swipe(200, 1400, 200, 1600, 500)
                        time.sleep(0.5)
                        continue
                   
                    # 根据时间选择退出刷新当前视频
                    # new_time = (datetime.datetime.now()+datetime.timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')
                    # print(new_time)
                    # start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    # print(start_time)
                    # if new_time < start_time:
                    #     print('超时退出')
                    #     break
                    self.driver.swipe(200, 1700, 200, 800, 400)
                    
                # 下一个视频
                self.driver.keyevent(4)
                time.sleep(2)
                self.driver.swipe(200, 1700, 200, 500, 500)
                print('*' * 25)
                break


def proxy():
    url = 'http://www.dongdongmeiche.cn/proxy/ba618b3e3adc4e7c93127546d58502a5'
    opener = urllib.request.build_opener()
    try:
        opener.open(url)
        fang = True
    except urllib.error.HTTPError:
        fang = False
    except urllib.error.URLError:
        fang = False
    if not fang:
        print('url validation failed!')
        os._exit(0)
    response = requests.get(url)
    content = response.json()
    code = content['errorcode']
    if code != 10001:
        print(content['context'])
        os._exit(0)
    print(content['context'])


def adb_devices():
    """读取设备列表"""   
    get_cmd = "adb devices"  # 查询连接设备列表
    count = 0
    try:
        while True:
            # 连接设备
            if count > 2:
                print("读取设备信息失败,请检查设备是否成功启动")
                break
            # 读取连接设备信息
            p = subprocess.Popen(get_cmd, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 stdin=subprocess.PIPE, shell=True)

            (output, err) = p.communicate()
            # 分割多条信息为列表
            output = output.decode().replace('\r', '').split('\n')
            # 剔除列表中空字符串
            output = list(filter(None, output))            
            print(output)            
            if len(output) < 5:
                print("读取设备信息失败,自动重启中...")
                count += 1
                os.popen('adb connect 127.0.0.1:21503')
                time.sleep(1)
                os.popen('adb connect 127.0.0.1:21513')
                time.sleep(1)
                os.popen('adb connect 127.0.0.1:21523')
                time.sleep(1)               
                os.popen('adb connect 127.0.0.1:21533')            
                time.sleep(1)
                continue
            # 连接设备列表
            devices = [i.split('\t') for i in output[1:]]
            # 读取成功列表
            success = [i[0] for i in devices if i[1] == 'device']
            for i in success:
                print("设备连接成功：[{}]".format(i))
            return success
    except:
        print('读取设备信息失败,请检查设备是否成功启动!')
        os.popen('adb connect 127.0.0.1:21503')
        time.sleep(1)
        os.popen('adb connect 127.0.0.1:21513')
        time.sleep(1)
        os.popen('adb connect 127.0.0.1:21523')     
        time.sleep(1)    
        os.popen('adb connect 127.0.0.1:21533')      
        time.sleep(1)


@run_time
def main(udid, port):
    while True:
        try:
            spider = Spider()
            print(f'**********程序[{udid}]启动中**********')
            desired_caps = {
                "automationName": "Uiautomator1",  # 引擎错误时添加此项 uiautomator2ServerLaunchTimeout'
                "platformName": "Android",
                "deviceName": udid,
                "adbExecTimeout": "100000",  # adb指令超时时间，默认是20000毫秒
                "appPackage": "com.ss.android.ugc.aweme",
                "appActivity": ".splash.SplashActivity",
                "udid": udid,  # 根据模拟器名称启动
                "noReset": True  # 默认保留登录状态
            }
            driver_server = 'http://127.0.0.1:{}/wd/hub'.format(port)
            # 启动APP
            spider.driver = webdriver.Remote(driver_server, desired_caps)
            # 设置等待
            spider.wait = WebDriverWait(spider.driver, 100, 1)
            spider.slide()
        except Exception as e:
            continue


if __name__ == '__main__':
    proxy()
    success = adb_devices()
    port = 4723
    for i in success:
        s = threading.Thread(target=main, args=(i, port))
        port += 2
        s.start()                
        time.sleep(20)


