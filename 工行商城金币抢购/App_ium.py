# -*- coding: utf-8 -*-
# @Time    : 2019/6/6 9:58
# @Author  : project
# @File    : App_ium.py
# @Software: PyCharm

import time
from datetime import datetime
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support import expected_conditions as EC
"""融e购商城"""


def run_time(func):
    def new_func(*args, **kwargs):
        start_time = datetime.now()
        print("程序开始时间：{}".format(start_time))
        func(*args, **kwargs)
        end_time = datetime.now()
        print("程序结束时间：{}".format(end_time))
        print("程序执行用时：{}s".format((end_time - start_time)))

    return new_func


class PanicBuying:
    def __init__(self):
        desired_caps = {
                      "automationName": "uiautomator2",  # 引擎
                      "platformName": "Android",
                      "deviceName": "127.0.0.1:62001",
                      "appPackage": "com.icbc.emallmobile",
                      "appActivity": "com.icbc.ui.activiy.WelcomePageActivity",
                      "noReset": True,
                      "platformVersion": "5.1.1"  # 模拟器版本号
                    }
        driver_server = 'http://127.0.0.1:4723/wd/hub'
        print('APP启动...')
        # 启动APP
        self.driver = webdriver.Remote(driver_server, desired_caps)
        # 设置等待
        self.wait = WebDriverWait(self.driver, 30, 0.5)

    def h5_cutover(self, h5=None):
        """
        页面切换
        WEBVIEW_com.icbc.emallmobile 商品详情页
        WEBVIEW_com.vphone.launcher 订单确认页
        :param h5: 1：商品列表 2：提交订单 3：原生页面
        :return: None
        """
        if h5 == 1:
            self.driver.switch_to.context('WEBVIEW_com.icbc.emallmobile')
            print('切换至H5 商品列表：{}页面'.format(self.driver.current_context))
        elif h5 == 2:
            self.driver.switch_to.context('WEBVIEW_com.vphone.launcher')
            print('切换至H5 提交订单：{}页面'.format(self.driver.current_context))
        else:
            self.driver.switch_to.context("NATIVE_APP")
            print('切换至原生：{}页面'.format(self.driver.current_context))

    def postal_hall(self):
        """
        进入邮币馆主题页面
        :return:
        """
        time.sleep(5)
        print('加载广告')
        # 进入工银金行家
        secondary_page_xpath = '//*[@resource-id="com.icbc.emallmobile:id/ll_platform"]/android.widget.TableRow[1]/android.widget.LinearLayout[4]'
        secondary_page = self.wait.until(EC.presence_of_element_located((By.XPATH, secondary_page_xpath)))
        secondary_page.click()
        print("进入工银金行家页面")

        # 进入邮币馆
        postal_hall_id = 'com.icbc.emallmobile:id/sdv_ad'
        postal_hall = self.wait.until(EC.presence_of_element_located((By.ID, postal_hall_id)))
        postal_hall.click()
        print("进入邮币馆页面")

    def submit_order(self, column_id, commodity_ID, norm=None, amt=1):
        """
        商品详情页
        :param column_id: 栏目ID 1-5
        :param commodity_ID: 商品ID 1-N
        :norm  norm: 商品规格
        :amt  amt: 购买数量
        :return:
        """
        while True:
            # 切换至商品列表H5页面
            self.h5_cutover(1)
            # 进入商品详情页
            commodity_xpath = "//*[@id=\"sale{}\"]/ul/li[{}]".format(column_id, commodity_ID)
            commodity = self.wait.until(EC.presence_of_element_located((By.XPATH, commodity_xpath)))
            commodity.click()
            # 切换为原生状态
            self.h5_cutover(3)

            # 获取商品价格后再点击立即购买防止页面加载不出来
            try:
                # 正常价格
                price_id = 'com.icbc.emallmobile:id/goods_detail_price'
                price = WebDriverWait(self.driver, 3, 0.5).until(EC.presence_of_element_located((By.ID, price_id)))
                print("商品价格：{}".format(price.get_attribute("text")))
            except Exception as e:
                # 带下划线价格
                price_id = 'com.icbc.emallmobile:id/tv_time_detail_price'
                price = WebDriverWait(self.driver, 3, 0.5).until(EC.presence_of_element_located((By.ID, price_id)))
                print("商品价格：{}".format(price.get_attribute("text")))
            try:
                # 立即购买
                status_id = 'com.icbc.emallmobile:id/comm_right_to_buy_tv'
                status = self.wait.until(EC.presence_of_element_located((By.ID, status_id)))
                status.click()
                break
            except Exception as e:
                # 看相似 按钮
                # status_id = 'com.icbc.emallmobile:id/comm_look_others_tv'
                # status = WebDriverWait(self.driver, 3, 0.5).until(EC.presence_of_element_located((By.ID, status_id)))

                # 活动倒计时
                start_time = 'com.icbc.emallmobile:id/tv_start_time'
                start = self.wait.until(EC.presence_of_element_located((By.ID, start_time)))
                print("抢购暂未开始!", start.get_attribute("text"))
                # TODO 活动倒计时计算
                self.driver.keyevent(4)

                continue

        # 选择商品规格
        if norm:
            option_id = "com.icbc.emallmobile:id/radio_color"
            option_list = self.wait.until(EC.presence_of_all_elements_located((By.ID, option_id)))
            for option in option_list:
                print(option.get_attribute("text"))
                if option.get_attribute("text") == norm:
                    option.click()
                    break
                else:
                    continue

            # 购买数量
            amount_id = "com.icbc.emallmobile:id/text_number_count_view"
            amount = self.wait.until(EC.presence_of_element_located((By.ID, amount_id)))
            amount.clear()
            amount.send_keys(amt)

            # 立即购买
            popup_buy_id = "com.icbc.emallmobile:id/text_sku_gotobuy"
            popup_buy = self.wait.until(EC.presence_of_element_located((By.ID, popup_buy_id)))
            popup_buy.click()
        else:
            # 立即购买
            home_buy_id = "com.icbc.emallmobile:id/comm_right_to_buy_tv"
            home_buy = self.wait.until(EC.presence_of_element_located((By.ID, home_buy_id)))
            home_buy.click()
            print('点击立即购买')

    def confirm_order(self):
        # 切换至提交订单H5
        self.h5_cutover(2)
        print('访问太快出错，设置等待时间')
        # 发票信息填写
        # a_xpath = '//div[@class="cols011"]'
        # a_list = driver.find_elements_by_xpath(a_xpath)
        # a_list = wait.until(EC.presence_of_all_elements_located((By.XPATH, a_xpath)))
        # a_list[4].click()
        # 点击发票
        invoice = self.wait.until(EC.presence_of_element_located((By.ID, 'invoiceHeadCommit')))
        invoice.click()

        # 发票类型
        commoninvoice = self.wait.until(EC.presence_of_element_located((By.ID, 'commoninvoice')))
        commoninvoice.click()
        # 发票抬头
        personal = self.wait.until(EC.presence_of_element_located((By.ID, 'personal')))
        personal.click()
        # 发票内容
        invoiceDetail_xpath = '//div[@id="invoiceDetail"]/a'
        invoiceDetail = self.wait.until(EC.presence_of_element_located((By.XPATH, invoiceDetail_xpath)))
        invoiceDetail.click()
        # 确定按钮 following-sibling 定位兄弟元素
        xxx = "//div[@id='invoiceDetail']/following-sibling::div[1]/a/span"
        aaa = self.wait.until(EC.presence_of_element_located((By.XPATH, xxx)))
        aaa.click()

        # time.sleep(2)
        # # 提交订单
        # # submit_id = "submitOrderBtn"
        # # submit = wait.until(EC.presence_of_element_located((By.ID, submit_id)))
        # # submit.click()

    @run_time
    def run(self):
        self.postal_hall()
        self.submit_order(1, 9, '银币套（30克银*3）', 1)  # TODO 配置文件
        self.confirm_order()


