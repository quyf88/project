import re
import os
import csv
import shutil
import datetime
import requests
from PIL import Image
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Spider:
    def __init__(self):
        chrome_options = Options()
        # keep_alive 设置浏览器连接活跃状态
        desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
        desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        prefs = {"profile.managed_default_content_settings.images": 1}  # 1 加载图片 2不加载图片,加快访问速度
        chrome_options.add_experimental_option("prefs", prefs)
        # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 有界面模式
        self.driver = webdriver.Chrome(chrome_options=chrome_options, keep_alive=False)
        # 隐形等待时间
        self.wait = WebDriverWait(self.driver, 10, 0.5)
        # 浏览器窗口最大化
        self.driver.maximize_window()
        # 文件名
        self.file_name = None

    def get_code(self):
        """
        筛选所在地区数据获取url
        :return:
        """
        url = 'https://www.landchina.com/default.aspx?tabid=263&ComName=default&tdsourcetag=s_pcqq_aiomsg'
        self.driver.get(url)
        name = input('筛选数据：')
        # 获取页数
        page_num = self.driver.find_element_by_css_selector('.pager .pager:nth-child(1)')
        print(page_num.text)
        page_num = re.findall(r'共(.*?)页', page_num.text)[0]
        page_num = 200 if int(page_num) > 200 else page_num
        print(page_num)
        for num in range(2, int(page_num)+2):
            # print('第：{}页数据获取中'.format(num-1))
            # 定位到数据标签
            res = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="TAB_contentTable"]')))
            # 提取出数据标签
            html = res.get_attribute('innerHTML')

            # 获取详情url
            urls = re.findall(r'href="(.*?)"', html, re.S | re.M)
            urls = [i.replace('amp;', '') for i in urls]
            # yield urls
            with open(name+'.txt', 'a+', encoding='utf-8') as f:
                for i in urls:
                    url = 'https://www.landchina.com/' + i
                    f.write(url)
                    f.write('\n')
                print('第：{}页url保存成功'.format(num - 1))
            # 页面跳转
            inpu = self.driver.find_element_by_css_selector('a+ input')
            inpu.clear()
            inpu.send_keys(num)
            enter = self.driver.find_elements_by_xpath('//input[contains(@value,"go")]')
            enter[0].click()

        self.driver.quit()

    def get_html(self, file_name):
        count = 1
        try_count = 1
        with open(file_name, 'r') as f:
            for url in f.readlines():
                try:
                    self.driver.get(url)
                    r = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="p1"]'))).text
                    r = r.replace('\n', '').replace(' ', '')
                except:
                    if try_count > 5:
                        self.driver.quit()
                        os._exit(0)
                    print('出错')
                    try_count += 1
                    continue
                # 行政区域
                regions = re.findall(
                    '行政区:(.*?)电子监管号', r)[0]
                # 项目名称
                name = re.findall(r'项目名称:(.*?)项目位置', r)[0]
                # 项目位置
                position = re.findall(r'项目位置:(.*?)面积', r)[0]
                # 土地用途
                use = re.findall(r'土地用途:(.*?)供地方式', r)[0]
                # 行业分类
                sort = re.findall(r'行业分类:(.*?)土地级别', r)[0]
                # 面积(公顷)
                area = re.findall(r'面积(.*?)土地来源', r)[0].replace('(公顷):', '')
                # 供地方式
                mode = re.findall(r'供地方式:(.*?)土地使用年限', r)[0]
                # 土地使用年限
                term = re.findall(r'土地使用年限:(.*?)行业分类', r)[0]
                # 成交价(万元)
                price = re.findall(r'成交价格(.*?)分期支付约定', r)[0].replace('(万元):', '')
                # 约定容积率
                agreement = re.findall(r'约定容积率:(.*?)约定交地时间', r)[0]
                # 合同签订日期
                contract_date = re.findall(r'合同签订日期:(.*?)$', r)[0]
                # 数据获取时间
                t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                url = url.replace('\n', '')
                data = [[regions, name, position, use, sort, area, mode, term, price, agreement, contract_date, url, t]]
                self.sav_data(data)
                print('第：[{}] 条数据保存成功'.format(count))
                count += 1
                # 备份
                shutil.copy(self.file_name, '备份数据.xlsx')

    def sav_data(self, data):
        """
        保存数据
        :return:
        """
        with open(self.file_name, "a+", encoding='utf-8', newline="") as f:
            k = csv.writer(f, delimiter=',')
            with open(self.file_name, "r", encoding='utf-8', newline="") as f1:
                reader = csv.reader(f1)
                if not [row for row in reader]:
                    k.writerow(['行政区域', '项目名称', '项目位置', '土地用途', '行业分类', '面积(公顷)', '供地方式', '土地使用年限', '成交价(万元)', '约定容积率', '合同签订日期', '数据来源', '数据写入日期'])
                    k.writerows(data)
                else:
                    k.writerows(data)

    def run(self):
        path = os.getcwd()
        files = os.listdir(path)
        files = [i for i in files if 'txt' in i if '备份数据' not in i]
        print(files)
        for file_name in files:
            print(file_name)
            (filename, extension) = os.path.splitext(file_name)
            self.file_name = filename + '.csv'
            print('新文件名：{}'.format(self.file_name))
            self.get_html(file_name)
            # 移动已处理完文件
            shutil.move(self.file_name, '完成/')
            os.remove(file_name)
            print('文件：{} 保存成功!'.format(self.file_name))

# def get_html():
#     """
#     获取详情页数据
#     :return:
#     """
#     headers = {'User-Agent': str(UserAgent().random),
#                'Connection': 'keep-alive',
#                'Host': 'www.landchina.com',
#                'Cookie': 'security_session_verify=635b63ed9e3ccba75b7d623780ad89ad; security_session_mid_verify=8963be16d687a59e3e05151b02af48a6; ASP.NET_SessionId=oytra2mgxsgxpc0x3tdieiy5; Hm_lvt_83853859c7247c5b03b527894622d3fa=1566871818; Hm_lpvt_83853859c7247c5b03b527894622d3fa=1566876411'
#                }
#     with open('上海url.txt', 'r') as f:
#         for url in f.readlines():
#             print(url)
#             response = requests.get(url, headers=headers)
#             print(response.status_code)
#             result = re.findall(r'供地结果信息', response.text)
#             if len(result):
#                 print(response.text)
#                 exit()
#             else:
#                 print(1)
#                 continue


if __name__ == '__main__':
    spider = Spider()
    spider.run()
    # spider.get_code()
