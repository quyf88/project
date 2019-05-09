# -*- coding: utf-8 -*-
# @Time    : 2019/5/5 16:09
# @Author  : project
# @File    : group_chat.py
# @Software: PyCharm
"""
自动添加群聊好友
"""

from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
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
        # 返回按钮
        self.back = None

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

    def group_list(self):
        """进入群聊列表"""

        # 点击通讯录
        tab = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@resource-id="com.tencent.mm:id/bq"]/android.widget.LinearLayout/android.widget.RelativeLayout[2]')))
        print('获取通讯录按钮')
        tab.click()
        print("-----点击通讯录-----")

        # 点击群聊
        group = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@resource-id="com.tencent.mm:id/mi"]/android.widget.LinearLayout/android.widget.RelativeLayout[2]')))
        print('获取群聊按钮')
        group.click()
        print("-----点击群聊-----")

    def friend_add(self):
        """添加好友"""

        self.back = self.driver.find_element_by_accessibility_id("返回")

        # 获取群聊数量
        group_amount = self.wait.until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/b0p")))
        amount = group_amount.get_attribute("text")
        if int(amount[:1]) == 0:
            return print("该账号共有{}，退出系统。".format(amount))
        print("该账号共有{}".format(amount))

        # 进入群聊页面
        for i in range(int(amount[:1])):
            item_xpath = '//*[@resource-id="com.tencent.mm:id/mi"]/android.widget.LinearLayout[{}]'.format(i + 1)
            group_item = self.wait.until(EC.presence_of_element_located((By.XPATH, item_xpath)))
            print('获取第{}个群聊'.format(i + 1))
            group_item.click()

            # 进入群成员页面
            member = self.wait.until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/jy")))
            member.click()
            print("成功获取群成员")

            # 获取群聊成员数量
            member_number = self.wait.until(EC.presence_of_element_located((By.ID, "android:id/text1")))
            member_number = member_number.get_attribute("text")
            print("该群共有：{}人".format(member_number))

            # 查看全部群成员
            try:
                view_all = WebDriverWait(self.driver, 3, 1).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@resource-id="android:id/list"]/android.widget.LinearLayout/*[@resource-id="android:id/title"]')))
                view_all.click()

                # 添加好友
                details = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/auo')))
                details.click()
                friend_add = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/cs')))
                friend_add.click()
                send = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/jx')))
                send.click()

            except Exception:
                print("已显示全部群成员")
                # 添加好友 find_elements_by_id 此方法返回一个列表
                details = self.driver.find_elements_by_id('com.tencent.mm:id/e0c')

                for detail in details:
                    detail.click()
                    friend_add = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/cs')))

                    # 判断是否已是好友
                    if friend_add.get_attribute("text") == '发消息':
                        wechat_number = self.driver.find_element_by_id('com.tencent.mm:id/b45')
                        print("{}：已经是您的好友".format(wechat_number.get_attribute("text")))
                        self.back.click()
                    elif self.driver.find_element_by_accessibility_id("添加成员"):
                        # TODO
                        pass

                    friend_add.click()
                    send = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/jx')))
                    send.click()
                    self.back.click()

                self.back.click()  # 返回
                self.back.click()
                self.group_list()  # 进入群聊页面


if __name__ == '__main__':
    add = GroupChat()
    # add.login()
    add.group_list()
    add.friend_add()




