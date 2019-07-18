import csv
import time
import datetime
from PIL import Image
from lxml import etree
from aip import AipOcr
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import fateadm_api


class Spider:
    def __init__(self):
        print('-----程序启动中...-----')
        # selenium无界面模式
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        # keep_alive 设置浏览器连接活跃状态
        # self.driver = webdriver.Chrome(chrome_options=chrome_options, keep_alive=False)
        print('-----程序成功启动-----')
        # 有界面模式
        self.driver = webdriver.Chrome(keep_alive=False)
        # 隐形等待时间
        self.wait = WebDriverWait(self.driver, 30, 0.5)
        # 浏览器窗口最大化
        self.driver.maximize_window()

    def read_file(self):
        """
        读取域名文件
        :return: 域名列表
        """
        print('读取域名文件....')
        with open('data.txt', 'r') as f:
            data = f.read()
        return data

    def spot_code(self):
        """
        验证码识别
        :return:
        """
        # 斐斐打码
        print('识别验证码中...')
        rsp = fateadm_api.TestFunc()
        return rsp.pred_rsp.value
        # 百度AI
        # APP_ID = '16834554'
        # API_KEY = 'Tg7ljO6PfpZudhYo2ZyhssTu'
        # SECRET_KEY = 'k3tSLgYSOR4yij3vzhdzFqUXeDAqVBev'
        #
        # client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        #
        # """ 读取图片 """
        # def get_file_content(filePath):
        #     with open(filePath, 'rb') as fp:
        #         return fp.read()
        #
        # image = get_file_content('./code/code.png')
        #
        # """ 调用通用文字识别（高精度版） """
        # res = client.basicAccurate(image)
        # print(res)

        # """ 如果有可选参数 """
        # options = {}
        # options["detect_direction"] = "true"
        # options["probability"] = "true"
        #
        # """ 带参数调用通用文字识别（高精度版） """
        # client.basicAccurate(image, options)

    def get_code(self):
        """
        指定元素 截屏
        selenium 截屏方法
        get_screenshot_as_file() 获取当前window的截图
        save_screenshot() 获取屏幕截图
        :return:
        """
        url = 'http://www.chaicp.com/piliang.html#first'
        self.driver.get(url)
        time.sleep(1)
        # 当前浏览器屏幕截图
        self.driver.save_screenshot('./code/button.png')
        # 定位需要截图的元素
        element = self.driver.find_element_by_xpath('//span[@class="Code-m"]')
        # print(element.location)  # 打印元素坐标
        # print(element.size)  # 打印元素大小
        # 构造元素坐标
        left = element.location['x']
        top = element.location['y']
        right = element.location['x'] + element.size['width']
        bottom = element.location['y'] + element.size['height']
        # 根据坐标位置拷贝
        im = Image.open('./code/button.png')
        im = im.crop((left, top, right, bottom))
        im.save('./code/code.png')
        print('获取验证码成功')

    def get_content(self):
        """
        请求数据
        :return:
        """
        while True:
            # 查询网址
            a = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="search"]/textarea')))
            a.click()
            data = self.read_file()
            a.send_keys(data)
            print('域名写入成功')
            # 验证码
            b = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="Code verify clear"]/input')))
            b.click()
            code = self.spot_code()
            b.clear()
            b.send_keys(code)
            print('验证码写入成功')
            # 查询 无界面模式下定位到元素无法点击 用Keys.ENTER 代替
            c = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="search"]/button')))
            c.send_keys(Keys.ENTER)
            print('提交请求,获取数据中...')

            # 判断验证码是否输入正确
            time.sleep(1)
            code_status = self.driver.find_element_by_xpath('//div[@class="content"]')
            response = code_status.get_attribute('innerHTML')
            if len(response):
                print('错误代码：{}'.format(response))
                # 刷新页面
                self.driver.refresh()
                continue
            print('验证码输入正确,验证成功')
            break

    def get_html(self):
        """
        获取查询后的HTML页面 保存到本地
        :return:
        """
        time.sleep(1)
        # 判断是否请求成功数据
        res = self.driver.find_elements_by_xpath('//div[@class="pl-main"]')
        if not len(res):
            print('数据查询失败')
            return

        self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="search"]/button')))
        # page_source 获取网页源码 加等待时间防止页面刷新不出来
        # response = self.driver.page_source
        # get_attribute('innerHTML') 获取指定元素源代码
        response = res[0].get_attribute('innerHTML')
        # 源代码保存为本地HTML文件
        with open('content.html', 'w', encoding='gbk') as f:
            f.write(response)
            print('数据查询成功，读取中...')

    def deal_html(self):
        """
        从html文件中读取数据 保存至文件
        :return:
        """
        with open('content.html', 'r', encoding='GBK') as f:
            a = f.read()
        result = etree.HTML(a)
        tbody_list = result.xpath('//tbody/tr')
        count = 1
        for tbody in tbody_list:
            # 主办单位
            organizer = tbody.xpath('./td[1]/text()')[0]
            # 单位性质
            software = [tbody.xpath('./td[2]/text()') if len(tbody.xpath('./td[2]/text()')) else '- -'][0]
            # 许可证号
            licenses = tbody.xpath('./td[3]/text()')[0]
            # 网站名称
            assemname = tbody.xpath('./td[4]/text()')[0]
            # 网址
            url = tbody.xpath('./td[5]/span/a/text()')[0]
            # 审核时间
            reviewtime = tbody.xpath('./td[6]/text()')[0]
            # 写入时间
            writertime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            data = ([[organizer, software, licenses, assemname, url, reviewtime, writertime]])

            with open("demo.csv", "a+", encoding='utf-8', newline="") as f:
                k = csv.writer(f, delimiter=',')
                with open("demo.csv", "r", encoding='utf-8', newline="") as f1:
                    reader = csv.reader(f1)
                    if not [row for row in reader]:
                        k.writerow(['主办单位', '单位性质', '许可证号', '网站名称', '网站首页网址', '审核时间', '写入时间'])
                        k.writerows(data)
                        print('第[{}]条数据插入成功'.format(count))
                    else:
                        k.writerows(data)
                        print('第[{}]条数据插入成功'.format(count))
            count += 1

    def run(self):
        start_time = datetime.datetime.now()
        print("程序开始时间：{}".format(start_time))
        self.get_code()
        self.get_content()
        self.get_html()
        self.deal_html()
        end_time = datetime.datetime.now()
        print("程序结束时间：{}".format(end_time))
        print("程序执行用时：{}s".format((end_time - start_time)))


if __name__ == '__main__':
    spider = Spider()
    spider.run()

