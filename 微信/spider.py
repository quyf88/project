# coding=utf-8
# 作者    ： Administrator
# 文件    ：批量添加子站.py
# IED    ：PyCharm
# 创建时间 ：2019/8/23 19:30
import os
import re
import csv
import time
import psutil
import shutil
import random
import hashlib
import datetime
import logging
import pandas as pd
from PIL import Image
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support import expected_conditions as EC

"""
获取好友基本信息和朋友圈动态
"""


def log_init():
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


class WeChatSpider:
    def __init__(self):
        self.log = log_init()
        self.desired_caps = {
            "platformName": "Android",
            "deviceName": "FFK0217B11002262",
            "appPackage": "com.tencent.mm",
            "appActivity": ".ui.LauncherUI",
            'noReset': True  # 获取登录状态
        }
        self.driver_server = 'http://127.0.0.1:4730/wd/hub'
        print('**********程序启动中**********')
        # 启动微信
        self.driver = webdriver.Remote(self.driver_server, self.desired_caps)
        # 设置隐形等待时间
        self.wait = WebDriverWait(self.driver, 10, 1, AttributeError)
        # 获取手机尺寸
        self.driver.get_window_size()
        self.x = self.driver.get_window_size()['width']  # 宽
        self.y = self.driver.get_window_size()['height']  # 长
        print(self.x, self.y)
        self.filename = datetime.datetime.now().strftime('%Y-%m-%d') + '.csv'
        # print(f'文件名：{self.filename}')
        self.name = None
        self.content = None
        # self.day = int(input('输入获取天数：'))
        self.day = 2
        # 好友微信号
        self.wx_num = None
        # 是否到达底部
        self.bottom = False
        # 读取关键词
        self.key_wo = self.key_words()
        # 日期
        self.release = None

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

    def get_address_book(self):
        """
        进入通讯录页面
        :return:
        """
        print("-----获取通讯录-----")
        while True:
            tab = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                '//*[@resource-id="com.tencent.mm:id/bq"]/android.widget.LinearLayout/android.widget.RelativeLayout[2]')))
            # print(tab.is_displayed())
            if tab.is_displayed():
                tab.click()
                return
            continue

    def get_friends(self):
        """
        获取好友列表
        """
        print('-----获取好友列表-----')
        while True:
            usernames = self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.tencent.mm:id/ng')))
            for i in range(len(usernames)-2):
                # print('总 {}  第 {}'.format(len(usernames), i))
                try:
                    self.name = usernames[i].text
                except:
                    break
                print('*'*50)
                print('好友：[{}] 信息获取中'.format(self.name))
                jumps = ['微信团队', '微信支付小管家', '文件传输助手']
                # if usernames[i].text != 'A0罗伟芙蓉旅业湖南湖北广东':
                #     continue
                # 效验是否获取
                make = self.make_file_id(self.name)
                print(make)
                if self.friend_validation(make):
                    continue
                if usernames[i].text in jumps:
                    continue

                # 进入好友详情页面
                usernames[i].click()
                yield

            # 是否到达底部
            if self.if_bottom():
                print('到达底部')
                self.bottom = True
                break

            # 向上滑动一屏
            self.driver.swipe(200, 1400, 200, 700, 1000)
            time.sleep(1)

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
        self.wx_num = re.findall(r'微信号: (.*?)$', wx_num)[0].replace(' ', '')

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
            # 写入效验文件
            make = self.make_file_id(self.name)
            self.friend_validation(make, vali=False)
            return False

        # 判断好友是否设置隐私
        try:
            WebDriverWait(self.driver, 3, 1, AttributeError).until(EC.presence_of_all_elements_located((By.ID, 'com.tencent.mm:id/egv')))
            print('朋友圈没有开放')
            self.driver.keyevent(4)
            time.sleep(1)
            self.driver.keyevent(4)
            time.sleep(0.5)
            # 写入效验文件
            make = self.make_file_id(self.name)
            self.friend_validation(make, vali=False)
            return False
        except:
            # 写入效验文件
            # make = self.make_file_id(self.name)
            # self.friend_validation(make, vali=False)
            return True

    def process_image(self, image_name):
        """
        图片处理
        :return:
        """
        # 读取图片
        img = Image.open(image_name)
        # 获取图片尺寸
        (width, height) = img.size
        # 剪裁图片
        phone_image = img.crop((0, 50, width, int(height) - 80))
        # 保存
        phone_image.save(image_name)

    def key_words(self):
        """
        读取关键词
        :param
        :return: True 有关键词
        """
        with open('关键词.txt', 'r') as f:
            cons = f.readlines()
            cons = [i.replace('\n', '') for i in cons]
        print(f'读取关键词成功：{cons}')
        return cons

    def get_circle_of_friends(self):
        """
        获取朋友圈信息
        :return:
        """
        co = 1
        count = 1
        while True:
            flag = False
            # 判断有没有数据
            bottoms = self.driver.find_elements_by_id('com.tencent.mm:id/ahy')
            if len(bottoms):
                self.driver.keyevent(4)
                time.sleep(1)
                self.driver.keyevent(4)
                time.sleep(1)
                return
            # 朋友圈数据列表
            cons = self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.tencent.mm:id/lk')))
            for i in range(len(cons)-2):
                if count > 2:
                    i = i + 1
                else:
                    i = i + 2
                    # 发布时间 date 日期 time 月份
                try:
                    date = WebDriverWait(self.driver, 1, 0.1, AttributeError).until(
                        EC.presence_of_all_elements_located((By.XPATH,
                                                             f'//android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout[{i}]/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView')))
                    if len(date) > 1:
                        release = date[1].text + date[0].text
                    else:
                        release = date[0].text
                except:
                    # 获取不到时间 主动抛出异常
                    if not self.release:
                        print('获取时间失败')
                    else:
                        release = self.release
                self.release = release
                # print(release, self.release)

                # 获取不到月份 默认当前月份 这种情况只会在今天 昨天 数据量多时出现
                if release == '今天':
                    # release = datetime.datetime.now().strftime('%m,%d').replace(',', '月')
                    print('跳过今天数据')
                    continue
                elif release == '昨天':
                    release = datetime.datetime.now() + datetime.timedelta(days=-1)
                    release = release.strftime('%m,%d').replace(',', '月')
                try:
                    # 判断时间
                    old_time = datetime.datetime.strptime('2020年' + release, '%Y年%m月%d')
                    new_time = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y,%m,%d'), '%Y,%m,%d')
                    # print(f'朋友圈发布时间：{old_time}, 当前系统时间：{new_time}')
                    # print((new_time - old_time).days)
                    # os._exit(0)
                except:
                    continue
                # if (new_time - old_time).days >= self.day:
                if (new_time - old_time).days != 1:
                    print('大于{}天不获取'.format(self.day))
                    flag = True
                    break

                # 内容
                try:
                    # 获取信息内容和图片数量
                    con = WebDriverWait(self.driver, 1, 0.1, AttributeError).until(
                        EC.presence_of_all_elements_located((By.XPATH,
                                                             f'//android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout[{i}]/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView')))
                    # 信息内容
                    content = con[0].text.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
                    # 获取图片数量
                    image_num = re.findall(r'\d', con[1].text) if len(con) > 1 else [1]
                except:
                    try:
                        content = self.driver.find_elements_by_xpath(f'//android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout[{i}]/android.widget.LinearLayout[2]/android.widget.LinearLayout[2]/android.widget.TextView')
                        content = content[0].text.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
                        image_num = None
                    except:
                        try:
                            content = self.driver.find_elements_by_xpath(
                                f'//android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout[{i}]/android.widget.LinearLayout[3]/android.widget.LinearLayout[2]/android.widget.TextView')
                            content = content[0].text.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ',
                                                                                                                    '')
                            image_num = None
                        except:
                            break
                print(f'时间：{self.release} 文本：{content} 图片：{image_num}')

                # 判断内容是否包含监控关键词
                key_word = [i for i in self.key_wo if i in content]
                if not key_word:
                    print('未检测到关键词,跳过!')
                    continue

                # 效验信息是否获取
                make = self.make_file_id(content)
                if co == 1:
                    if self.make_file_csv(make):
                        print('好友没有发布新消息')
                        flag = True
                        break
                co += 1
                if self.content_validation(make):
                    print('已处理跳过')
                    continue

                # 图片保存
                if image_num:
                    con[0].click()
                    image_path = []
                    print('图片处理中...')
                    try:
                        for n in range(int(image_num[0])):
                            # 保存图片
                            # 长按屏幕
                            image_name = self.long_press()
                            # 格式 mmexport1572159236223.jpg
                            # path = os.getcwd() + r'\ExportFile\image\{}'.format(image_name)
                            image_path.append(image_name)
                            save_path = datetime.datetime.now().strftime('%Y-%m-%d')
                            save_path = 'ExportFile/image/{}'.format(save_path)
                            if not os.path.exists(save_path):
                                os.mkdir(save_path)
                            
                            # 根据文件名保存图片至指定位置
                            self.driver.get_screenshot_as_file(save_path + '/' + image_name)
                            # self.process_image('ExportFile/config/{}'.format(name))
                            print('第：[{}] 张图片下载成功,文件名：{}'.format(n + 1, image_name))
                            self.driver.keyevent(4)
                            time.sleep(1)
                            # 切换下一张图片
                            if n == int(image_num[0])-1:
                                break
                            self.driver.swipe(self.x*3/4, self.y/4, self.x/4, self.y/4, 200)
                    except Exception as e:
                        # print(e)
                        # self.log.info(e)
                        continue

                    # 数据写入文件
                    t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    # ID, '昵称', '个性签名', '发布日期', '内容', '图片', 校验码, '获取日期'
                    data = [self.wx_num, self.name, self.content, release, content, image_path, make, t]
                    # 已处理信息写入效验文件
                    self.content_validation(make, vali=False)
                    self.data_save([data])
                    self.driver.keyevent(4)
                    time.sleep(1)
                else:
                    t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    data = [self.wx_num, self.name, self.content, release, content, '无图片', make, t]
                    # 已处理信息写入效验文件
                    self.content_validation(make, vali=False)
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
            # 好友朋友圈设置权限
            if self.driver.find_elements_by_id('com.tencent.mm:id/egv'):
                break
            # 向上滑动一屏
            count += 1
            self.driver.swipe(200, 1200, 200, 500, 800)
            time.sleep(2)

        # 写入效验文件
        make = self.make_file_id(self.name)
        self.friend_validation(make, vali=False)

        self.driver.keyevent(4)
        time.sleep(1.5)
        self.driver.keyevent(4)
        time.sleep(1.5)

    def long_press(self):
        """
        长按屏幕
        :return:
        """
        action1 = TouchAction(self.driver)
        el = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/eg1')))
        el.click()
        action1.long_press(el=el, duration=2000).wait(1000).perform()

        # 编辑
        edits = self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.tencent.mm:id/cw')))
        edit = [i for i in edits if i.text == '编辑']
        edit[0].click()
        image_name = 'mmexport' + str(round(time.time() * 1000)) + '.png'
        time.sleep(1)
        # 点击一下屏幕
        tap = self.driver.find_elements_by_class_name('android.widget.FrameLayout')
        if tap:
            action1.tap(tap[0], 100, 100).perform()
        return image_name

    def if_bottom(self):
        """
        判断是否到达底部
        :return: True 到达底部
        """
        # print('判断是否到达底部')
        bottom = self.driver.find_elements_by_id('com.tencent.mm:id/b0p')
        if bottom:
            return True
            # print('程序执行完毕!')
            # os._exit(0)
        return False

    def content_validation(self, make, vali=True):
        """
        效验信息今日是否获取过
        :return:
        """
        if vali:
            with open('ExportFile/ContentValidation.txt', 'r') as f:
                flight = [i.replace('\n', '') for i in f.readlines()]
                if make in flight:
                    return True
                return False
        else:
            with open('ExportFile/ContentValidation.txt', 'a+') as f:
                f.write(make)
                f.write('\n')

    def make_file_csv(self, src):
        """
        效验是否获取
        :return:
        """
        # 加载数据
        path = os.getcwd()
        files = os.listdir(path)
        if self.filename not in files:
            print(f'创建文件:{self.filename}')
            self.data_save([])
            time.sleep(2)
        print(self.filename)
        df_read = pd.read_csv(self.filename)
        df = pd.DataFrame(df_read)
        # 获取指定表头的列数
        phone_num = 0  # 校验码
        for i in range(len(df.keys())):
            if df.keys()[i] == '校验码':
                phone_num = i
        # 循环每一行
        for indexs in df.index:
            # 读取指定行列数据 df.ix[行,列]
            data1 = df.ix[indexs, phone_num]
            # 修改指定单元格数据df.iloc[行, 列]
            if data1 == src:
                df.to_csv(self.filename, index=False, encoding='utf_8_sig')
                return True
        df.to_csv(self.filename, index=False, encoding='utf_8_sig')
        return False

    def friend_validation(self, make, vali=True):
        """
        效验是否获取过该好友信息
        :return:
        """
        if vali:
            with open('ExportFile/FriendValidation.txt', 'r') as f:
                flight = [i.replace('\n', '') for i in f.readlines()]
                if make in flight:
                    return True
                return False
        else:
            with open('ExportFile/FriendValidation.txt', 'a+') as f:
                f.write(make)
                f.write('\n')

    def make_file_id(self, src):
        """
        生成哈希MD5码
        :param src: 字符串
        :return:
        """
        m1 = hashlib.md5()
        m1.update(src.encode('utf-8'))
        return m1.hexdigest()

    def data_save(self, data):
        with open(self.filename, "a+", encoding='utf-8', newline="") as f:
            k = csv.writer(f, delimiter=',')
            with open(self.filename, "r", encoding='utf-8', newline="") as f1:
                reader = csv.reader(f1)
                if not [row for row in reader]:
                    k.writerow(['ID', '昵称', '个性签名', '发布日期', '内容', '图片', '校验码', '获取时间'])
                    k.writerows(data)
                    print('数据写入成功')
                else:
                    k.writerows(data)
                    print('数据写入成功')

        # 数据实时备份
        shutil.copy(self.filename, '备份.csv')

    def run(self):
        time.sleep(2)
        self.get_address_book()
        # 获取好友列表
        for username in self.get_friends():
            # 是否自身
            if not self.if_one_self():
                continue
            # 获取微信号
            self.get_friend_num()
            # 获取个性签名
            # self.get_signature()
            # 异常判断
            if not self.judge():
                continue
                # 获取朋友圈信息
            self.get_circle_of_friends()


