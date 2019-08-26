from selenium import webdriver
import requests


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


if __name__ == '__main__':
    Proxy()