# coding=utf-8
# 作者    ： Administrator
# 文件    ：Login.py
# IED    ：PyCharm
# 创建时间 ：2019/6/19 0:07
import os
import re
import time
import logging
import configparser
from appium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import send_sms
import adb_server
from 飞常达数据采集.MD5.MD5_Dao import Md5Dao

# 手动启动模拟器 adb connect 127.0.0.1:62001
# 查看连接 adb devices


def run_time(func):
    def new_func(*args, **kwargs):
        start_time = datetime.now()
        print("程序开始时间：{}".format(start_time))
        func(*args, **kwargs)
        end_time = datetime.now()
        print("程序结束时间：{}".format(end_time))
        print("程序执行用时：{}s".format((end_time - start_time)))

    return new_func


class Spider:
    def __init__(self):
        self.log = self.log_init()
        # 是否启用短信通知
        self.sms = None
        # 短信通知号码
        self.phone = None
        # 关注机场数量
        self.ports_num = None
        # 统计已查看机场列表
        self.airport_names = []
        self.desired_caps = {
            "platformName": "Android",
            "deviceName": "OS105",
            "appPackage": "com.feeyo.vz.pro.cdm",
            "appActivity": "com.feeyo.vz.pro.activity.cdm.WelcomeActivity",
            "noReset": True
        }
        self.driver_server = 'http://127.0.0.1:4723/wd/hub'
        self.log.info('机场航班信息实时监测系统启动中...')
        # 读取设备信息
        self.adb_serve()
        # 启动APP
        self.driver = webdriver.Remote(self.driver_server, self.desired_caps)
        # 设置等待
        self.wait = WebDriverWait(self.driver, 40, 0.5)

    def conf(self):
        """读取配置文件"""
        cf = configparser.ConfigParser()
        path = os.path.abspath('.') + '\config\config.ini'
        cf.read(path, encoding='utf-8')
        sms = cf.get('brower', 'sms')
        self.sms = eval(sms)
        phone = cf.get('brower', 'phone')
        self.phone = str(phone).split(',')
        print('<font color="green">配置文件读取成功!通知号码：[{}]</font>'.format(phone))

    def log_init(self):
        """日志模块"""
        path = os.path.abspath('.') + r'\log\run.log'
        formatter = logging.Formatter('%(asctime)s | %(name)-6s | %(levelname)-6s| %(message)s')
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        fh = logging.FileHandler(path, encoding='utf-8', mode='w+')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        console.setFormatter(formatter)
        # 如果需要同時需要在終端上輸出，定義一個streamHandler
        # print_handler = logging.StreamHandler()  # 往屏幕上输出
        # print_handler.setFormatter(formatter)  # 设置屏幕上显示的格式
        logger = logging.getLogger("Spider")
        # logger.addHandler(print_handler)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(console)
        logger.addHandler(fh)
        return logger

    def adb_serve(self):
        """读取设备信息"""
        adb = adb_server.run()
        if not adb:
            self.log.error('<font color="red">{}</font>'.format('请检查设备是否打开'))
            return
        print('<font color="green">设备：[{}]正常运行中</font>'.format(adb))

    def login(self):
        """账号登录"""
        self.log.info("监测账号是否登录...")
        while True:
            try:
                dialog = self.driver.find_element_by_id('com.feeyo.vz.pro.cdm:id/radio_chat')
                dialog.click()
                break
            except Exception as e:
                self.driver.keyevent(4)
                print(e)
        try:
            login = self.driver.find_element_by_id('com.feeyo.vz.pro.cdm:id/guide_btn_login')
            self.log.info("账号未登录...请登录账号")
            login.click()
            self.log.info("账号登录中...")
            username = self.wait.until(EC.presence_of_element_located((By.ID, 'com.feeyo.vz.pro.cdm:id/login_edt_phone_number')))
            username.click()
            username.send_keys('18672366488')
            password = self.wait.until(EC.presence_of_element_located((By.ID, 'com.feeyo.vz.pro.cdm:id/login_edt_user_password')))
            password.click()
            password.send_keys('18672366488')
            login_end = self.wait.until(EC.presence_of_element_located((By.ID, 'com.feeyo.vz.pro.cdm:id/login_btn_login')))
            login_end.click()
            self.log.info("账号登录成功!")

        except Exception as e:
            self.log.info("账号已登录!")

    def loop_look(self):
        """进入关注机场页面"""
        airport_page = self.wait.until(EC.presence_of_element_located((By.ID, 'com.feeyo.vz.pro.cdm:id/radio_airport')))
        airport_page.click()
        self.log.info("开始监控关注机场")
        # time.sleep(2)
        # self.log.info("等待2秒刷新页面，防止频繁访问页面加载问题")
        # 关注机场数量
        airports_num = self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.feeyo.vz.pro.cdm:id/tab_layout_display_txt_count')))
        ports_num = airports_num[0].text
        self.ports_num = int(re.findall(r'\d.*', ports_num)[0])
        self.log.info("监控机场数量：{}".format(ports_num))

    def run(self):

        while True:
            # 关注机场列表
            if len(self.airport_names) >= self.ports_num:
                self.driver.swipe(500, 500, 500, 1800, 500)
                time.sleep(0.5)
                self.driver.swipe(500, 500, 500, 1800, 500)
                time.sleep(0.5)
                self.driver.swipe(500, 500, 500, 1800, 500)
                self.airport_names = []
            try:
                # 机场名
                airports_name = self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.feeyo.vz.pro.cdm:id/airport_dynamic_new_txt_state')))
                for airport_name in airports_name:
                    airport_name_text = airport_name.text.split('-')[0]
                    # 判断当前当前机场是否有机场名
                    if not airport_name_text:
                        self.airport_names.append('无机场名称')
                        # self.log.info('<font color="green">空机场名跳过</font>')
                        continue
                    # 效验是否已处理
                    if airport_name_text in self.airport_names:
                        continue
                    print("[{}]：机场航班信息获取中...".format(airport_name_text))
                    self.airport_names.append(airport_name_text)
                    airport_name.click()

                    # 出场延误航班数量
                    mora_num = self.wait.until(EC.presence_of_element_located((By.ID, 'com.feeyo.vz.pro.cdm:id/detail_flow_delay_text')))
                    num = re.findall(r'\d', mora_num.text)
                    if not int(num[0]):
                        print("[{}]机场暂无延误航班,出场延误航班数：{}".format(airport_name_text, num[0]))
                        self.driver.keyevent(4)  # 返回上一页
                        continue

                    # 进入机场航班信息页面
                    flight_page = self.wait.until(EC.presence_of_element_located((By.ID, 'com.feeyo.vz.pro.cdm:id/vznairport_detail_diaplay')))
                    flight_page.click()

                    flight_out = self.wait.until(EC.presence_of_element_located((By.ID, 'com.feeyo.vz.pro.cdm:id/airport_display_img_port')))
                    flight_out.click()
                    # 延误航班页面
                    mora_page = self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.feeyo.vz.pro.cdm:id/tab_layout_display_txt_count')))
                    mora_page[2].click()
                    # 判断当前机场是否有延误航班
                    time.sleep(1)
                    if not int(mora_page[2].text):
                        self.driver.keyevent(4)  # 返回当前机场详情页面
                        time.sleep(1)
                        self.driver.keyevent(4)  # 返回机场列表页面
                        continue

                    # 航班号
                    flight_id = self.wait.until(EC.presence_of_all_elements_located(
                        (By.ID, 'com.feeyo.vz.pro.cdm:id/item_display_list_txt_airport_route')))

                    print("[{}]机场出场延误航班数：{}".format(airport_name_text, len(flight_id)))
                    count = 0
                    for flight in flight_id:
                        try:
                            # 延误时间
                            mora_time = self.wait.until(EC.presence_of_all_elements_located(
                                (By.ID, 'com.feeyo.vz.pro.cdm:id/item_display_list_txt_delay_time_plus')))
                            mora_time_text = mora_time[count].text
                        except:
                            self.driver.keyevent(4)  # 返回当前机场详情页面
                            time.sleep(1)
                            self.driver.keyevent(4)  # 返回机场列表页面
                            break

                        count += 1
                        self.log.info('机场[{}]航班号[{}]延误时间[{}]'.format(airport_name_text, flight.text, mora_time_text))
                        if not mora_time_text:
                            continue
                        if int(mora_time_text) < 180 or int(mora_time_text) > 800:
                            continue
                        else:
                            # 进入航班详情页面
                            flight.click()
                            # 获取延误航班详细信息
                            self.get_flight_content(mora_time_text, airport_name_text)
                            self.driver.keyevent(4)  # 返回延误航班页面
                            time.sleep(1)

                    self.driver.keyevent(4)  # 返回当前机场详情页面
                    time.sleep(1)
                    self.driver.keyevent(4)  # 返回机场列表页面

                try:
                    # 上滑一屏
                    self.driver.swipe(500, 1400, 500, 600, 800)
                    print(self.airport_names, self.ports_num)
                    time.sleep(1)
                except Exception as e:
                    print(e)
            except Exception as e:
                self.log.error(e)
                # self.log.exception(e)
                break

    def get_flight_content(self, mora_time_text, airport_name_text):
        """获取延误航班详细信息"""
        # 航班号
        flight_number = self.wait.until(
            EC.presence_of_all_elements_located((By.ID, 'com.feeyo.vz.pro.cdm:id/tab_layout_txt_title')))
        flight_number_text = flight_number[0].text
        # 出发地
        departure = self.wait.until(
            EC.presence_of_element_located((By.ID, 'com.feeyo.vz.pro.cdm:id/item_start_airport_name')))
        departure_text = departure.text
        # 计划起飞时间
        planning_time = self.wait.until(
            EC.presence_of_element_located((By.ID, 'com.feeyo.vz.pro.cdm:id/item_start_plan_fly_time')))
        planning_time_text = planning_time.text
        # 实际起飞时间
        departure_time = self.wait.until(
            EC.presence_of_element_located((By.ID, 'com.feeyo.vz.pro.cdm:id/item_start_fly_time')))
        departure_time_text = departure_time.text
        # 目的地
        destination = self.wait.until(
            EC.presence_of_element_located((By.ID, 'com.feeyo.vz.pro.cdm:id/item_end_airport_name')))
        destination_text = destination.text
        # 计划到达时间
        planned_time = self.wait.until(
            EC.presence_of_element_located((By.ID, 'com.feeyo.vz.pro.cdm:id/item_end_plan_fly_time')))
        planned_time_text = planned_time.text
        # 预计达到时间
        estimated_time = self.wait.until(
            EC.presence_of_element_located((By.ID, 'com.feeyo.vz.pro.cdm:id/item_end_fly_time')))
        estimated_time_text = estimated_time.text

        # self.log.info("航班：[{}],[{}],实际起飞时间：[{}],出发地：[{}],目的地：[{}],{} 预计到达：[{}],延误时间：[{}]".format(flight_number_text,
        #                                                                                          planning_time_text,
        #                                                                                          departure_time_text,
        #                                                                                          departure_text,
        #                                                                                          destination_text,
        #                                                                                          planned_time_text,
        #                                                                                          estimated_time_text,
        #                                                                                          mora_time_text))
        content = "[{}]机场,[{}]航班,[{}]出发,目的地[{}],延误时间[{}]".format(airport_name_text, flight_number_text,
                                                                 departure_text, destination_text, mora_time_text)
        self.log.info('<font color="green">content:{}</font>'.format(content))
        # 短信发送
        if self.sms:
            self.sms_MD5(content, flight_number_text)

    def sms_MD5(self, content, flight_number):
        """"效验当日已发送短信航班信息"""
        # 实例化
        # md5 = Md5Dao()
        # 短信发送日志信息
        path = os.path.abspath('.') + '\log\send_sms.txt'
        with open(path, 'a+', encoding='utf-8')as f:
            f.seek(0)
            a = [i.replace('\n', '') for i in f.readlines()]
            if flight_number not in a:
                f.write(flight_number + '\n')
                self.sms_post(content)
        # 效验是否发送 False 已发送 True 未发送
        # res = md5.dateupdate(path)
        # return res

    def sms_post(self, content):
        """短信发送"""
        for i in self.phone:
            print("<font color='green'>短信发送成功：{}</font>".format(content))
            # send_sms.send_sms(i, content)

    @run_time
    def main(self):
        self.conf()  # 读取配置文件
        self.login()  # 登录
        self.loop_look()  # 进入关注航班
        self.run()  # 主程序


if __name__ == '__main__':
    loop = Spider()
    loop.main()

