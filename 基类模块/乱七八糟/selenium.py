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
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        # keep_alive 设置浏览器连接活跃状态
        self.driver = webdriver.Chrome(chrome_options=chrome_options, keep_alive=False)
        # 有界面模式
        # self.driver = webdriver.Chrome(keep_alive=False)
        # 隐形等待时间
        self.wait = WebDriverWait(self.driver, 30, 0.5)
        # 浏览器窗口最大化
        # self.driver.maximize_window()

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
        print(element.location)  # 打印元素坐标
        print(element.size)  # 打印元素大小
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

    # def get_con(self):
    #     """
    #     请求数据
    #     :return:
    #     """
    #     headers = {"User-Agent": UserAgent().random}
    #     url = 'http://www.chaicp.com/home_cha/p_piliang'
    #     data = {
    #         'ym': 'jd.com',
    #         'code': input('验证码：')
    #     }
    #     res = requests.post(url, data=data, headers=headers, verify=False)
    #     print(res.text)

    def get_content(self):
        """
        请求数据
        :return:
        """
        while True:
            # 查询网址
            a = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="search"]/textarea')))
            a.click()
            a.send_keys('taobao.com')
            # 验证码
            b = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="Code verify clear"]/input')))
            b.click()
            code = input("验证码：")
            b.clear()
            b.send_keys(code)
            # 查询 无界面模式下定位到元素无法点击 用Keys.ENTER 代替
            c = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="search"]/button')))
            c.send_keys(Keys.ENTER)

            # 判断验证码是否输入正确
            time.sleep(1)
            code_status = self.driver.find_element_by_xpath('//div[@class="content"]')
            response = code_status.get_attribute('innerHTML')
            if len(response):
                print('错误代码：{}'.format(response))
                # 刷新页面
                self.driver.refresh()
                continue
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
            print('查询失败')
            return
        print(res[0].is_displayed())
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="search"]/button')))
        # page_source 获取网页源码 加等待时间防止页面刷新不出来
        # response = self.driver.page_source
        # get_attribute('innerHTML') 获取指定元素源代码
        response = res[0].get_attribute('innerHTML')
        # 源代码保存为本地HTML文件
        with open('a.html', 'w', encoding='gbk') as f:
            f.write(response)
            print('保存成功')

    def run(self):
        self.get_code()
        self.get_content()
        self.get_html()


if __name__ == '__main__':
    spider = Spider()
    spider.run()
