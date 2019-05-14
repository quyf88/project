# -*- coding: utf-8 -*-
# @Time    : 2019/5/5 16:09
# @Author  : project
# @File    : group_chat.py
# @Software: PyCharm
"""
自动添加群聊好友
"""
import time
import re
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from appium.webdriver.connectiontype import ConnectionType
from selenium.webdriver.support import expected_conditions as EC


class GroupChat:
    def __init__(self):
        self.desired_caps = {
            "platformName": "Android",
            "deviceName": "OS105",
            "appPackage": "com.tencent.mm",
            "appActivity": ".ui.LauncherUI",
            "noReset": True  # 获取登录状态
        }
        self.driver_server = 'http://127.0.0.1:4723/wd/hub'
        print('微信启动...')
        # 启动微信
        self.driver = webdriver.Remote(self.driver_server, self.desired_caps)
        # 设置等待
        self.wait = WebDriverWait(self.driver, 30, 1, AttributeError)
        # 计数
        self.count = 0
        # 获取连接网络方式 返回1,2,3,4,6
        self.network = self.driver.network_connection

    def login(self):
        """登录模块"""

        print("-----点击登录-----")
        login = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/e4g')))
        login.click()

        # 输入手机号
        print("-----账号输入-----")
        phone = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/kh')))
        phone.click()
        phone_num = ""
        # phone_num = input('请输入账号：')
        # phone.send_keys(phone_num)
        phone.send_keys(phone_num)

        # 点击下一步
        print("-----点击下一步-----")
        button = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/axt')))
        button.click()

        # 输入密码
        print("-----密码输入-----")
        # pass_w = input('请输入密码：')
        pass_w = ""
        # presence_of_element_located 元素加载出，传入定位元组，如(By.ID, 'p')
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/kh')))
        password.send_keys(pass_w)

        # 点击登录
        print("-----登录中-----")
        login = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/axt')))
        login.click()

        print("-----关闭通讯录弹窗-----")
        # WebDriverWait 10秒内每隔2秒运行一次直到找到元素 规定时间内找不到则报错 element_to_be_clickable 元素可点击
        tip = WebDriverWait(self.driver, 10, 2).until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/az9')))
        tip.click()

    def group_page(self):
        """进入群聊页面"""

        # 通讯录
        tab = self.wait.until(EC.presence_of_element_located((By.XPATH,
             '//*[@resource-id="com.tencent.mm:id/bq"]/android.widget.LinearLayout/android.widget.RelativeLayout[2]')))
        print('获取到通讯录按钮')
        tab.click()
        print("-----点击通讯录-----")

        # 群聊
        group = self.wait.until(EC.presence_of_element_located((By.XPATH,
             '//*[@resource-id="com.tencent.mm:id/mi"]/android.widget.LinearLayout/android.widget.RelativeLayout[2]')))
        print('获取到群聊按钮')
        group.click()
        print("-----点击群聊-----")

    def group_get(self):
        """获取群聊信息"""
        while True:
            try:
                # 获取群聊数量
                group_amount = self.driver.find_element_by_id("com.tencent.mm:id/b0p")
                amount = group_amount.get_attribute("text")
                self.count = int(re.search(r'\d+', amount).group())
                if int(amount[:1]) == 0:
                    return print("该账号共有{}，退出系统。".format(amount))
                print("该账号共有:{}个群聊".format(self.count))
                break
            except:
                self.driver.swipe(500, 1800, 500, 500, 1000)

        self.driver.swipe(500, 500, 500, 1220, 1000)

    def add_friend(self):
        """添加好友"""
        group_list = []

        # 进入群聊页面 获取群列表
        group_item = self.driver.find_elements_by_id('com.tencent.mm:id/mz')
        for group in group_item[4:]:
            if self.count == 0:
                break
            group.click()

            # 获取当前群名称
            get_group_name = self.wait.until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/k3")))
            group_name = re.sub(r'\(.*\)', '', get_group_name.get_attribute("text"))
            print('获取群聊:{}中...'.format(group_name))

            # 判断当前群是否添加
            if group_name in group_list:
                print("跳过：{}，已添加过".format(group_name))
                continue
            # 进入群成员页面
            member = self.wait.until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/jy")))
            member.click()
            print("成功获取群成员")

            # 获取当前群聊成员数量
            member_number = self.wait.until(EC.presence_of_element_located((By.ID, "android:id/text1")))
            member_number = member_number.get_attribute("text")
            amount = re.search(r'\d+', member_number).group()
            print("该群共有：{}人".format(amount))

            # 判断当前页面是否有“查看全部群成员”标签
            view_all = self.driver.find_elements_by_id('android:id/title')
            # 群聊人数较少直接添加
            if len(view_all) != 0 and view_all[0].get_attribute("text") != '查看全部群成员':
                print("已显示全部群成员")

                # 获取当前群聊成员列表 发送添加请求 find_elements_by_id 此方法返回一个列表
                details = self.driver.find_elements_by_id('com.tencent.mm:id/e0c')
                for detail in details:
                    time.sleep(0.5)
                    # 判断"+"号 name = accessibility id
                    if detail.get_attribute("name") == "添加成员":
                        break
                    else:
                        detail.click()  # 进入个人详情

                    # 获取"添加到通讯录"标签
                    time.sleep(2)
                    friend_add = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/cs')))

                    # 判断是否已是好友
                    if friend_add.get_attribute('text') == '发消息':
                        wechat_number = self.driver.find_element_by_id('com.tencent.mm:id/b45')
                        print("{}：已经是您的好友".format(wechat_number.get_attribute("text")))
                        time.sleep(0.5)
                        self.driver.keyevent(4)
                        continue

                    friend_add.click()  # 点击"添加到通讯录"
                    time.sleep(1)

                    # 判断对方是否开启好友验证
                    if friend_add.is_displayed():
                        time.sleep(0.5)
                        self.driver.keyevent(4)
                        continue

                    # 判断对方是否设置隐私
                    privacy = self.driver.find_elements_by_id("com.tencent.mm:id/az_")
                    if len(privacy) != 0:
                        privacy[0].click()
                        # time.sleep(0.5)
                        self.driver.keyevent(4)
                        continue

                    # 清空默认验证申请文本
                    clear_text = self.wait.until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/e0o")))
                    clear_text.clear()

                    # 发送
                    _count1 = 0
                    while True:
                        try:
                            if _count1 == 1:
                                time.sleep(0.5)
                                self.driver.keyevent(4)
                                break
                            TouchAction(self.driver).tap(x=957, y=121).wait(200).perform()
                            send = self.driver.find_element_by_id('com.tencent.mm:id/jx')
                            if send.is_displayed():
                                _count1 += 1
                                continue
                        except:
                            time.sleep(0.5)
                            self.driver.keyevent(4)
                            break

                time.sleep(0.5)
                self.driver.keyevent(4)
                time.sleep(0.5)
                self.driver.keyevent(4)
                self.group_page()

            elif len(view_all) == 0:
                self.driver.swipe(500, 1800, 500, 500, 2000)  # 向上滑一屏
                view_all = self.driver.find_elements_by_id('android:id/title')
                view = view_all[0].get_attribute("text")
                if view == "查看全部群成员":
                    view_all[0].click()
                    time.sleep(1)
                    self.driver.swipe(1000, 400, 1000, 2000, 500)
                    time.sleep(0.5)
                    # 添加好友
                    while True:
                        temp = []
                        flag = True
                        details = self.driver.find_elements_by_id('com.tencent.mm:id/auq')

                        for detail in details:
                            detail_text = detail.get_attribute("text")
                            time.sleep(0.5)
                            if len(temp) >= int(amount):
                                flag = False
                                print("本群已经添加完成")
                                break
                            elif detail_text in temp:
                                print("跳过：{}，已被添加过".format(detail_text))
                                continue

                            # 进入个人详情 获取"添加到通讯录"标签
                            detail.click()
                            time.sleep(1.5)
                            friend_add = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/cs')))

                            # 判断是否已是好友
                            if friend_add.get_attribute("text") == '发消息':
                                # wechat_number = self.driver.find_element_by_id('com.tencent.mm:id/b45')
                                print("{}：已经是您的好友".format(detail_text))
                                temp.append(detail_text)
                                time.sleep(0.5)
                                self.driver.keyevent(4)
                                continue

                            # 点击添加到通讯录
                            friend_add.click()
                            time.sleep(1)

                            # 判断对方是否开启好友验证
                            if friend_add.is_displayed():
                                temp.append(detail_text)
                                print("添加好友:{},成功".format(detail_text))
                                time.sleep(0.5)
                                self.driver.keyevent(4)
                                continue

                            # 判断对方是否设置隐私
                            privacy = self.driver.find_elements_by_id("com.tencent.mm:id/az_")
                            if len(privacy) != 0:
                                temp.append(detail_text)
                                privacy[0].click()
                                self.driver.keyevent(4)
                                continue

                            # 判断对方账户是否异常
                            if friend_add.is_displayed():
                                temp.append(detail_text)
                                self.driver.keyevent(4)
                                print("对方账户异常，无法添加。")
                                continue

                            # 清空默认验证申请文本
                            clear_text = self.wait.until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/e0o")))
                            clear_text.clear()

                            # 发送
                            _count = 0
                            while True:
                                TouchAction(self.driver).tap(x=957, y=121).wait(500).perform()
                                if friend_add.is_displayed():
                                    temp.append(detail_text)
                                    print("添加好友:{},消息发送成功".format(detail_text))
                                    time.sleep(0.5)
                                    self.driver.keyevent(4)
                                    break
                                elif _count == 1:
                                    temp.append(detail_text)
                                    self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/kb'))).click()
                                    self.driver.keyevent(4)
                                    break
                                else:
                                    _count += 1
                                    continue

                        time.sleep(0.5)
                        self.driver.swipe(500, 1600, 500, 600, 1200)
                        if flag is False:
                            temp.clear()
                            break

                    time.sleep(0.5)
                    self.driver.keyevent(4)
                    time.sleep(0.5)
                    self.driver.keyevent(4)
                    time.sleep(0.5)
                    self.driver.keyevent(4)
                    self.group_page()

            # 当前群添加完成
            group_list.append(group_name)
            self.count -= 1
            print("群添加完成：{}".format(group_name))

        self.driver.swipe(500, 1800, 500, 500, 2000)
        print("当前账号添加完成，退出系统！")

    def main(self):
        # self.login()
        self.group_page()
        self.group_get()
        self.add_friend()


if __name__ == '__main__':
    add = GroupChat()
    add.main()
