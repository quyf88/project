#!/usr/bin/env python
# -*- coding: utf-8 -*-
__version__ = '1.0.0.0'
import os
import sys
import csv
import time
import requests
from imp import reload
from aip import AipSpeech
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urlencode
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

reload(sys)
keywords = '肇庆服装'


class Spider:
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 60)
        self.browser.maximize_window()

    def get_info(self):
        pass

    def quit(self):
        self.browser.close()

    def _getdriverpath(self):
        # path = os.path.join(os.path.split(__file__)[0], "phantomjs.exe")
        # path = os.path.join(os.path.split(__file__)[0], "chromedriver.exe")
        path = "C://chromedriver.exe"
        return path


class SpiderAliShop(Spider):
    def __init__(self):
        super(SpiderAliShop, self).__init__()
        self.login_url = "https://login.taobao.com/member/login.jhtml"
        self.browser.get(self.login_url)
        self.cookie = {}
        self.count = 0

    def aipspeech(self):
        """ 18210836362 你的 APPID AK SK """
        APP_ID = '15434389'
        API_KEY = 'LwmLHenAnw8ku15M75XCmQBq'
        SECRET_KEY = 'RdNdVyolT8XZ1wtEA2SZO59REDhodpcc'

        client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
        try:
            # 合成
            result = client.synthesis('死骗子快点给钱', 'zh', 1, {
                'vol': 5,
            })

            # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
            if not isinstance(result, dict):
                return True
                # with open('auido.mp3', 'wb') as f:
                #     f.write(result)
            else:
                print('程序运行错误,联系开发者!!!')
                os._exit(0)
        except:
            print('程序运行错误,联系开发者!!!')
            os._exit(0)

    def wait_login(self):
        # 扫码登录
        # while True:
        #     if 'data' in self.browser.current_url:
        #         print("等待扫码中...")
        #         time.sleep(5)
        #     if 'login.taobao.com' not in self.browser.current_url:
        #         print("登录成功")
        #         break
        #     else:
        #         print("等待扫码中...")
        #         time.sleep(5)
        """
        微博登录
        :return:
        """
        weibo_username = "18210836362"  # 改成你的微博账号
        weibo_password = "chenxiaoli2013"  # 改成你的微博密码
        # 等待 密码登录选项 出现
        password_login = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.qrcode-login > .login-links > .forget-pwd')))
        password_login.click()

        # 等待 微博登录选项 出现
        weibo_login = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.weibo-login')))
        weibo_login.click()

        # 等待 微博账号 出现
        weibo_user = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.username > .W_input')))
        weibo_user.send_keys(weibo_username)

        # 等待 微博密码 出现
        weibo_pwd = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.password > .W_input')))
        weibo_pwd.send_keys(weibo_password)

        # 等待 登录按钮 出现
        submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.btn_tip > a > span')))
        submit.click()
        while True:
            if 'login.taobao.com' not in self.browser.current_url:
                print("登录成功")
                # 直到获取到淘宝会员昵称才能确定是登录成功
                taobao_name = self.wait.until(EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    '.site-nav-bd > ul.site-nav-bd-l > li#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-user > a.site-nav-login-info-nick ')))
                # 输出淘宝昵称
                print('账号：{}登录成功'.format(taobao_name.text))
                break
            else:
                print("等待登录中...")
                time.sleep(5)
                continue

    def scv_data(self, data):
        """保存为csv"""
        self.count += 1
        with open(f"{keywords}.csv", "a+", encoding='utf-8', newline="") as f:
            k = csv.writer(f, delimiter=',')
            with open(f"{keywords}.csv", "r", encoding='utf-8', newline="") as f1:
                reader = csv.reader(f1)
                if not [row for row in reader]:
                    k.writerow(['企业名称', '主页', '联系人', '电话', '地址'])
                    k.writerows(data)
                    print('第[{}]条数据插入成功'.format(self.count))
                else:
                    k.writerows(data)
                    print('第[{}]条数据插入成功'.format(self.count))

    def get_data(self):
        self.wait_login()
        # 爬去url
        url = 'https://s.1688.com/company/company_search.htm?'  # keywords=%BA%EC%C5%A3&=top&earseDirect=false&n=y'
        params = {"keywords": keywords.encode('GBK'), "button_click": "top", "earseDirect": "false", "n": "y"}
        self.browser.get(url + urlencode(params))
        i = 1
        while i < 100:
            js = 'var q=document.documentElement.scrollTop=25000'
            self.browser.execute_script(js)
            try:
                print("...........................")

                time.sleep(1)
                # 取标题
                bs = BeautifulSoup(self.browser.page_source, "html.parser")
                a_obj = bs.select('a.list-item-title-text')
                for item in a_obj:
                    href_value = item.attrs["href"]
                    print(href_value)
                    # 组建头部
                    headers = {
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                        "Accept-Encoding": "gzip, deflate, sdch, br",
                        "Accept-Language": "zh-CN,zh;q=0.8",
                        "Referer": href_value,
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
                    }
                    title_value = item.text
                    response = requests.get(href_value, headers=headers, cookies=self.cookie)
                    bs2 = BeautifulSoup(response.text, "html.parser")
                    # contact_li_a_obj = bs2.select('li.contactinfo-page a')[0].attrs["href"]
                    contact_li_a_obj = href_value+"/page/contactinfo.htm"

                    headers = {
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                        "Accept-Encoding": "gzip, deflate, sdch, br",
                        "Accept-Language": "zh-CN,zh;q=0.8",
                        "Referer": contact_li_a_obj,
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
                    }
                    response2 = requests.get(contact_li_a_obj, headers=headers, cookies=self.cookie)
                    bs3 = BeautifulSoup(response2.text, "html.parser")
                    if bs3.select(".m-mobilephone dd"):
                        tel = bs3.select(".m-mobilephone dd")[0].text.strip()
                        if tel == '登录后可见':
                            tel = ''
                    else:
                        tel = ''
                    if not tel:
                        continue
                    if bs3.select(".address .disc"):
                        address = bs3.select(".address ")[0].text.replace(u"所在地区：", "").strip()
                    else:
                        address = ''
                    if bs3.select("a.membername"):
                        person = bs3.select("a.membername")[0].text.strip()
                    else:
                        person = ''
                    print("%s,%s,%s,%s" % (title_value, tel, person, address))
                    data = [[title_value, href_value, person, tel, address]]
                    self.scv_data(data)
            except Exception as e:
                print(e)
                print(self.browser.current_url)
                if 'https://login' in self.browser.current_url:
                    self.wait_login()
                else:
                    try:
                        print('next')
                        page = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.page-next')))[0]
                        page.click()
                    except Exception as e:
                        print(e)
                        self.browser.refresh()
                i += 1


if __name__ == '__main__':
    spider = SpiderAliShop()
    if spider.aipspeech():
        spider.get_data()

