# -*- coding: UTF-8 -*-
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
from dateutil.parser import parse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import send_sms

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
        self.log.info('机场航班信息实时监测系统启动中...')
        # 启动APP
        self.driver = None
        # 设置等待
        self.wait = None

    def conf(self):
        """读取配置文件"""
        cf = configparser.ConfigParser()
        path = os.path.abspath('.') + '\config\config.ini'
        cf.read(path, encoding='utf-8')
        sms = cf.get('sms', 'sms')
        self.sms = eval(sms)
        phone = cf.get('phone', 'phone')
        self.phone = str(phone).split(',')
        print('<font color="green">配置文件读取成功!通知号码：[{}]</font>'.format(phone))

    def log_init(self):
        """日志模块"""
        path = os.path.abspath('.') + r'\log\run.log'
        formatter = logging.Formatter('%(asctime)s | %(name)-6s | %(levelname)-6s| %(message)s')
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        fh = logging.FileHandler(path, encoding='utf-8', mode='a+')
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
                time.sleep(2)
                self.driver.swipe(500, 500, 500, 1200, 500)
                time.sleep(2)
                self.driver.swipe(500, 500, 500, 1200, 500)
                time.sleep(2)
                self.driver.swipe(500, 500, 500, 1200, 500)
                self.airport_names = []
                print("防止刷新太快,刷新一遍后等待30秒再次启动")
                time.sleep(15)

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
                    mora_num = self.get_attr(airport_name, 'com.feeyo.vz.pro.cdm:id/detail_flow_delay_text')
                    if not mora_num:
                        print("[{}]机场信息获取失败".format(airport_name_text))
                        continue
                    # mora_num = WebDriverWait(self.driver, 3, 0.5).until(EC.presence_of_element_located((By.ID, 'com.feeyo.vz.pro.cdm:id/detail_flow_delay_text')))
                    num = re.findall(r'\d', mora_num.text)
                    if not int(num[0]):
                        print("[{}]机场暂无延误航班,出场延误航班数：{}".format(airport_name_text, num[0]))
                        self.driver.keyevent(4)  # 返回上一页
                        continue

                    # 进入机场航班信息页面
                    flight_page = self.wait.until(EC.presence_of_element_located((By.ID, 'com.feeyo.vz.pro.cdm:id/vznairport_detail_diaplay')))
                    flight_page.click()
                    # 出场
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

                    # 计算航班延误时间
                    self.time_calculation(airport_name_text)

                    self.driver.keyevent(4)  # 返回当前机场详情页面
                    time.sleep(1)
                    self.driver.keyevent(4)  # 返回机场列表页面
                    time.sleep(1)

                # 滑动前添加等待时间 防止滑动出错
                time.sleep(1)
                self.driver.swipe(500, 1150, 500, 500, 1000)
                print(len(self.airport_names), self.ports_num)
                time.sleep(1)

            except Exception as e:
                self.log.error(e)
                self.log.exception(e)
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

    def time_calculation(self, airport_name):
        """
        计算航班延误时间
        :param airport_name: 机场名
        :return:
        """
        # 航班号
        flight_id = self.wait.until(EC.presence_of_all_elements_located(
            (By.ID, 'com.feeyo.vz.pro.cdm:id/item_display_list_txt_airport_route')))
        flight_id = [i.text for i in flight_id]
        # 计划起飞时间
        plan_time = self.wait.until(EC.presence_of_all_elements_located(
            (By.ID, 'com.feeyo.vz.pro.cdm:id/item_display_list_txt_airport_plane_position')))
        plan_time = [i.text for i in plan_time]
        # 预计起飞时间
        estimate = self.wait.until(EC.presence_of_all_elements_located(
            (By.ID, 'com.feeyo.vz.pro.cdm:id/item_display_list_txt_delay_time')))
        estimate = [i.text for i in estimate]

        data_list = zip(flight_id, plan_time, estimate)

        print("[{}]机场出场延误航班数：{}".format(airport_name, len(flight_id)))
        count = 0
        for data in data_list:

            mora_time = int((parse(data[2]) - parse(data[1])).total_seconds()/60)

            if not mora_time > 180 or not mora_time < 800:
                if not count:
                    print('<font color="red">暂无符合条件航班</font>')
                else:
                    print("已无符合条件航班")
            else:
                content = '机场[{}]航班号[{}]延误时间[{}]'.format(airport_name, data[0], mora_time)
                self.log.info('<font color="green">content:{}</font>'.format(content))
                # 短信发送
                if self.sms:
                    self.sms_MD5(content, data[0])
                count += 1
                time.sleep(1)
                # 进入航班详情页面
                # flight.click()
                # # 获取延误航班详细信息
                # self.get_flight_content(mora_time_text, airport_name_text)

    def get_attr(self, old_page, by_id):
        """页面刷新"""
        for i in range(3):
            try:
                res = WebDriverWait(self.driver, 3, 0.5).until(EC.presence_of_element_located((By.ID, by_id)))
                return res
            except:
                print("获取不到页面信息,重新刷新页面")
                self.driver.keyevent(4)
                old_page.click()
        self.driver.keyevent(4)
        return None

    def sms_MD5(self, content, flight_number):
        """"
        效验当日已发送短信航班信息
        content  短信内容
        flight_number  航班号
        """
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
            else:
                print("航班号[{}]短信已发送".format(flight_number))
        # 效验是否发送 False 已发送 True 未发送
        # res = md5.dateupdate(path)
        # return res

    def sms_post(self, content):
        """短信发送"""
        for i in self.phone:
            print("<font color='green'>短信发送成功：{}</font>".format(content))
            # send_sms.send_sms(i, content)


@run_time
def main():
    loop = Spider()
    desired_caps = {
        "platformName": "Android",
        # "deviceName": "127.0.0.1:{}".format(62025),
        "deviceName": "OS105",
        "appPackage": "com.feeyo.vz.pro.cdm",
        "appActivity": "com.feeyo.vz.pro.activity.cdm.WelcomeActivity",
        "noReset": True
    }
    driver_server = 'http://127.0.0.1:{}/wd/hub'.format(4723)
    # 启动APP
    loop.driver = webdriver.Remote(driver_server, desired_caps)
    # 设置等待
    loop.wait = WebDriverWait(loop.driver, 40, 0.5)
    time.sleep(5)
    loop.conf()  # 读取配置文件
    # loop.login()  # 登录
    loop.loop_look()  # 进入关注航班
    loop.run()  # 主程序


if __name__ == '__main__':
    main()
#     """多进程启动"""
#     # 加载appium进程
#     # 构建appium进程组
#     for i in range(2):
#         port = 4730 + 5 * i
#         devi_port = 62025 + i
#         result = Process(target=main, args=(port, devi_port))
#         print('process start')
#         result.start()
#
#     result.join()
#     print('Process close')

# 15926309718
# 19801216



