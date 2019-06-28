# -*- coding: UTF-8 -*-
# 作者    ： Administrator
# 文件    ：Login.py
# IED    ：PyCharm
# 创建时间 ：2019/6/19 0:07
import os
import re
import time
import logging
import requests
import subprocess
from appium import webdriver
from datetime import datetime
from dateutil.parser import parse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 手动启动模拟器 adb connect 127.0.0.1:62001
# 查看连接 adb devices
import chat


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
        # 日志
        self.log = self.log_init()
        self.log.info('<font color="red"微信登录</font>')
        self.chatpush = chat.Itchat()
        self.log.info('<font color="red"微信登录成功</font>')
        # 效验航班记录文件
        self.flight_MD5()
        # 是否启用短信通知
        self.sms = None
        # 短信通知号码
        self.phone = None
        # 关注机场数量
        self.ports_num = None
        # 延误航班效验临时列表
        self.flight = []
        # 程序运行次数
        self.count = 1
        # 屏幕尺寸
        self.x = None
        self.y = None
        self.log.info('机场航班信息实时监测系统启动中...')
        # 启动APP
        self.driver = None
        # 设置等待
        self.wait = None

    def adb_devices(self):
        """读取设备列表"""
        get_cmd = "adb devices"  # 查询连接设备列表
        count = 0
        while True:
            # 连接设备
            if count > 2:
                self.log.info("读取设备信息失败,请检查设备是否成功启动")
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
            if not len(output) > 1:
                self.log.info("读取设备信息失败,自动重启中...")
                count += 1
                continue
            # 连接设备列表
            devices = [i.split('\t') for i in output[1:]]
            # 读取成功列表
            success = [i[0] for i in devices if i[1] == 'device']
            for i in success:
                self.log.info("设备连接成功：[{}]".format(i))
            break

    def get_size(self):
        """获取屏幕尺寸"""
        self.x = self.driver.get_window_size()['width']
        self.y = self.driver.get_window_size()['height']

    def conf(self):
        """读取配置文件"""

        path = os.path.abspath('.') + '\config\config.txt'
        with open(path, 'r', encoding='utf-8') as f:
            a = [i.replace('\n', '') for i in f.readlines()]
            self.sms = eval(a[0])
            if self.sms:
                self.phone = str(a[1]).split(',')
        print('<font color="green">配置文件读取成功!通知号码：[{}]</font>'.format(self.phone))

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
        count = 1
        while True:
            if count > 3:
                break
            try:
                dialog = self.driver.find_element_by_id('com.feeyo.vz.pro.cdm:id/radio_chat')
                dialog.click()
                break
            except Exception as e:
                self.driver.keyevent(4)
                count += 1
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
            flang = False
            try:
                # 机场名
                airports_name = self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.feeyo.vz.pro.cdm:id/airport_dynamic_new_txt_state')))

                for i in range(len(airports_name)):
                    time.sleep(1)
                    airport_name_text = airports_name[i].text.split('-')[0]
                    # 效验是否已处理
                    res = self.validation(airport_name_text)
                    if res == 1:
                        flang = True
                        print("当前循环已完成,开启下一轮监控")
                        break
                    elif not res == 2:
                        self.log.info("[{}]机场已处理".format(airport_name_text))
                        continue
                    self.log.info("[{}]：机场航班信息获取中...".format(airport_name_text))
                    airports_name[i].click()

                    # 出场延误航班数量
                    mora_num = self.get_attr(airports_name[i], 'com.feeyo.vz.pro.cdm:id/detail_flow_delay_text')
                    if not mora_num:
                        self.log.info("[{}]机场信息获取失败".format(airport_name_text))
                        continue
                    num = re.findall(r'\d', mora_num.text)
                    if not int(num[0]):
                        self.log.info("[{}]机场暂无延误航班,出场延误航班数：{}".format(airport_name_text, num[0]))
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
                    time.sleep(2)
                    if not int(mora_page[2].text):
                        print("获取延误航班信息失败，请检查网络环境!")
                        self.driver.keyevent(4)  # 返回当前机场详情页面
                        time.sleep(1)
                        self.driver.keyevent(4)  # 返回机场列表页面
                        continue

                    self.log.info('<font color="red">航班延误时间计算中,请稍后...</font>')
                    if int(mora_page[2].text) > 20:
                        i = int(int(mora_page[2].text)/20)
                        # 计算航班延误时间
                        for q in range(i):
                            self.time_calculation(airport_name_text)
                            time.sleep(1)
                            self.driver.swipe(self.x/2, self.y*3/5, self.x/2, self.y/5, 800)
                            time.sleep(2)
                            self.driver.swipe(self.x/2, self.y*3/5, self.x/2, self.y/5, 800)

                    self.time_calculation(airport_name_text)

                    self.driver.keyevent(4)  # 返回当前机场详情页面
                    time.sleep(0.5)
                    self.driver.keyevent(4)  # 返回机场列表页面
                    time.sleep(1)
                if flang:
                    continue
                # 滑动前添加等待时间 防止滑动出错
                time.sleep(1)
                self.driver.swipe(self.x/2, self.y*3/5, self.x/2, self.y/5, 800)
                # self.driver.swipe(500, 1150, 500, 500, 1000)
                time.sleep(1)

            except Exception as e:
                print(e)
                self.log.error(e)
                self.log.exception(e)
                break

    def validation(self, airport_name):
        """
        效验机场是否处理过
        :param airport_name: 机场名
        :return: False 没有处理
        """
        path = os.path.abspath('.') + r'\log\airport_names.txt'
        with open(path, 'a+', encoding='utf-8')as f:
            f.seek(0)
            a = [i.replace('\n', '') for i in f.readlines()]
            if len(a) >= self.ports_num:
                f.seek(0)  # 移动光标
                f.truncate()  # 清空文件
                self.new_round()
                return 1
            if airport_name not in a:
                f.write(airport_name + '\n')
                return 2

    def new_round(self):
        """开启新一轮监控"""
        time.sleep(1)
        self.driver.swipe(self.x/2, self.y/4, self.x/2, self.y*3/4, 200)
        time.sleep(1)
        self.driver.swipe(self.x/2, self.y/4, self.x/2, self.y*3/4, 200)
        time.sleep(1)
        self.driver.swipe(self.x/2, self.y/4, self.x/2, self.y*3/4, 200)
        self.log.info('<font color="darkcyan">防止刷新太快,刷新一遍后等待5秒再次启动</font>')
        time.sleep(5)
        self.count += 1

    def time_calculation(self, airport_name):
        """
        计算航班延误时间
        :param airport_name: 机场名
        :return:
        """
        count = 1
        flight_list = []
        while True:
            if count >= 3:
                self.log.info('<font color="red">读取航班时间失败!暂时跳过...</font>'.format(count))
                return
            try:
                # 机号
                machine_number = self.wait.until(EC.presence_of_all_elements_located(
                    (By.ID, 'com.feeyo.vz.pro.cdm:id/item_display_list_txt_planeno')))
                machine = [i.text for i in machine_number]
                # 航班号
                flights = self.wait.until(EC.presence_of_all_elements_located(
                    (By.ID, 'com.feeyo.vz.pro.cdm:id/item_display_list_txt_airport_route')))

                # 目的地
                destinations = self.driver.find_elements_by_id(
                    'com.feeyo.vz.pro.cdm:id/item_display_list_txt_airport_departure_or_destination')
                # 计划起飞时间
                plans_time = self.driver.find_elements_by_id(
                    'com.feeyo.vz.pro.cdm:id/item_display_list_txt_airport_plane_position')
                # 预计起飞时间
                estimates = self.driver.find_elements_by_id('com.feeyo.vz.pro.cdm:id/item_display_list_txt_delay_time')
                break
            except Exception as e:
                self.log.info('<font color="red">读取航班时间失败!重试[{}]...</font>'.format(count))
                count += 1
                continue

        for i in range(len(machine)):
            if machine[i] == '--':
                self.log.info("机号为空跳过")
                continue

            # 航班号
            # flights_xpath = '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.feeyo.' \
            #                 'vz.pro.cdm:id/recycler_view"]/android.widget.LinearLayout[{}]/android.widget' \
            #                 '.TextView[1]'.format(i + 1)
            # flights = self.wait.until(EC.presence_of_element_located((By.XPATH, flights_xpath)))
            flight = flights[i].text  # 航班号
            if flight.replace(':', '').isdigit() or len(flight) <= 1 or '+' in flight:
                print("航班号读取错误[{}]".format(flight))
                continue

            # 航班已处理过跳过
            if flight in self.flight or flight in flight_list:
                self.log.info("[{}]航班已处理".format(flight))
                continue

            if '9C' in flight or 'AQ' in flight:
                self.log.info("[{}]航班9C or AQ开头 跳过".format(flight))
                flight_list.append(flight)
                continue

            # 本次处理航班号存入临时列表 等待当前页面处理完成统一写入文件
            flight_list.append(flight)
            self.log.info('<font color="green">[{}]航班延误时间计算中...</font>'.format(flight))

            # 目的地
            # destination_xpath = '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.feeyo.' \
            #                     'vz.pro.cdm:id/recycler_view"]/android.widget.LinearLayout[{}]/android.widget' \
            #                     '.TextView[3]'.format(i+1)
            # destinations = self.driver.find_element_by_xpath(destination_xpath)

            # 计划起飞时间
            # plans_time_xpath = '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.feeyo.' \
            #                    'vz.pro.cdm:id/recycler_view"]/android.widget.LinearLayout[{}]/android.widget' \
            #                    '.TextView[4]'.format(i+1)
            # plans_time = self.driver.find_element_by_xpath(plans_time_xpath)

            # 预计起飞时间
            # estimates_xpath = '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.feeyo.vz.pro.cdm:id' \
            #                   '/recycler_view"]/android.widget.LinearLayout[{}]/android.widget.LinearLayout' \
            #                   '/android.widget.TextView[2]'.format(i+1)
            # estimates = self.driver.find_element_by_xpath(estimates_xpath)

            destination = destinations[i].text  # 目的地
            if destination.replace(':', '').isdigit() or len(destination) <= 1:
                print("目的地读取错误[{}]".format(destination))
                continue
            plan_time = plans_time[i].text  # 计划起飞
            if not plan_time.replace(':', '').isdigit():
                print("计划起飞时间读取错误[{}]".format(plan_time))
                continue
            estimate = estimates[i].text  # 预计起飞
            if not estimate.replace(':', '').isdigit():
                print("预计起飞时间读取错误[{}]".format(estimate))
                continue
            # TODO
            with open("t.txt", 'a+', encoding='utf-8') as f:
                f.write('{} {} {} {}'.format(flight, destination,plan_time,estimate) + '\n')
            self.log.info('{} {} {} {}'.format(flight, destination,plan_time,estimate))
            # 计算时间差
            mora_time = int((parse(estimate) - parse(plan_time)).total_seconds() / 60)
            # 判断是否隔天航班
            if str(mora_time)[0] == '-':
                mora_time = (24 * 60 - int(str(mora_time)[1:]))

            content = '机场[{}]航班号[{}]出发地[{}]目的地[{}]延误时间[{}]'.format(airport_name, flight, airport_name, destination,
                                                                   mora_time)
            if mora_time < 150 or mora_time > 1000:
                self.log.info('<font color="red">{},不符合条件</font>'.format(content))
                continue
            self.log.info('<font color="green">content:{}</font>'.format(content))

            # 微信推送
            self.chatpush.SendFriend(content)
            self.log.info('<font color="green">微信推送发送成功</font>')
            # 短信发送
            # if self.sms:
            #     # self.log.info("短信发送成功{}".format(content))
            #     self.sms_post(content)

        # 航班号写入文件
        if not flight_list:
            return
        self.update_flight(flight_list)
        return

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

    def flight_MD5(self):
        """"
        效验当日已发送短信航班信息 避免重复读取
        flight  航班号
        """
        # 短信发送日志信息
        path = os.path.abspath('.') + r'\log\flight_MD5.txt'
        if os.path.exists(path):
            # 获取文件创建日期
            filetime = os.path.getctime(path)
            mailtime = datetime.fromtimestamp(filetime).strftime('%Y-%m-%d')
            # 当前系统日期
            currdate = time.time()
            mailtime1 = datetime.fromtimestamp(currdate).strftime('%Y-%m-%d')
            # 判断文件创建日期是否等于当前系统日期 如不相等 删除前一天的发送记录
            if mailtime != mailtime1:
                os.remove(path)
                self.log.info("<font color='red'>日期更新,删除已处理航班信息记录文件!</font>")
                self.log.info("<font color='red'>文件删除中...等待30秒刷新系统缓存</font>")
                time.sleep(30)
            else:
                self.log.info("<font color='red'>航班信息记录文件日期没有更新!</font>")

    def update_flight(self, flight=None):
        """
        更新已处理航班号文件
        flight 需更新航班号列表
        """
        path = os.path.abspath('.') + r'\log\flight_MD5.txt'
        with open(path, 'a+', encoding='utf-8')as f:
            if flight:
                for i in flight:
                    f.write(i + '\n')
                self.log.info('更新航班记录成功!')
            f.seek(0)
            self.flight = [i.replace('\n', '') for i in f.readlines()]
            self.log.info('读取已处理航班记录成功!')

    def sms_post(self, content):
        """短信发送"""
        for i in range(len(self.phone)):
            time.sleep(1)
            url = 'http://sms.kingtto.com:9999/sms.aspx'
            content = '【智能航班】{}'.format(content)
            params = {
                'action': 'send',
                'account': 'hongkegu',
                'password': 'chenxiaoli2013',
                'userid': '4112',
                'mobile': self.phone[i],
                'content': content,
                'rt': 'json'
            }

            response = requests.post(url, data=params)
            result = response.json()
            if result['Message'] == 'ok':
                self.log.info("通知短信发送成功：{}{}".format(self.phone[i], content))
            else:
                self.log.error("通知短信发送失败：{}").format(result['message'])
            if result['RemainPoint'] < 5000:
                self.log.info("<font color='red'>短信余额不足请及时充值!</font>")


@run_time
def main():

    loop = Spider()
    loop.adb_devices()  # 读取设备信息
    loop.update_flight()  # 读取航班记录文件
    loop.conf()  # 读取配置文件
    desired_caps = {
        "platformName": "Android",
        # "deviceName": "127.0.0.1:{}".format(62025),
        "deviceName": "d750dac5",
        "appPackage": "com.feeyo.vz.pro.cdm",
        "appActivity": "com.feeyo.vz.pro.activity.cdm.WelcomeActivity",
        "noReset": True
    }
    driver_server = 'http://127.0.0.1:{}/wd/hub'.format(4730)
    # 启动APP
    loop.driver = webdriver.Remote(driver_server, desired_caps)
    # 设置等待
    loop.wait = WebDriverWait(loop.driver, 10, 0.5)
    time.sleep(10)
    loop.login()  # 登录
    loop.get_size()  # 获取屏幕尺寸
    loop.loop_look()  # 进入关注航班
    loop.run()  # 主程序


if __name__ == '__main__':
    main()


# 15926309718
# 19801216