class Monitor:
    def write(self):
        """
        将主程序进程号写入文件
        :return:
        """
        # 获取当前进程号
        pid = os.getpid()
        print('当前进程号：{}'.format(pid))
        with open('pid.txt', 'w') as f:
            f.write(str(pid))

    def read(self):
        """
        读取进程中的数据
        :return:
        """
        if os.path.exists('pid.txt'):
            with open('pid.txt', 'r') as f:
                pid = f.read()
                return pid
        else:
            return '0'

    def run(self):
        pid = int(self.read())
        print('读取进程号：{}'.format(pid))
        if pid:
            # 获取所有进程pid
            running_pids = psutil.pids()
            if pid in running_pids:
                print('程序正在运行中!')
                return True
            else:
                self.write()
                print('程序没有运行，启动中!')
                return False
        else:
            self.write()
            print('程序没有运行，启动中!')
            return False

    def kill(self):
        """
        杀死进程
        :return:
        """
        command = 'taskkill /F /IM python.exe'
        os.system(command)


if __name__ == '__main__':
    # wechat = WeChatSpider()
    # wechat.run()
    # with open('ExportFile/ContentValidation.txt', 'w') as f:
    #     f.seek(0)
    #     f.truncate()
    #     print('获取记录清空成功')
    # 监测程序是否在运行中
    monitor = Monitor()
    if monitor.run():
        os._exit(0)
    start_time = datetime.datetime.now()
    print("程序开始时间：{}".format(start_time))
    count = 0
    while True:
        try:
            wechat = WeChatSpider()
            wechat.run()
            with open('ExportFile/FriendValidation.txt', 'w') as f:
                f.seek(0)
                f.truncate()
                print('获取记录清空成功')
            if wechat.bottom:
                continue

        except Exception as e:
            # log = log_init()
            # log.info(e)
            count += 1
            continue
    #
    # end_time = datetime.datetime.now()
    # print('程序异常次数：{}'.format(count))
    # print("程序结束时间：{}".format(end_time))
    # print("程序执行用时：{}s".format((end_time - start_time)))


