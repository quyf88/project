# coding=utf-8
# 作者    ： Administrator
# 文件    ：spider.py
# IED    ：PyCharm
# 创建时间 ：2019/8/23 19:30
import os
import re
import csv
import time
import random
import datetime
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support import expected_conditions as EC

"""
获取好友基本信息和朋友圈动态
"""


class WeChatSpider:
    def __init__(self):
        self.desired_caps = {
            "platformName": "Android",
            "deviceName": "OS105",
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
        self.listion = []
        self.name = None
        self.content = None
        # self.day = int(input('输入获取天数：'))
        self.day = 1

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

    def get_friends(self):
        """
        获取好友列表
        """
        print('-----检测账号是否登录-----')
        print('-------账号已登录-----')
        print("-----获取通讯录-----")
        tab = self.wait.until(EC.presence_of_element_located((By.XPATH,
                '//*[@resource-id="com.tencent.mm:id/bq"]/android.widget.LinearLayout/android.widget.RelativeLayout[2]')))
        tab.click()

        print('-----获取好友列表-----')
        while True:
            usernames = self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.tencent.mm:id/ng')))
            for username in usernames:
                self.name = username.text
                print('*'*50)
                print('好友：[{}] 信息获取中'.format(self.name))
                jumps = ['微信团队', '微信支付小管家', '文件传输助手']
                # if username.text != 'A0东北云南呼伦贝尔桂林章天宇13833285615':
                #     continue
                if username.text in jumps:
                    continue
                if username.text in self.listion:
                    # print('{}已处理跳过')
                    continue
                self.listion.append(self.name)

                # 进入好友详情页面
                username.click()
                yield

            # 向上滑动一屏
            self.driver.swipe(self.x/4, self.y*3/4, self.x/4, self.y/4, 1000)

    def if_one_self(self):
        """
        判断是否自己
        :return:
        """
        _one_self = self.driver.find_elements_by_id('com.tencent.mm:id/cs')
        _one_self = [i for i in _one_self if i.text == '音视频通话']
        if not _one_self:
            print('自己,跳过!')
            self.driver.keyevent(4)
            time.sleep(0.5)
            return False
        return True

    def get_signature(self):
        """
        获取个性签名
        :return:
        """
        # 判断是否为好友设置标签
        labels = self.driver.find_elements_by_id('com.tencent.mm:id/dmn')
        if len(labels):
            self.wait.until(EC.presence_of_all_elements_located((By.ID, 'android:id/title')))[1].click()
        else:
            # 进入更多信息页面
            self.wait.until(EC.presence_of_all_elements_located((By.ID, 'android:id/title')))[2].click()
        # time.sleep(1)
        # 获取个性签名信息
        sign_1 = self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.tencent.mm:id/dmw')))
        sign_1 = [i for i in sign_1 if i.text == '个性签名']
        if sign_1:
            content = self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.tencent.mm:id/dmx')))[1].text
            self.content = content.replace('\n', '').replace('\r', '')
            print('个性签名：{}'.format(self.content))
        else:
            self.content = '无个性签名'
            print('无个性签名')
        # for i in range(len(sign_1)):
        #     q = i if sign_1[i].text == '个性签名' else False
        #     if q:
        #         content = self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.tencent.mm:id/dmx')))[1].text
        #         self.content = content.replace('\n', '').replace('\r', '')
        #         print('个性签名：{}'.format(self.content))
        #     else:
        #         self.content = '无个性签名'
        #         # print('无个性签名')

        self.driver.keyevent(4)
        time.sleep(1)

    def get_friend_num(self):
        """
        获取好友微信号
        :return:
        """
        # 好友微信号
        wx_num = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/b45'))).text
        print(wx_num)
        return wx_num

    def judge(self):
        """
        各种异常判断
        :return:
        """
        # 判断是否设置标签
        # labels = self.driver.find_elements_by_id('com.tencent.mm:id/dmn')
        # 页面标签列表
        b_list = self.driver.find_elements_by_id('com.tencent.mm:id/d7w')

        if b_list:
            b_list[0].click()
        else:
            print('好友没有开通朋友圈')
            self.driver.keyevent(4)
            time.sleep(0.5)
            return False

        # 判断好友是否设置隐私
        try:
            WebDriverWait(self.driver, 3, 1, AttributeError).until(EC.presence_of_all_elements_located((By.ID, 'com.tencent.mm:id/egv')))
            print('朋友圈没有开放')
            self.driver.keyevent(4)
            time.sleep(1)
            self.driver.keyevent(4)
            time.sleep(0.5)
            return False
        except:
            return True

    def get_circle_of_friends(self):
        """
        获取朋友圈信息
        :return:
        """
        cons_list = []
        release = ''
        while True:
            flag = False
            # 判断有没有数据
            bottoms = self.driver.find_elements_by_id('com.tencent.mm:id/ahy')
            if len(bottoms):
                self.driver.keyevent(4)
                time.sleep(0.5)
                self.driver.keyevent(4)
                time.sleep(0.5)
                return
            # 朋友圈数据列表
            cons = self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.tencent.mm:id/lk')))
            for i in range(len(cons)-1):
                # 发布时间 date 日期 time 月份
                try:
                    date = WebDriverWait(self.driver, 1, 0.1, AttributeError).until(EC.presence_of_all_elements_located((By.XPATH, '//android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout[{}]/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView'.format(i+2))))
                    if len(date) > 1:
                        release = date[1].text + date[0].text
                    else:
                        release = date[0].text
                except Exception as e:
                    pass

                # 获取不到月份 默认当前月份 这种情况只会在今天 昨天 数据量多时出现
                if release == '今天':
                    release = datetime.datetime.now().strftime('%m,%d').replace(',', '月')
                elif release == '昨天':
                    release = datetime.datetime.now() + datetime.timedelta(days=-1)
                    release = release.strftime('%m,%d').replace(',', '月')
                print(release)
                # 判断时间
                old_time = datetime.datetime.strptime('2019年' + release, '%Y年%m月%d')
                new_time = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y,%m,%d'), '%Y,%m,%d')
                if (new_time-old_time).days >= self.day:
                    print('大于{}天不获取'.format(self.day))
                    flag = True
                    break

                # 内容
                try:
                    # 获取信息内容和图片数量
                    con = WebDriverWait(self.driver, 1, 0.1, AttributeError).until(EC.presence_of_all_elements_located((By.XPATH,
                            '//android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout[{}]/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView'.format(
                                i + 2))))
                    content = con[0].text.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
                except:
                    print('跳过')
                    continue
                    # try:
                    #     WebDriverWait(self.driver, 1, 0.1, AttributeError).until(EC.presence_of_all_elements_located((
                    #                                                                                                  By.XPATH,
                    #                                                                                                  '//android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout[{}]/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.TextView'.format(
                    #                                                                                                      i + 2))))
                    #     print('文字信息跳过')
                    #     continue
                    # except:
                    #     WebDriverWait(self.driver, 1, 0.1, AttributeError).until(EC.presence_of_all_elements_located((
                    #                                                                                                  By.XPATH,
                    #                                                                                                  '//android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout[{}]/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView'.format(
                    #                                                                                                      i + 2))))
                    #     print('链接信息跳过')
                    #     continue
                    #
                # 获取图片数量
                image_num = re.findall(r'\d', con[1].text) if len(con) > 1 else [1]
                print('图片数量：{}'.format(image_num))
                if content in cons_list:
                    print('已处理跳过')
                    continue
                cons_list.append(content)
                print(release, content)

                # 图片保存
                if image_num:
                    con[0].click()
                    image_path = []
                    for n in range(int(image_num[0])):
                        # 保存图片
                        # 长按屏幕
                        self.long_press()
                        rand = random.randint(10000, 99999)
                        name = str(round(time.time() * 1000)) + str(rand) + str(n+1) + '.png'
                        path = os.getcwd() + r'\image\{}'.format(name)
                        image_path.append(path)
                        self.driver.get_screenshot_as_file('image/{}'.format(name))
                        print('第：[{}]张图片下载成功,保存至：{}'.format(n + 1, path))
                        self.driver.keyevent(4)
                        time.sleep(0.5)
                        # 切换下一张图片
                        if n == int(image_num[0])-1:
                            break
                        self.driver.swipe(self.x*3/4, self.y/4, self.x/4, self.y/4, 200)

                    # 数据写入文件
                    t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    data = [self.name, self.content, release, content, image_path, t]
                    self.driver.keyevent(4)
                else:
                    t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    data = [self.name, self.content, release, content, '无图片', t]
                self.data_save([data])

            if flag:
                break

            # 判断是否非好友
            try:
                prompt = self.driver.find_element_by_xpath('//*[@resource-id="com.tencent.mm:id/egt"]/android.widget.TextView[2]').text
                print(prompt)
                break
            except:
                pass

            # 向上滑动一屏
            self.driver.swipe(self.x/4, self.y*3/4, self.x/4, self.y/4, 1000)
            time.sleep(1)
        # 向上滑动一屏
        self.driver.keyevent(4)
        time.sleep(1)
        self.driver.keyevent(4)
        time.sleep(0.5)

    def long_press(self):
        """
        长按屏幕
        :return:
        """
        action1 = TouchAction(self.driver)
        el = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/eg1')))
        el.click()
        print(el)
        action1.long_press(el=el, duration=2000).wait(1000).perform()

        # 编辑
        edits = self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.tencent.mm:id/cw')))
        edit = [i for i in edits if i.text == '编辑']
        edit[0].click()

        # 点击一下屏幕
        tap = self.driver.find_elements_by_class_name('android.widget.FrameLayout')
        if tap:
            action1.tap(tap[0], 100, 100).perform()

    def if_bottom(self):
        """
        判断是否到达底部
        :return:
        """
        bottom = self.driver.find_elements_by_id('com.tencent.mm:id/b0p')
        if bottom:
            print('程序执行完毕!')
            os._exit(0)

    def run(self):
        # 获取好友列表
        for username in self.get_friends():
            # 是否自身
            if not self.if_one_self():
                continue
            # 获取微信号
            self.get_friend_num()
            # 获取个性签名
            self.get_signature()
            # 异常判断
            if not self.judge():
                continue
                # 获取朋友圈信息
            self.get_circle_of_friends()
            # 是否获取完成
            self.if_bottom()

    def data_save(self, data):
        with open("demo.csv", "a+", encoding='utf-8', newline="") as f:
            k = csv.writer(f, delimiter=',')
            with open("demo.csv", "r", encoding='utf-8', newline="") as f1:
                reader = csv.reader(f1)
                if not [row for row in reader]:
                    k.writerow(['好友', '个性签名', '发布日期', '内容', '图片', '获取日期'])
                    k.writerows(data)
                    print('数据写入成功')
                else:
                    k.writerows(data)
                    print('数据写入成功')


if __name__ == '__main__':
    wechat = WeChatSpider()
    wechat.run()




