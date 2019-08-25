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
# iframe
login_if = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#loginDiv > iframe')))  # 定位iframe
self.driver.switch_to.frame(login_if)  # 切换iframe
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