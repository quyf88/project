# coding=utf-8
# 作者    ： Administrator
# 文件    ：spider.py
# IED    ：PyCharm
# 创建时间 ：2019/8/10 14:07
import csv
import sys
import time
import requests
import pytesseract
import pandas as pd
from PIL import Image
from lxml import etree
# from aip import AipOcr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import fateadm_api
from read_code import Code


class Spider:
    def __init__(self):
        print('-----程序启动中...-----')
        # selenium无界面模式
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        # keep_alive 设置浏览器连接活跃状态
        # self.driver = webdriver.Chrome(chrome_options=chrome_options, keep_alive=False)
        print('-----程序启动成功-----')
        # 有界面模式
        self.driver = webdriver.Chrome(keep_alive=False)
        # 隐形等待时间
        self.wait = WebDriverWait(self.driver, 10, 0.5)
        # 浏览器窗口最大化
        self.driver.maximize_window()
        url = 'http://tyrz.gdbs.gov.cn/am/login/initAuth.do?gotoUrl=http%3A%2F%2Ftyrz.gdbs.gov.cn%2Fam%2Foauth2%2Fauthorize%3Fclient_id%3Dszjxgcxt%26service%3DinitService%26scope%3Dall%26redirect_uri%3Dhttps%253A%252F%252Famr.sz.gov.cn%252Fpsout%252Fjsp%252Fgcloud%252Fpubservice%252Fuserstsso%252Fgodeal.jsp%26response_type%3Dcode'
        self.driver.get(url)
        # 保存数据
        self.load_list = []

    def login(self):
        """登录"""
        print('账号登录中...')
        username = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#loginName')))
        username.send_keys('wyn16888')
        password = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#loginPwd')))
        password.send_keys('wyn16888')
        self.get_code_image(True)
        code = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tempValidateCode')))
        spot_code = self.spot_code()
        # print('验证码：{}'.format(spot_code))
        code.send_keys(spot_code)
        enter = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#userLoginBtn')))
        enter.click()
        print('账号：wyn16888 登录成功')

    def get_code_image(self, login):
        """
        获取验证码图片
        指定元素 截屏
        selenium 截屏方法
        get_screenshot_as_file() 获取当前window的截图
        save_screenshot() 获取屏幕截图
        :return:
        """
        # 当前浏览器屏幕截图
        self.driver.save_screenshot('./code/button.png')
        if login:
            # 登录页面 定位需要截图的元素
            element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#codeIm')))
            # print(element.location)  # 打印元素坐标
            # print(element.size)  # 打印元素大小
            # 构造元素坐标
            left = element.location['x']
            top = element.location['y']
            right = element.location['x'] + element.size['width']
            bottom = element.location['y'] + element.size['height']
        else:
            # 查询页面
            left = 820
            top = 510
            right = 910
            bottom = 545

        # 根据坐标位置拷贝
        im = Image.open('./code/button.png')
        im = im.crop((left, top, right, bottom))
        im.save('./code/code.png')

    def spot_code(self, balances=False):
        """
        验证码识别
        balances 查询余额
        :return:
        """
        # 斐斐打码
        # print('---验证码识别中---')
        count = 1
        while True:
            if balances:
                balance = fateadm_api.TestFunc(balances=True)
                if balance < 1000:
                    print('余额不足及时充值：{}'.format(balance))
                elif balance < 100:
                    print('余额严重不足即将不能使用：{}'.format(balance))
                elif balance < 10:
                    print('*' * 30)
                    print('余额不足,请充值：{}'.format(balance))
                    print('*' * 30)
                    sys.exit()
                return print('打码平台余额：{}'.format(balance))
            rsp = fateadm_api.TestFunc()
            if count > 3:
                print('验证码识别失败! 请联系开发者')
                sys.exit()
            if not rsp.pred_rsp.value:
                count += 1
                continue
            return rsp.pred_rsp.value

    def get_phone(self, pre_name, pre_code, pre_type):
        """获取账号登录状态"""
        while True:
            # 填写请求信息
            time.sleep(3)
            self.driver.get('https://amr.sz.gov.cn/aicmerout/jsp/gcloud/giapout/industry/aicmer/processpage/step_one.jsp?ywType=30')
            num = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#regno')))
            num.send_keys(pre_code)
            name = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#entNa')))
            name.send_keys(pre_name)
            self.get_code_image(False)
            code = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#validCode')))
            spot_code = self.spot_code()
            print('验证码：{}'.format(spot_code))
            code.send_keys(spot_code)
            # code.send_keys(input('输入验证码: '))
            enter = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.btn-primary')))[0]
            enter.click()

            # 处理弹窗
            time.sleep(3)
            # 切换iframe 弹窗
            try:
                ups_iframe = self.driver.find_element_by_css_selector('.layui-layer-content > iframe')
                self.driver.switch_to.frame(ups_iframe)
                confirmBtn = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#confirmBtn')))
                confirmBtn.click()
            except:
                print('验证码错误')
                continue

            # 提取数据
            time.sleep(10)
            print('睡眠10秒,防止封IP或网络加载问题')
            # 切换详细信息 iframe
            detail_iframe = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#formRender')))
            self.driver.switch_to.frame(detail_iframe)
            if pre_type in '个体工商户':
                # 个体户
                JingYingZhe = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="JingYingZhe_GtBg"]/div[1]/div')))
                JingYingZhe.click()
                FamilyMem = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="FamilyMem_Bg"]/div[1]/div')))
                FamilyMem.click()
                phone = self.process_phone(True)
                return phone
            elif pre_type in '有限责任公司(自然人独资)':
                # 公司
                Farendaibiao = self.driver.find_element_by_xpath('//*[@id="FaDingDaiBiaoRenXinXi"]/div')
                Farendaibiao.click()
                guquanbiangeng = self.driver.find_element_by_xpath('//*[@id="GQBGHGZS"]/div')
                guquanbiangeng.click()
                phone = self.process_phone(False)
                return phone

    def process_phone(self, pre_type):
        """
        处理手机号图片
        指定元素 截屏
        selenium 截屏方法
        get_screenshot_as_file() 获取当前window的截图
        save_screenshot() 获取屏幕截图
        :return:
        """
        # 当前浏览器屏幕截图
        self.driver.save_screenshot('./code/phone_page.png')
        # 根据坐标位置拷贝
        im = Image.open('./code/phone_page.png')
        if pre_type:
            im = im.crop((310, 100, 660, 130))
        else:
            im = im.crop((310, 160, 500, 185))
        im.save('./code/phone.png')
        print('成功获取手机号图片')
        img = Image.open('code/phone.png')
        phone = pytesseract.image_to_string(img)
        print('成功获取手机号：{}'.format(phone))
        return phone

    def read_xls(self):
        """
        读取 XLS表格数据
        :return:
        """
        # 加载数据
        df_read = pd.read_excel(r'ceshi111.xlsx.xlsx')
        df = pd.DataFrame(df_read)
        # keys = ['企业名称', '省份', 'l联系电话', '城市', '统一社会信用代码', '法定代表人', '企业类型', '成立日期',
        #         '成立日期', '地址', '邮箱', '经营范围', '网址', '电话号码', '电话号码（更多号码）']
        pre_names = df['企业名称']
        pre_codes = df['统一社会信用代码']
        pre_privinces = df['所属省份']
        pre_citys = df['所属城市']
        pre_persons = df['法定代表人']
        pre_types = df['企业类型']
        pre_datas = df['成立日期']
        pre_prices = df['注册资本']
        pre_addresss = df['企业地址']
        pre_ranges = df['经营范围']
        # pre_site=df['网址']
        for pre_name, pre_privince, pre_code, pre_city, pre_person, pre_type, pre_data, pre_price, pre_address, pre_range in zip(
                pre_names, pre_privinces, pre_codes, pre_citys, pre_persons, pre_types, pre_datas, pre_prices,
                pre_addresss, pre_ranges):
            pre_base = {}
            pre_base['企业名称'] = pre_name
            pre_base['省份'] = pre_privince
            pre_base['城市'] = pre_city
            pre_base['统一社会信用代码'] = pre_code
            pre_base['法定代表人'] = pre_person
            pre_base['企业类型'] = pre_type
            pre_base['成立日期'] = pre_data
            pre_base['注册资本'] = pre_price
            pre_base['地址'] = pre_address
            pre_base['经营范围'] = pre_range
            yield pre_base

    def save(self):
        df = pd.DataFrame(self.load_list)
        df.to_excel('{}'.format('a.xlsx'), sheet_name='data')
        print('end!')

    def run(self):
        self.login()
        datas = spider.read_xls()
        for query_data in datas:
            # print(query_data)
            pre_name = query_data['企业名称']
            pre_code = query_data['统一社会信用代码']
            pre_type = query_data['企业类型']
            print(pre_name, pre_code, pre_type)
            # 获取信息提取手机号
            phone = self.get_phone(pre_name, pre_code, pre_type)
            query_data['联系方式'] = phone
            self.load_list.append(query_data)

        self.save()


if __name__ == '__main__':
    spider = Spider()
    spider.run()
