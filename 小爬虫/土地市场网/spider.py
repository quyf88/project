import re
import time
import requests
from PIL import Image
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC


class Spider:
    def __init__(self):
        # selenium无界面模式
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # keep_alive 设置浏览器连接活跃状态
        # 有界面模式
        self.driver = webdriver.Chrome(chrome_options=chrome_options, keep_alive=False)
        # 隐形等待时间
        self.wait = WebDriverWait(self.driver, 10, 0.5)
        # 浏览器窗口最大化
        self.driver.maximize_window()

    def get_code(self):
        """
        指定元素 截屏
        selenium 截屏方法
        get_screenshot_as_file() 获取当前window的截图
        save_screenshot() 获取屏幕截图
        :return:
        """
        url = 'https://www.landchina.com/default.aspx?tabid=263&ComName=default&tdsourcetag=s_pcqq_aiomsg'
        self.driver.get(url)
        time.sleep(3)

        res = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="TAB_contentTable"]')))
        # print(res.text)
        resp = res.get_attribute('innerHTML')
        print(resp)
        # 获取页数
        page_num = self.driver.find_element_by_css_selector('.pager .pager:nth-child(1)')
        print(page_num.text)
        page_num = re.findall(r'共(.*?)页', page_num.text)[0]
        print(page_num)

        # 页面跳转
        inpu = self.driver.find_element_by_css_selector('a+ input')
        inpu.clear()
        inpu.send_keys(2)
        enter = self.driver.find_elements_by_xpath('//input[contains(@value,"go")]')
        enter[1].click()

        # ur = 'https://www.landchina.com/default.aspx?tabid=386&comname=default&wmguid=75c72564-ffd9-426a-954b-8ac2df0903b7&recorderguid=9084DAD1502E61D7E055000000000001'
        # self.driver.get(ur)
        # time.sleep(1)
        # r = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="p1"]'))).text
        # print(r)
        # # with open('content.html', 'w', encoding='gbk') as f:
        # #     f.write(resp)
        # #     print('数据查询成功，读取中...')




if __name__ == '__main__':
    spider = Spider()
    spider.get_code()

