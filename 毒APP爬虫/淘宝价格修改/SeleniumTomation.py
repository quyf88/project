# -*- coding:utf-8 -*-
import re
import os
import time
import logging
import openpyxl
import traceback
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Spider:
    def __init__(self):
        self.log = self.init_log()
        self.log.info("程序启动中...请输入针对所有商品进行加减价的具体金额:(如不需修改请写'0')")
        self.edit_count = 0
        self.counts = 0
        self.good_ids = []
        self.goods_urls = {}
        self.size_price_dict = {}
        self.in_add_price = int(input("输入金额：(减价'-')"))
        chrome_options = Options()
        desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
        desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        '''设置浏览器是否显示图片'''
        prefs = {"profile.managed_default_content_settings.images": 1}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument(
            "user-data-dir=C:\\Users\\Coolio\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="chromedriver.exe")
        self.wait = WebDriverWait(self.driver, 20)
        self.driver.maximize_window()


    def main(self):
        # 登录
        self.login_by_scan()
        try:
            start_time = datetime.now()
            self.log.info("程序开始时间：{}".format(start_time))
            # 获取在售商品信息
            self.get_goods_urls()
            # 在售商品匹配excel表格数据
            self.read_excel()
            self.edit()
            end_time = datetime.now()
            self.log.info("所有商品更新完成")
            self.log.info("总计更新{}条商品信息".format(self.edit_count))
            self.log.info("程序结束时间：{}".format(end_time))
            self.log.info("程序执行用时：{}s".format((end_time - start_time)))
        except:
            traceback.print_exc()
            self.log.debug("程序出现异常,请联系开发者")

    def login_by_scan(self):
        self.log.info("开始登录,请等待页面加载完成后,扫码登录...")
        self.driver.get('https://login.taobao.com/member/login.jhtml?redirectURL=https://www.taobao.com/')
        while True:
            if 'login.taobao.com' not in self.driver.current_url:
                self.log.info("登录成功")
                cookies = self.driver.get_cookies()
                self.log.info(cookies)
                break
            else:
                self.log.info("等待扫码中...")
                time.sleep(2)

    def get_total_page(self):
        """获取出售中的商品页数"""
        goods_num = self.driver.find_element_by_id("list-pagination-top-total").get_attribute("innerHTML")

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
        """获取出售中的商品信息 产品ID 编码 url"""

        self.log.info("开始获取出售中的商品信息...")
        self.driver.get("https://sell.taobao.com/auction/merchandise/auction_list.htm?type=11")
        time.sleep(2)
        total_page = self.get_total_page()

        # 产品ID 编码
        trs = self.driver.find_elements_by_class_name("list-table-desc-extend-cell")
        for tr in trs:
            tr_text = tr.text

            # 产品ID
            product_id = re.search(r'ID:(\d+)', tr_text).group().replace('ID:', '')
            # 编码
            gsid = re.search(r'编码:(.*)', tr_text).group().replace('编码:', '')
            # url
            edit_url = "https://item.publish.taobao.com/sell/publish.htm?itemId={}".format(product_id)

            product_id = gsid
            self.good_ids.append(product_id)
            self.goods_urls[product_id] = edit_url

        self.get_other_page_urls(total_page)
        if len(self.good_ids) == 0:
            self.log.info("没有获取到商品信息")
            return

    def edit(self):
        total_page = int(self.total_page_num)
        total_page = total_page + 1
        for i in range(1, total_page):
            # 点击下一页
            if i > 1:
                next_page = self.driver.find_elements_by_xpath(
                    '//*[@class="next-btn next-btn-normal next-btn-medium next-pagination-item next"]')
                next_page[0].click()
            # 产品ID
            trs = self.driver.find_elements_by_class_name("list-table-desc-extend-cell")
            for tr in trs:
                # 商家编码
                gsid = re.search(r'编码:(.*)', tr.text).group().replace('编码:', '')
                for key in self.size_price_dict.keys():
                    if str(gsid) not in key:
                        continue

                    time.sleep(2)
                    self.log.info("\n\n开始修改商品：{}".format(key))
                    self.edit_min_price(key)
                    time.sleep(2)
                    break

    def get_other_page_urls(self, total_page):
        """获取所有页面商品url"""
        total_page = total_page + 1
        for i in range(2, total_page):
            # 点击下一页
            next_page = self.driver.find_element_by_class_name('next-btn next-btn-normal next-btn-medium next-pagination-item next')
            next_page.click()

            trs = self.driver.find_elements_by_class_name("list-table-desc-extend-cell")
            for tr in trs:
                tr_text = tr.text
                print(tr_text)
                # 产品ID
                product_id = re.search(r'ID:(\d+)', tr_text).group().replace('ID:', '')
                # 编码
                gsid = re.search(r'编码:(.*)', tr_text).group().replace('编码:', '')
                # url
                edit_url = "https://item.publish.taobao.com/sell/publish.htm?itemId={}".format(product_id)

                product_id = product_id + "~" + gsid
                self.good_ids.append(product_id)
                self.goods_urls[product_id] = edit_url

        self.log.info("出售中的商品匹配到Excel中的编号：{}".format(self.good_ids))

    def read_excel(self):
        """匹配出在售商品数据"""
        self.log.info("开始读取excel中待修改的数据...")
        path = "excel/"
        root_dir = os.path.split(os.path.realpath(__file__))[0]
        path = os.path.join(root_dir, path)
        for file in os.listdir(path):
            if '.' in file and file.split(".")[1] == "xlsx":
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
                            product = key
                            break
                    if not is_match:
                        continue
                    size_price = row[15].value
                    size_price = self.parse_price(size_price)
                    self.size_price_dict[product] = size_price

        self.log.info("出售中的商品成功匹配excel数据{}条".format(len(self.size_price_dict.keys())))

    def parse_price(self, datas):
        """取出有价格的尺码数据"""
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
        """日志"""
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
        """修改商品价格"""
        all_price = []
        count = 0

        # 定位隐藏属性
        time.sleep(3)
        mouses = self.driver.find_elements_by_xpath('//div[@class="list-table-desc-extend-cell"]')
        for mouse in mouses:
            gsid = re.search(r'编码:(.*)', mouse.text).group().replace('编码:', '')
            if gsid == key:
                ActionChains(self.driver).move_to_element(mouse).perform()
                self.driver.find_elements_by_xpath('//i[@class="next-icon next-icon-edit2 next-icon-small table-cell-edit-icon"]')[self.counts].click()

                time.sleep(3)
                # 尺码
                SKUS = self.driver.find_elements_by_xpath('//*[@class="next-table-cell first"]')
                # 价格
                input_box = self.driver.find_elements_by_xpath('//td[@class="next-table-cell last"]/div/div/div/span/span//span/input')
                original_price = str(input_box[count].get_attribute("value")).replace(".00", "")
                # excel 价目表
                price_dict = self.size_price_dict[key]

                for size in SKUS:
                    size = str(size.text).split('/')[-1]

                    if size not in price_dict.keys():
                        self.log.info("商品编号：{} 尺码：{}==》原价：{} 未匹配到excel中的数据,不做修改".format(key, size, original_price))
                        continue
                    if self.in_add_price:
                        edit_value = int(price_dict[size]) + self.in_add_price
                    else:
                        edit_value = price_dict[size]
                    input_box[count].send_keys(Keys.CONTROL, 'a')
                    time.sleep(0.2)
                    input_box[count].send_keys(Keys.BACK_SPACE)
                    time.sleep(0.2)

                    input_box[count].send_keys(edit_value)
                    self.log.info('修改成功：商家编码[{}], 尺码[{}]，初始金额[{}]，Excel金额[{}], 增减金额[{}], '
                                  '修改后金额[{}]'.format(key, size, original_price, price_dict[size], self.in_add_price, edit_value))
                    # self.log.info("商品编号：{} 尺码：{} 原价 ：{} 修改为==》{}".format(key, size, original_price, edit_value))
                    # edit_value = str(edit_value).replace(".00", "")
                    all_price.append(int(edit_value))
                    count += 1
                list.sort(all_price)

                min_price = all_price[0]
                # 一口价
                price = self.driver.find_element_by_xpath('//*[@name="price"]')
                price_str = str(price.get_attribute("value")).replace('.00', '')
                price.send_keys(Keys.CONTROL, 'a')
                time.sleep(0.2)
                price.send_keys(Keys.BACK_SPACE)
                time.sleep(0.2)
                price.send_keys(min_price)
                self.log.info("商品编号：{} 一口价修改 {}==》{}".format(key, price_str, min_price))
                time.sleep(1)

                # 提交
                submit_btn = self.driver.find_elements_by_xpath('//*[@class="next-btn next-btn-normal next-btn-medium"]')
                time.sleep(0.5)
                submit_btn[0].click()
                time.sleep(1)

                self.edit_count = self.edit_count + 1
                self.counts += 2
            else:
                continue


if __name__ == '__main__':
    bot = Spider()
    bot.main()
