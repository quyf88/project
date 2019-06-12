# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
import openpyxl
import threading
import time, json, random
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import traceback
import re
import os
import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings()
import logging
from selenium.webdriver.common.keys import Keys


class Spider(object):
    def __init__(self):
        self.log = self.init_log()
        self.log.info("程序启动中...")
        self.edit_count = 0
        self.add_price = 0
        self.good_ids = []
        self.fail_ids = []
        self.success_ids = []
        self.goods_urls = {}
        self.size_price_dict = {}
        self.cookie = ''
        self.token = ''

        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
        desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        '''设置浏览器是否显示图片'''
        prefs = {"profile.managed_default_content_settings.images": 1}
        chrome_options.add_experimental_option("prefs", prefs)
        #chrome_options.add_argument("user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data\\Default");
        #chrome_options.add_argument("user-data-dir=C:\\Users\\Coolio\\AppData\\Local\\Google\\Chrome\\User Data\\Default");

        self.driver = webdriver.Chrome()
        #self.driver = webdriver.Chrome(chrome_options=chrome_options,executable_path="chromedriver.exe")
        self.wait = WebDriverWait(self.driver, 20)
        self.driver.maximize_window()

    def main(self):
        self.login_by_scan()
        # self.login_by_cookie()
        #try:
        start = time.time()
        self.get_goods_urls()
        self.read_excel()
        self.edit()
        end = time.time()
        spend = (end - start) // 60
        self.log.info("总计匹配[{}]条商品信息, 修改成功[{}]条，修改失败[{}]条，失败原因请查看更新日志! 耗时:[{}]分钟.."
                      .format(len(self.size_price_dict), len(self.success_ids), len(self.fail_ids), spend))

    def login_by_cookie(self):
        print("开始cookies登录")
        self.driver.get("https://www.taobao.com")

        cookies = [{'domain': '.taobao.com', 'httpOnly': True, 'name': 'cookie2', 'path': '/', 'secure': False,
                    'value': '50b28eaeb096654e599fb0844dce970d'},
                   {'domain': '.taobao.com', 'expiry': 1581821254.533909, 'httpOnly': False, 'name': 'thw', 'path': '/',
                    'secure': True, 'value': 'cn'},
                   {'domain': '.taobao.com', 'expiry': 1558685395.155936, 'httpOnly': False, 'name': 't', 'path': '/',
                    'secure': False, 'value': 'f0befd3785396912271915ebec8bdce2'},
                   {'domain': '.taobao.com', 'expiry': 1550986977.944252, 'httpOnly': False, 'name': '_m_h5_tk',
                    'path': '/', 'secure': True, 'value': '2f6fc9550517202aa1a1f0875889f7db_1550390459773'},
                   {'domain': '.taobao.com', 'expiry': 2181103264, 'httpOnly': False, 'name': '_tb_token_', 'path': '/',
                    'secure': True, 'value': '1df5e5ee7eb5'},
                   {'domain': '.taobao.com', 'expiry': 1865647436.657436, 'httpOnly': True, 'name': 'enc', 'path': '/',
                    'secure': True,
                    'value': 'H7yEj5rfskpQaAUyRLIaandz8ZpRUMdg5ggguFBe5yqLyHj6el8W8b5bsDWpSfOuvxorSSkyfpAaXRr2DVHDdQ%3D%3D'},
                   {'domain': '.taobao.com', 'expiry': 1581823437.33291, 'httpOnly': False, 'name': 'hng', 'path': '/',
                    'secure': True, 'value': 'CN%7Czh-CN%7CCNY%7C156'},
                   {'domain': '.taobao.com', 'httpOnly': False, 'name': '_nk_', 'path': '/', 'secure': False,
                    'value': 'trendup%5Cu4E3B'},
                   {'domain': '.taobao.com', 'expiry': 1865652302.155698, 'httpOnly': False, 'name': 'cna', 'path': '/',
                    'secure': True, 'value': 'EmzuFLlINxUCAXcEsaqTuz9U'},
                   {'domain': '.taobao.com', 'expiry': 1581824524, 'httpOnly': False, 'name': 'x', 'path': '/',
                    'secure': True,
                    'value': 'e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0'},
                   {'domain': '.taobao.com', 'httpOnly': False, 'name': 'dnk', 'path': '/', 'secure': False,
                    'value': 'trendup%5Cu4E3B'},
                   {'domain': '.taobao.com', 'expiry': 1551514195.156672, 'httpOnly': False, 'name': 'mt', 'path': '/',
                    'secure': False, 'value': 'ci=1_1&np='},
                   {'domain': '.taobao.com', 'expiry': 1566025727, 'httpOnly': False, 'name': 'UM_distinctid',
                    'path': '/', 'secure': True,
                    'value': '168f522d73735f-04c318f0fb224c-3f674706-384000-168f522d7386bf'},
                   {'domain': '.taobao.com', 'expiry': 1550986977.944315, 'httpOnly': False, 'name': '_m_h5_tk_enc',
                    'path': '/', 'secure': True, 'value': 'e5a9f440e737235f4cbbbf3af32dfd89'},
                   {'domain': '.taobao.com', 'expiry': 1582445395.156411, 'httpOnly': False, 'name': 'tracknick',
                    'path': '/', 'secure': False, 'value': 'trendup%5Cu4E3B'},
                   {'domain': '.taobao.com', 'expiry': 1553501395.15646, 'httpOnly': False, 'name': 'lgc', 'path': '/',
                    'secure': False, 'value': 'trendup%5Cu4E3B'},
                   {'domain': '.taobao.com', 'expiry': 1604909395.156635, 'httpOnly': False, 'name': 'tg', 'path': '/',
                    'secure': False, 'value': '4'},
                   {'domain': '.taobao.com', 'httpOnly': False, 'name': 'v', 'path': '/', 'secure': False,
                    'value': '0'},
                   {'domain': '.taobao.com', 'httpOnly': False, 'name': 'uc1', 'path': '/', 'secure': False,
                    'value': 'cookie14=UoTZ5Om3bC2GgQ%3D%3D&lng=zh_CN&cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&existShop=true&cookie21=VFC%2FuZ9ajCbF8%2BYBppEi9Q%3D%3D&tag=8&cookie15=WqG3DMC9VAQiUQ%3D%3D&pas=0'},
                   {'domain': '.taobao.com', 'httpOnly': True, 'name': 'unb', 'path': '/', 'secure': False,
                    'value': '2200534816426'},
                   {'domain': '.taobao.com', 'httpOnly': False, 'name': 'sg', 'path': '/', 'secure': False,
                    'value': '%E4%B8%BB6b'},
                   {'domain': '.taobao.com', 'httpOnly': False, 'name': '_l_g_', 'path': '/', 'secure': False,
                    'value': 'Ug%3D%3D'},
                   {'domain': '.taobao.com', 'httpOnly': True, 'name': 'skt', 'path': '/', 'secure': False,
                    'value': '646addc80c7e40b1'},
                   {'domain': '.taobao.com', 'httpOnly': True, 'name': 'cookie1', 'path': '/', 'secure': False,
                    'value': 'BvBUZS%2BqsuqTYu7cgCSrKpt5mcPhHxjTG3glpSFuZC0%3D'},
                   {'domain': '.taobao.com', 'httpOnly': False, 'name': 'csg', 'path': '/', 'secure': False,
                    'value': 'b60c08e4'},
                   {'domain': '.taobao.com', 'expiry': 1553501395.156316, 'httpOnly': True, 'name': 'uc3', 'path': '/',
                    'secure': False,
                    'value': 'vt3=F8dByEzb%2FMhA%2BQyRjfg%3D&id2=UUphyuwKL0ki46FuSw%3D%3D&nk2=F4T6omkcT%2BMM&lg2=WqG3DMC9VAQiUQ%3D%3D'},
                   {'domain': '.taobao.com', 'httpOnly': False, 'name': 'existShop', 'path': '/', 'secure': False,
                    'value': 'MTU1MDkwOTM5Ng%3D%3D'},
                   {'domain': '.taobao.com', 'expiry': 1582445395.1565, 'httpOnly': False, 'name': '_cc_', 'path': '/',
                    'secure': False, 'value': 'V32FPkk%2Fhw%3D%3D'},
                   {'domain': '.taobao.com', 'httpOnly': True, 'name': 'cookie17', 'path': '/', 'secure': False,
                    'value': 'UUphyuwKL0ki46FuSw%3D%3D'},
                   {'domain': '.taobao.com', 'expiry': 1566461357, 'httpOnly': False, 'name': 'l', 'path': '/',
                    'secure': False,
                    'value': 'bBxf0HdVvFqSxaG0BOfwNuI81__9wIRb4sPzw4sasICP9vsW5yVFWZaAtJJXC3Gcw1WkR3jnmqCLBeYBq6C..'},
                   {'domain': '.taobao.com', 'expiry': 1566461395, 'httpOnly': False, 'name': 'isg', 'path': '/',
                    'secure': False, 'value': 'BG1tMbuWzbxkeqnHYTNPW-dtfAknYr4U-XIaG69yqoRzJo3YdxqxbLv0FPvAprlU'}]

        for cookie in cookies:
            self.driver.add_cookie(cookie)
        time.sleep(1)
        self.driver.refresh()

    def login_by_scan(self):
        self.log.info("开始登录,请等待页面加载完成后,扫码登录...")
        self.driver.get('https://login.taobao.com/member/login.jhtml?redirectURL=https://www.taobao.com/')
        while True:
            if 'data' in self.driver.current_url:
                self.log.info("等待扫码中...")
                time.sleep(2)
            if 'login.taobao.com' not in self.driver.current_url:
                self.log.info("登录成功")
                break
            else:
                self.log.info("等待扫码中...")
                time.sleep(2)

    def get_total_page(self):
        html = self.driver.page_source.replace(' ', '').replace("'", '"')
        try:
            self.token = re.findall('tokenValue:"(.*?)"', html, re.I | re.S)[0]
            self.log.info("获取此商家登陆状态的token成功, token:[{}]".format(self.token))
        except Exception as ex:
            print(html)
            self.log.error("获取此商家登陆状态的token失败, 原因:[{}], 请联系管理员!!!".format(ex))
            return None
        for k in self.driver.get_cookies():
            self.cookie += '{}={}; '.format(k['name'], k['value'])

        goods_num = self.driver.find_element_by_id("list-pagination-top-total").text
        # goods_num = self.driver.find_element_by_id("J_onSaleCount_1").text
        result = re.search("\d+", goods_num)
        if result is None:
            self.log.info("获取出售中的商品数量失败")
            return None

        goods_num = int(result.group(0))
        self.log.info("出售中的宝贝数量：{}".format(goods_num))
        page_size = 20
        total_page_num = (goods_num + page_size - 1) // page_size
        self.log.info("计算出宝贝总数页：{}".format(total_page_num))
        self.total_page_num = total_page_num
        return total_page_num

    def get_goods_urls(self):
        self.log.info("开始获取出售中的商品信息...")
        # self.driver.get("https://sell.taobao.com/auction/merchandise/auction_list.htm?type=11")
        self.driver.get(
            'https://item.publish.taobao.com/taobao/manager/render.htm?tab=on_sale&table.sort.startDate_m=desc')
        time.sleep(5)
        total_page = self.get_total_page()
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        spans = soup.find_all('span', class_='product-desc-span')
        for span in spans:
            if 'ID' not in str(span) or '编码' not in str(span):
                continue
            product_data = str(span.get_text()).strip()
            product_id = str(re.findall('ID:(.*?)编码:', product_data, re.S | re.I)[0]).strip()
            gsid = str(re.findall('编码:(.*?)<', str(span), re.S | re.I)[0]).strip()
            product_id = product_id + "~" + gsid
            self.good_ids.append(product_id)

        self.get_other_page_urls(total_page)
        if len(self.good_ids) == 0:
            self.log.info("没有获取到商品信息")
            return

    def edit(self):
        self.log.info("开始修改出售中的商品价格...")
        if len(self.size_price_dict) == 0:
            self.log.info("出售中的商品没有匹配到任何Excel中的数据")
            return
        for items in self.good_ids:
            itemid = items.split('~')[0]  # 淘宝上的itemid
            gsid = items.split('~')[1]  # 淘宝上的商家编码

            for j in self.size_price_dict.keys():
                prices = self.size_price_dict[j]
                if j == gsid:
                    url = 'https://item.publish.taobao.com/taobao/manager/fastEdit.htm?optType=editPriceRender'

                    data = {
                        'itemId': itemid
                    }
                    headers = {
                        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
                        'x-xsrf-token': self.token,
                        'cookie': self.cookie
                    }
                    try:

                        res1 = requests.post(url, data=data, headers=headers, verify=False)
                        html = res1.text
                        if '登录页面' in html:
                            self.log.info('获取到的cookie错误，请重新登陆！')
                            return
                        res1_j = res1.json()
                    except Exception as ex:
                        self.log.debug('获取修改商品的详情信息失败，原因:{}, 请联系开发人员！'.format(ex))
                        return
                    if res1_j.get('success'):
                        value = res1_j['data']['value']

                        if 'skuPriceTable' in value and 'dataSource' in value['skuPriceTable']:

                            self.log.info('获取商家编码[{}], ID[{}]商品详情信息成功, 共存在[{}]种商品尺码'.format(gsid, itemid, len(
                           value['skuPriceTable']['dataSource'])))
                        else:
                            self.log.info('获取商家编码[{}], ID[{}]商品详情信息成功, 共存在[{}]种商品尺码'.format(gsid, itemid, '--'))
                        # threading.Thread(target=self.edit_price_by_itemid, args=(gsid, itemid, value, prices)).start()
                        self.edit_price_by_itemid(gsid, itemid, value, prices)
                    else:
                        self.log.info('获取修改商品的详情信息失败，请确认itemid是否正确!')
                continue
        return

    def edit_price_by_itemid(self, gsid, itemid, value, prices):
        size_price_list = []  # 获取到的商家价格进行存储，到时候取最小的一个值   or not 'dataSource' in value['skuPriceTable']
        if 'skuPriceTable' not in value or 'dataSource' not in value['skuPriceTable']:
            print("there is no dataSource or no skuPriceTable")
            return
        for j in value['skuPriceTable']['dataSource']:
            prop = str(j['prop']).split('/')[-1]  # 淘宝上查询到的大小 36，35
            price = j['skuPrice']
            for t in prices:
                u_prop = t  # excel中读取到的尺码, 即将修改的
                u_price = str(prices[t])  # excel中读取到的金额，即将修改的
                if u_price == '--':
                    continue
                if u_prop == prop and u_price != '--':
                    new_skuPrice = float(u_price) + float(self.add_price)
                    j['skuPrice'] = new_skuPrice
                    self.log.info('即将修改商家编码[{}], ID[{}], 尺码[{}]，初始金额[{}]，Excel金额[{}], 增减金额[{}], '
                                  '修改后金额[{}]的商品信息'.format(gsid, itemid, u_prop, price, u_price, self.add_price,
                                                          new_skuPrice))
        for j in value['skuPriceTable']['dataSource']:
            size_price_list.append(float(j['skuPrice']))

        one_price = sorted(size_price_list)[0]
        value['price'] = str(one_price)  # 针对一口价做处理
        url = 'https://item.publish.taobao.com/taobao/manager/fastEdit.htm?optType=editPriceSubmit'
        data = {
            'value': str(value).replace("'", '"'),
            'itemId': itemid
        }
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
            'x-xsrf-token': self.token,
            'cookie': self.cookie
        }
        res = requests.post(url, headers=headers, data=data, verify=False)
        res_j = res.json()
        if res_j.get('success'):
            self.success_ids.append(itemid)
            self.log.info('修改商家编码[{}], ID[{}]价格成功，请刷新后查看...'.format(gsid, itemid))
        else:
            self.fail_ids.append(itemid)
            self.log.info('修改商家编码[{}],ID[{}]的价格失败，原因[{}]!!!，提交数据:[{}]'.format(gsid, itemid, res_j, value))

    def get_other_page_urls(self, total_page):
        total_page = total_page + 1
        for i in range(2, total_page):
            url = 'https://item.publish.taobao.com/taobao/manager/render.htm?pagination.current={}&pagination.' \
                  'pageSize=20&tab=on_sale&table.sort.startDate_m=desc'.format(i)
            self.driver.get(url)
            time.sleep(3)

            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            spans = soup.find_all('span', class_='product-desc-span')
            for span in spans:
                if 'ID' not in str(span) or '编码' not in str(span):
                    continue
                product_data = str(span.get_text()).strip()
                product_id = str(re.findall('ID:(.*?)编码:', product_data, re.S | re.I)[0]).strip()
                gsid = str(re.findall('编码:(.*?)<', str(span), re.S | re.I)[0]).strip()
                product_id = product_id + "~" + gsid
                self.good_ids.append(product_id)

        self.log.info("出售中的商品即将用来匹配Excel中的编号：{}".format(self.good_ids))

    def edit_price(self):
        self.log.info("开始修改出售中的商品价格...")
        if len(self.size_price_dict) == 0:
            self.log.info("出售中的商品没有匹配到任何Excel中的数据")
            return
        for key in self.size_price_dict.keys():
            price_dict = self.size_price_dict[key]
            url = self.goods_urls[key]
            self.log.info("开始修改商品,链接：{}".format(url))
            js = 'window.open("{}");'.format(url)
            self.driver.execute_script(js)
            time.sleep(3)
            windows = self.driver.window_handles
            self.driver.switch_to_window(windows[1])
            trs = self.driver.find_elements_by_css_selector(".sell-sku-inner-table.sell-sku-body-table tbody tr")
            price_one = self.driver.find_element_by_id("price").get_attribute("value")
            all_price = []
            if len(trs) == 0:
                self.log.info("当前商品：{}没有尺码，不做修改跳过".format(key))
                self.driver.close()
                time.sleep(2)
                self.driver.switch_to_window(windows[0])
                continue
            for tr in trs:
                tds = tr.find_elements_by_tag_name("td")
                size = str(tds[1].text).strip()
                input_box = tr.find_element_by_css_selector('input[name="skuPrice"]')
                original_price = input_box.get_attribute("value")
                original_price = str(original_price).replace(".00", "")
                # if original_price == price_one:
                #     self.log.info("商品编号：{} 尺码：{}--原价：{} 当前为一口价不做修改".format(key,size,original_price))
                #     continue
                if size not in price_dict.keys():
                    self.log.info("商品编号：{} 尺码：{}==》原价：{} 未匹配到excel中的数据,不做修改".format(key, size, original_price))
                    all_price.append(int(original_price))
                    continue
                edit_value = price_dict[size]
                input_box.send_keys(Keys.CONTROL, 'a')
                time.sleep(0.2)
                input_box.send_keys(Keys.BACK_SPACE)
                time.sleep(0.2)
                input_box.send_keys(edit_value)
                self.log.info("商品编号：{} 尺码：{} 原价 ：{} 修改为==》{}".format(key, size, original_price, edit_value))
                edit_value = str(edit_value).replace(".00", "")
                all_price.append(int(edit_value))

            list.sort(all_price)
            min_price = all_price[0]
            min_price_box = self.driver.find_element_by_id("price")
            min_price_box.send_keys(Keys.CONTROL, 'a')
            time.sleep(0.2)
            min_price_box.send_keys(Keys.BACK_SPACE)
            time.sleep(0.2)
            min_price_box.send_keys(min_price)
            self.log.info("商品编号：{} 一口价修改 {}==》{}".format(key, price_one, min_price))
            time.sleep(1)
            self.driver.find_element_by_id("button-submit").click()
            time.sleep(1)

            item_id = str(key).split("~")[0]
            show_url = "https://item.taobao.com/item.htm?id={}".format(item_id)
            while True:
                if self.driver.current_url == show_url or self.driver.current_url != url:
                    self.log.info("商品编号：{} 修改成功".format(key))
                    self.edit_count = self.edit_count + 1
                    break
                else:
                    time.sleep(1)

            self.driver.close()
            self.log.info("系统沉睡1秒后继续...")
            time.sleep(1)
            self.driver.switch_to_window(windows[0])

    def read_excel(self):
        self.log.info("开始读取excel中待修改的数据...")
        path = "excel/"
        root_dir = os.path.split(os.path.realpath(__file__))[0]
        path = os.path.join(root_dir, path)
        for file in os.listdir(path):
            if '.' in file and file.split(".")[1] == "xlsx" and not file.startswith('~$'):
                excel_path = path + file
                self.log.info("开始读取 ==》{}".format(excel_path))
                workbook = openpyxl.load_workbook(filename=excel_path, read_only=False)
                sheet = workbook['Sheet1']
                rownum = sheet.max_row
                self.log.info("{}总条数：{}".format(excel_path, rownum))
                for index, row in enumerate(sheet.rows):
                    if index == 0:
                        continue
                    product = str(row[8].value)
                    is_match = False
                    for key in self.good_ids:
                        if product in key:
                            is_match = True
                            # product = key
                            break
                    if not is_match:
                        continue
                    size_price = row[15].value
                    size_price = self.parse_price(size_price)
                    self.size_price_dict[product] = size_price
        # print(self.size_price_dict)
        self.log.info("出售中的商品成功匹配excel数据{}条".format(len(self.size_price_dict.keys())))

    def parse_price(self, datas):
        datas = list(eval(datas))
        result = {}
        for item in datas:
            key = item[0]
            value = str(item[1])
            if "--" in value:
                continue
            result[key] = value
        return result

    def init_log(self):
        formatter = logging.Formatter('%(asctime)s | %(name)-6s | %(levelname)-6s| %(message)s')
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        fh = logging.FileHandler('run.log', encoding='utf-8', mode='w')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        console.setFormatter(formatter)
        logger = logging.getLogger("Spider")
        logger.setLevel(logging.DEBUG)
        logger.addHandler(console)
        logger.addHandler(fh)
        return logger

    def edit_min_price(self, key):
        iframes = self.driver.find_elements_by_tag_name("iframe")
        self.driver.switch_to_frame(iframes[1])
        time.sleep(0.5)
        plist = self.driver.find_elements_by_css_selector("#edit-price-SKU-iframe form p")
        plist = plist[0:len(plist) - 1]
        price_dict = self.size_price_dict[key]
        all_price = []
        min_price_box = None
        price_one = 0
        for item in plist:
            input_box = item.find_element_by_css_selector('input[name="new-SKU-price"]')
            lable = item.find_element_by_css_selector(".SKU-name").text
            if "一口价" in lable:
                min_price_box = input_box
                price_one = input_box.get_attribute("value")
                price_one = str(price_one).replace(".00", "")
                time.sleep(1)
                continue
            else:
                lable = str(lable).replace("：", "").strip()
                index = lable.rindex("/")
                size = lable[index + 1:]
                original_price = input_box.get_attribute("value")
                original_price = str(original_price).replace(".00", "")
                if size not in price_dict.keys():
                    self.log.info("商品编号：{} 尺码：{}==》原价：{} 未匹配到excel中的数据,不做修改".format(key, size, original_price))
                    all_price.append(int(original_price))
                    continue
                edit_value = price_dict[size]
                input_box.send_keys(Keys.CONTROL, 'a')
                time.sleep(1)
                input_box.send_keys(Keys.BACK_SPACE)
                time.sleep(1)
                input_box.send_keys(edit_value)
                self.log.info("商品编号：{} 尺码：{} 原价 ：{} 修改为==》{}".format(key, size, original_price, edit_value))
                edit_value = str(edit_value).replace(".00", "")
                all_price.append(int(edit_value))

        list.sort(all_price)
        print(all_price)
        min_price = all_price[0]
        min_price_box.send_keys(Keys.CONTROL, 'a')
        time.sleep(1)
        min_price_box.send_keys(Keys.BACK_SPACE)
        time.sleep(1)
        min_price_box.send_keys(min_price)
        self.log.info("商品编号：{} 一口价修改 {}==》{}".format(key, price_one, min_price))
        time.sleep(1)

        submit_btn = self.driver.find_element_by_css_selector("#edit-price-SKU-iframe form .J_edit-SKU-save ")
        time.sleep(1)
        submit_btn.click()
        time.sleep(1)
        self.driver.switch_to_default_content()
        self.edit_count = self.edit_count + 1


if __name__ == '__main__':
    in_add_price = input('请输入针对所有商品进行加减价的具体金额!')
    # in_add_price = 0
    bot = Spider()
    bot.add_price = in_add_price
    bot.main()
