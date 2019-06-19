# coding=utf-8
# 作者    ： Administrator
# 文件    ：Login.py
# IED    ：PyCharm
# 创建时间 ：2019/6/19 0:07
import os
import re
import time
import logging
from appium import webdriver
from datetime import datetime
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


class News:
    def __init__(self):
        self.log = self.log_init()
        # 关注机场数量
        self.ports_num = None
        # 统计已查看机场列表
        self.airport_names = []
        # 已发短信通知航班号
        self.flight_id = []
        self.desired_caps = {
            "platformName": "Android",
            "deviceName": "OS105",
            "appPackage": "com.feeyo.vz.pro.cdm",
            "appActivity": "com.feeyo.vz.pro.activity.cdm.WelcomeActivity",
            "noReset": True
        }
        self.driver_server = 'http://127.0.0.1:4723/wd/hub'
        self.log.info('机场航班信息实时监测系统启动中...')
        # 启动APP
        self.driver = webdriver.Remote(self.driver_server, self.desired_caps)
        # 设置等待
        self.wait = WebDriverWait(self.driver, 10, 0.5)

    def log_init(self):
        """日志模块"""
        path = os.path.abspath('.') + r'\log\run.log'
        formatter = logging.Formatter('%(asctime)s | %(name)-6s | %(levelname)-6s| %(message)s')
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        fh = logging.FileHandler(path, encoding='utf-8', mode='w')
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
        dialog = self.wait.until(EC.presence_of_element_located((By.ID, 'com.feeyo.vz.pro.cdm:id/radio_chat')))
        dialog.click()
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
            password.send_keys('19790107')
            login_end = self.wait.until(EC.presence_of_element_located((By.ID, 'com.feeyo.vz.pro.cdm:id/login_btn_login')))
            login_end.click()
            self.log.info("账号登录成功!")

        except Exception as e:
            self.log.info("账号已登录!")
            self.log.error(e)

    def loop_look(self):
        """进入关注机场页面"""
        airport_page = self.wait.until(EC.presence_of_element_located((By.ID, 'com.feeyo.vz.pro.cdm:id/radio_airport')))
        airport_page.click()
        self.log.info("开始监控关注机场")
        time.sleep(2)
        self.log.info("等待2秒刷新页面，防止频繁访问页面加载问题")
        # 关注机场数量
        airports_num = self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.feeyo.vz.pro.cdm:id/tab_layout_display_txt_count')))
        ports_num = airports_num[0].text
        self.ports_num = int(re.findall(r'\d', ports_num)[0])
        self.log.info("监控机场数量：{}".format(ports_num))

    def run(self):

        while True:
            # 关注机场列表
            if len(self.airport_names) == self.ports_num:
                self.driver.swipe(500, 500, 500, 2000, 500)
                time.sleep(0.5)
                self.driver.swipe(500, 500, 500, 2000, 500)
                time.sleep(0.5)
                self.driver.swipe(500, 500, 500, 2000, 500)
                self.airport_names = []
            try:
                # 机场名
                airports_name = self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.feeyo.vz.pro.cdm:id/airport_dynamic_new_txt_state')))
                for airport_name in airports_name:
                    airport_name_text = airport_name.text.split('-')[0]
                    if airport_name_text in self.airport_names:
                        continue
                    self.log.info("[{}]：机场航班信息获取中...".format(airport_name_text))
                    self.airport_names.append(airport_name_text)
                    airport_name.click()

                    # 出场延误航班数量
                    mora_num = self.wait.until(EC.presence_of_element_located((By.ID, 'com.feeyo.vz.pro.cdm:id/detail_flow_delay_text')))
                    num = re.findall(r'\d', mora_num.text)
                    if not int(num[0]):
                        self.log.info("[{}]机场暂无延误航班,出场延误航班数：{}".format(airport_name_text, num[0]))
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

                    # 航班号
                    flight_id = self.wait.until(EC.presence_of_all_elements_located(
                        (By.ID, 'com.feeyo.vz.pro.cdm:id/item_display_list_txt_airport_route')))
                    # 延误时间
                    mora_time = self.wait.until(EC.presence_of_all_elements_located(
                        (By.ID, 'com.feeyo.vz.pro.cdm:id/item_display_list_txt_delay_time_plus')))

                    self.log.info("[{}]机场出场延误航班数：{}".format(airport_name_text, len(flight_id)))
                    count = 0
                    for flight in flight_id:

                        mora_time_text = mora_time[count].text
                        count += 1
                        self.log.info('机场[{}]航班号[{}]延误时间[{}]'.format(airport_name_text, flight.text, mora_time_text))
                        if not mora_time_text:
                            continue
                        if int(mora_time_text) < 180:
                            continue
                        else:
                            # 进入航班详情页面
                            flight.click()
                            # 航班号
                            flight_number = self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.feeyo.vz.pro.cdm:id/tab_layout_txt_title')))
                            flight_number_text = flight_number[0].text
                            # 出发地
                            departure = self.wait.until(EC.presence_of_element_located((By.ID, 'com.feeyo.vz.pro.cdm:id/item_start_airport_name')))
                            departure_text = departure.text
                            # 计划起飞时间
                            planning_time =self.wait.until(EC.presence_of_element_located((By.ID, 'com.feeyo.vz.pro.cdm:id/item_start_plan_fly_time')))
                            planning_time_text = planning_time.text
                            # 实际起飞时间
                            departure_time = self.wait.until(EC.presence_of_element_located((By.ID, 'com.feeyo.vz.pro.cdm:id/item_start_fly_time')))
                            departure_time_text = departure_time.text
                            # 目的地
                            destination = self.wait.until(EC.presence_of_element_located((By.ID, 'com.feeyo.vz.pro.cdm:id/item_end_airport_name')))
                            destination_text = destination.text
                            # 计划到达时间
                            planned_time = self.wait.until(EC.presence_of_element_located((By.ID, 'com.feeyo.vz.pro.cdm:id/item_end_plan_fly_time')))
                            planned_time_text = planned_time.text
                            # 预计达到时间
                            estimated_time = self.wait.until(EC.presence_of_element_located((By.ID, 'com.feeyo.vz.pro.cdm:id/item_end_fly_time')))
                            estimated_time_text = estimated_time.text

                            self.log.info("航班：[{}],[{}],实际起飞时间：[{}],出发地：[{}],目的地：[{}],{} 预计到达：[{}],延误时间：[{}]".format(flight_number_text, planning_time_text, departure_time_text,
                                            departure_text, destination_text, planned_time_text, estimated_time_text, mora_time_text))

                            # 短信发送
                            if flight_number_text not in self.flight_id:

                                content = "[{}]机场,[{}]航班,[{}]出发,目的地[{}],延误时间[{}]".format(airport_name_text, flight_number_text,
                                                                                         departure_text, destination_text, mora_time_text)
                                print('发送成功')
                                # send_sms.send_sms('18210836362', content)
                                self.flight_id.append(flight_number_text)

                            self.driver.keyevent(4)  # 返回延误航班页面

                    self.driver.keyevent(4)  # 返回当前机场详情页面
                    time.sleep(1)
                    self.driver.keyevent(4)  # 返回机场列表页面

                # 上滑一屏
                self.driver.swipe(500, 1800, 500, 600, 800)
                time.sleep(2)
            except Exception as e:
                self.log.error(e)
                # self.log.exception(e)
                continue

    @run_time
    def main(self):
        self.loop_look()
        self.run()


if __name__ == '__main__':
    loop = News()
    loop.login()

