"""
谷歌浏览器 xpath定位插件 Xpath Helper
#### **获取标签value值**
  - ```cmd
    # 商品ID   a/@data-nid 获取a标签下 data-nid的value值        
    commodity_id = self.driver.find_element_by_xpath('//div[@class="pic"]/a/@data-nid') 
    ```
#### **根据标签文本 定位标签**
  - ```cmd
    self.wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "下一页")]')))
    ```
#### **元素click点击失败 用 ENTER点击**
- ```cmd
    .send_keys(Keys.ENTER)
   ```
"""

"""
谷歌浏览器 CSS定位插件 SelectorGadget
CSS 定位
#kw :定位id='kw'元素
.username > .W_input :定位class='username'下的class='W_input'的元素
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# selenium无界面模式 keep_alive 设置浏览器连接活跃状态
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options, keep_alive=False)
wait = WebDriverWait(driver, 8, 0.5)  # 设置隐式等待时间
driver.maximize_window()  # 窗口最大化

# selenium有界面模式
chrome_options = Options()
desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
prefs = {"profile.managed_default_content_settings.images": 1}  # 1 加载图片 2不加载图片,加快访问速度
chrome_options.add_experimental_option("prefs", prefs)
# 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = webdriver.Chrome(chrome_options=chrome_options)
wait = WebDriverWait(driver, 8, 0.5)  # 设置隐式等待时间
driver.maximize_window()  # 窗口最大化


url = 'https://www.baidu.com/'
response = driver.get(url)
a = driver.find_element_by_css_selector('#kw')
time.sleep(1)
a.click()
time.sleep(1)
a.send_keys('haha')

"""常用方法"""
# 打印当前所有所有句柄（窗口）
driver.window_handles
# 获取当前窗口句柄
driver.current_window_handle
# 获取当前页面源码
driver.page_source
# 获取指定元素源码
ke = driver.find_element_by_xpath('//*[@id="Form1"]/div[4]/div/div[3]/div[2]/div[3]/div[6]/div[2]')
html = ke.get_attribute('innerHTML')



# 滚屏
js = "var q=document.body.scrollTop=1200"
driver.execute_script(js)

# 滑动滚动条到某个指定的元素
div=driver.find_element_by_xpath('//div[@class="title-tab text-center"]')
js4 = "arguments[0].scrollIntoView();"
# 将下拉滑动条滑动到当前div区域
driver.execute_script(js4, div)



# iframe
login_if = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#loginDiv > iframe')))  # 定位iframe
driver.switch_to.frame(login_if)  # 切换iframe
driver.switch_to.default_content()  # 退出当前iframe


"""添加cookie"""
# 添加cookie前 需要先打开页面
driver.get('https://www.v99two.com/')
# 获取登录前cookies
# for ck in self.driver.get_cookies():
#     print(ck)
# 登录
# time.sleep(30)
# 获取登录后cookies
# for ck in self.driver.get_cookies():
#     print(ck)
# driver请求添加cookie参数
cookies = {'domain': '.v99two.com', 'name': 'PHPSESSID', 'value': '6cc7af233de034dd73d6333a2db5e5d8'}
driver.add_cookie(cookie_dict=cookies)

# 设置代理
class Proxy(object):
    def __init__(self):
        proxies = requests.get('http://www.uu-ip.com/ProxyiPAPI.aspx?action=GetIPAPI&qty=1&ordernumber=56b059a66c25a48db7a3e4426ff6573c').text
        self.proxy_ip = 'http://{}'.format(proxies)
        print(self.proxy_ip)
        self.browser = self.getbrowser()
        self.getpage(self.browser)

    def getbrowser(self):
        options = webdriver.ChromeOptions()
        # 设置代理
        desired_capabilities = webdriver.DesiredCapabilities.INTERNETEXPLORER.copy()
        desired_capabilities['proxy'] = {
            "httpProxy": self.proxy_ip,
            "proxyType": "MANUAL",  # 此项不可注释
            # "ftpProxy": self.proxy_ip,  # 代理ip是否支持这个协议
            # "sslProxy": self.proxy_ip,  # 代理ip是否支持这个协议
            # "noProxy": None,
            # "class": "org.openqa.selenium.Proxy",
            # "autodetect": False
        }
        # 使用无头模式
        options.add_argument('headless')
        browser = webdriver.Chrome(chrome_options=options,
                                   desired_capabilities=desired_capabilities)
        return browser

    def getpage(self, browser):
        # 打开目标网站
        browser.get("https://www.baidu.com")
        # 对整个页面进行截图
        browser.save_screenshot('百度.png')
        # 打印网站的title信息
        print(browser.title)

        # 检测代理ip是否生效
        browser.get("http://httpbin.org/ip")
        # 获取当前所有窗口集合(list类型) --- 因为打开多个窗口
        handles = browser.window_handles
        # 切换到最新的窗口
        browser.switch_to_window(handles[-1])
        # 打印新窗口网页的内容
        print(browser.page_source)


"""selenium get()请求页面加载超时设置"""
def selenium_get(self, url):
    # 限定页面加载时间最大为100秒
    self.driver.set_page_load_timeout(100)
    try:
        self.driver.get(url)
        return True
    except:
        print(u'页面加载超时!')
        # 当页面加载时间超过设定时间，通过执行Javascript来停止载，然后继续执行后续操作
        self.driver.execute_script('window.stop()')
        return False