if __name__ == '__main__':
    panic = PanicBuying()
    panic.run()



# 滑动屏幕
# touchaction = TouchAction(driver)
# touchaction.press(x=500, y=1500).move_to(x=500, y=200).wait(500).release().perform()

# 切换二级目录
# contents = '精品典藏'
# if contents == '新品尚新':
#     content_xpa = '//div[@class="icon-nav container"]/ul/li[1]'
#     content = wait.until(EC.presence_of_element_located((By.XPATH, content_xpa)))
#     content.click()
# elif contents == '精品典藏':
#     content_xpa = '//div[@class="icon-nav container"]/ul/li[2]'
#     content = wait.until(EC.presence_of_element_located((By.XPATH, content_xpa)))
#     content.click()
# elif contents == '热门币类':
#     content_xpa = '//div[@class="icon-nav container"]/ul/li[3]'
#     content = wait.until(EC.presence_of_element_located((By.XPATH, content_xpa)))
#     content.click()
# elif contents == '热门钞类':
#     content_xpa = '//div[@class="icon-nav container"]/ul/li[4]'
#     content = wait.until(EC.presence_of_element_located((By.XPATH, content_xpa)))
#     content.click()
# elif contents == '热门邮票':
#     content_xpa = '//div[@class="icon-nav container"]/ul/li[5]'
#     content = wait.until(EC.presence_of_element_located((By.XPATH, content_xpa)))
#     content.click()
# else:
#     print('目录不正确')

# 获取商品状态


        # 如果有规格选择商品规格
















