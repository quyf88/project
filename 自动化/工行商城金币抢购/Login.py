# -*- coding: utf-8 -*-
# @Time    : 2019/6/17 8:47
# @Author  : project
# @File    : Login.py
# @Software: PyCharm
import re
import os
import ssl
import time
import logging
import urllib3
import requests
import openpyxl
import configparser
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

urllib3.disable_warnings()


class Spider(object):
    def __init__(self):
        # 初始化log模块
        self.log = self.init_log()
        # cookies
        self.cookie = ''

        # __browser_url = r'C:\Users\Administrator\AppData\Roaming\360se6\Application\360se.exe'
        # chrome_options = Options()
        # chrome_options.binary_location = __browser_url
        # self.driver = webdriver.Chrome(chrome_options=chrome_options)


        self.driver = webdriver.Ie()
        self.wait = WebDriverWait(self.driver, 30, 0.5)
        self.driver.maximize_window()

    def init_log(self):
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

    def login_by_scan(self):
        self.log.info("开始登录,请等待页面加载完成后,登录...")
        self.driver.get('https://login.mall.icbc.com.cn/login')
        while True:
            # current_url 获取当前页面url
            if 'login.mall.icbc.com.cn' not in self.driver.current_url:
                self.log.info("登录成功")
                break
            else:
                self.log.info("等待登录中...")
                time.sleep(5)

    def get_token(self):

        time.sleep(5)
        self.driver.get('https://mall.icbc.com.cn/products/pd_9000874368.jhtml')
        standard = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="img_sku"]/em')))

        if len(standard):
            standard[1].click()
        time.sleep(5)
        enit = self.wait.until(EC.presence_of_element_located((By.ID, 'buynow')))
        enit.click()
        # html = self.driver.page_source.replace(' ', '').replace("'", '"')

        # print(html)
        # 获取登录成功后cookie
        # for k in self.driver.get_cookies():
        #     self.cookie += '{}={}; '.format(k['name'], k['value'])
        # print(self.cookie)

        # headers = {
        #     'user-agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        #
        #     'cookie': self.cookie
        # }
        # data = {
        #     'sleep': 0,
        #     'verifyCodeValue': '',
        #     'submitRequestStr': {"submitRequestOrders":[{"orderProdType":"2","logisticType":"10000000","deliveryType":"1","deliveryDateId":"3","isNeedReceipt":"1","invoiceTitleType":"0","invoiceTitle":"个人","invoiceContent":"0000000501","invoiceType":"0","companyName":"","taxpayerId":"","registerAddress":"","registerTel":"","depositBank":"","bankAccount":"","fulfilPromotionId":"","freePostPromotionId":"","freePostFreight":"0","orderMemberMemo":"","minsNum":"","selectCouponIds":"","refundCouponAmount":"0","selectVendorCouponIds":"","refundVendorCouponAmount":"0","consigneeName":"","idCardNum":"","consigneeMobile":"","consigneeEmail":"","merDefines":"{\"merDefined1\":\"\",\"merDefined2\":\"\",\"merDefined3\":\"\"}","consigneeTelephone":"","mobileChannelDetail":"","ifGiveInsu":"","storeVO":{"mercId":"10002377","storeId":"011385","storeName":"工银金行家直营店","prodType":"2","orderProductMaxCount":"","isSupportOverseas":"","logstorId":"","shjdMode":"","orderKey":"","prods":[{"prodId":"9000874368","prodChannelType":"","mercProdId":"","prodName":"2019年中国北京世界园艺博览会贵金属纪念币","finaProdType":"2","prodStat":"0","skuId":"90000000000019634871","weight":"0","volume":"0","skuInfo":"规格:30克银币单枚装","originPrice":"590.00","price":"590","currType":"001","count":"1","prodImg":"https://image6.mall.icbc.com.cn/oaasImage/10002377/0/1557364288067_2.jpg","promSerial":"9bef27df-735d-47fa-b97a-9f7c3c0b695a","promId":"201906149087096","promType":"14","addTime":"","tringKey":"90000000000019634871","trings":[],"gifts":[],"logstId":"","areaId":"110106","maxBuyNum":"","prodStorage":"","balanceType":"","isDelivery":"","shippingTemplatesID":"","salesType":"","prodKey":"","prodPrvId":"","prodFlag":"","orderKey":"","futuresInfoYear":"","futuresInfoNum":""}],"returnFlag":"0"},"isIntegralOrder":"false","useIntegralOrder":"0","useIntegralAmountOrder":"0.00","areaCode":"","brCode":"","dataId":"","saleCode":"","recommendType":""}],"paymentType":"01","consigneeId":"900009541264","orderCreateType":"01","isIntegral":"false","useIntegral":"0","useIntegralAmount":"0.00","integralRate":"0","isHandDiscount":"0","prodTakeAddressId":"110106","channelSeq":"","logStartTime":"1560746058937","flashSaleSecret":"12449e4b-e7cc-42e2-b65e-751506d6fb1d"},
        #     'struts.token.name': 'tokenCommit',
        #     'tokenCommit': '330OU11SJKEZHRM5O995RZOOCT3WAE5T'
        # }
        # url = 'https://mall.icbc.com.cn/order/createOrder.jhtml'
        #
        # res1 = requests.post(url, data=data, headers=headers, verify=False)
        # html = res1.text
        #
        # print(1)
        # print(res1)
        # print(res1.cookies)
        # print(2)
        # print(html)





if __name__ == '__main__':
    bot = Spider()
    bot.login_by_scan()
    bot.get_token()