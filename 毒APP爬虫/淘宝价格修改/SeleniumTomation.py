# -*- coding:utf-8 -*-
import re
import os
import time
import logging
import openpyxl
import traceback
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Spider:
    def __init__(self):
        self.log = self.init_log()
        self.log.info("程序启动中...请输入针对所有商品进行加减价的具体金额:(如不需修改请写'0')")
        self.log.info("PS:程序运行过程中保持浏览器启动后的状态，不要最小化或移动窗口，鼠标不要和浏览器有交互行为!!!")
        # 成功修改数量
        self.edit_count = 0
        # 商品编码列表
        self.good_ids = []
        # 商品总页数
        self.page_nums = None
        # 商品总数
        self.good_nums = None
        # 价格修改按钮
        self.counts = 0
        # 在售商品和表格成功匹配的数据 商品编码：尺寸价格
        self.size_price_dict = {}

        # 增减价
        self.in_add_price = None
        # 运行间隔时间
        self.remove_time = None
        chrome_options = Options()
        desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
        desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        '''设置浏览器是否显示图片'''
        prefs = {"profile.managed_default_content_settings.images": 1}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument(
            "user-data-dir=C:\\Users\\Coolio\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="chromedriver.exe")
        self.wait = WebDriverWait(self.driver, 30, 0.5)
        self.driver.maximize_window()

    def main(self, price, remove_time):
        self.in_add_price = int(price)
        self.remove_time = int(remove_time)
        # 登录
        self.login_by_scan()
        try:
            start_time = datetime.now()
            self.log.info("程序开始时间：{}".format(start_time))
            # 获取在售商品信息
            self.get_total_page()
            # 获取所有在售商品编码
            self.get_gdis()

            # 开始主循环
            page_nums = int(self.page_nums) + 1
            for page_num in range(1, page_nums):
                self.log.info("开始修改第：{}页，共：{}页".format(page_num, self.page_nums))
                url = 'https://item.publish.taobao.com/taobao/manager/render.htm?pagination.current={}&pagination.pageSize=20&tab=on_sale'.format(
                    page_num)
                self.driver.get(url)
                # 进入下一页初始化价格修改位置按钮
                if page_num > 1:
                    self.counts = 0
                self.edit()
                # # 初始化 商品编码列表
                # self.good_ids = []
                # # 初始化 在售商品和表格成功匹配的数据 商品编码：尺寸价格
                # self.size_price_dict = {}
                # 页面刷新
                # self.driver.refresh()

            end_time = datetime.now()
            self.log.info("所有商品更新完成")
            self.log.info("总计更新{}条商品信息".format(self.edit_count))
            self.log.info("程序结束时间：{}".format(end_time))
            self.log.info("程序执行用时：{}s".format((end_time - start_time)))
            self.driver.close()
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
                # 进入在售商品页面
                self.driver.get("https://sell.taobao.com/auction/merchandise/auction_list.htm?type=11")
                break
            else:
                self.log.info("等待扫码中...")
                time.sleep(5)

    def get_total_page(self):
        """获取在售商品 总数 总页数 商品编码"""
        self.log.info("开始获取出售中的商品信息...")

        # 在售商品总数
        goods_num_id = self.wait.until(EC.presence_of_element_located((By.ID, 'list-pagination-top-total')))
        goods_num_text = goods_num_id.get_attribute("innerHTML")
        goods_num = re.search("\d+", goods_num_text)
        if goods_num is None:
            self.log.info("获取出售中的商品数量失败")
            return None
        self.good_nums = goods_num.group()
        self.log.info("出售中的商品数量：{}".format(goods_num.group()))

        # 在售商品总页数
        page_num_xpath = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="pagination-toolbar"]/div[2]/div/span')))
        page_num_text = page_num_xpath.text
        page_num = page_num_text.split('/')[-1]
        if page_num is None:
            self.log.info("获取出售中的商品总页数失败")
            return None
        self.page_nums = page_num
        self.log.info("出售中的商品总页数：{}".format(page_num))

    def get_gdis(self):
        """获取所有在售商品编码"""
        gsid_num = 0
        page_nums = int(self.page_nums) + 1
        for page_num in range(1, page_nums):
            if page_num > 1:
                url = 'https://item.publish.taobao.com/taobao/manager/render.htm?pagination.current={}&pagination.pageSize=20&tab=on_sale'.format(page_num)
                self.driver.get(url)
            self.log.info("获取第：{}页商品编码，共：{}页".format(page_num, self.page_nums))
            trs = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="list-table-desc-extend-cell"]')))
            for tr in trs:
                try:
                    tr_num = re.search(r'编码:(.*)', tr.text)
                    gsid = tr_num.group().replace('编码:', '')
                    self.good_ids.append(gsid)
                    gsid_num += 1
                except Exception as e:
                    tr_id = re.search(r'ID:(.*)', tr.text)
                    self.log.error("获取商品编码失败：{}".format(tr_id.group()))

            if len(self.good_ids) == 0:
                self.log.info("没有获取到有效的商品编码")
                return None
            self.log.info("当前页面获取到有效商品编码：{}".format(gsid_num))
        self.log.info("共获取到有效商品编码：{}".format(len(self.good_ids)))
        self.read_excel()

    def edit(self):
        """修改商品价格"""
        modify = 0
        good_ids = []
        trs = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="list-table-desc-extend-cell"]')))
        try:
            for tr in trs:
                gsids = re.findall(r'编码:(.*)', tr.text)
                if not len(gsids):
                    tr_id = re.search(r'ID:(.*)', tr.text)
                    self.log.error("{}获取商品编码失败,跳过修改".format(tr_id.group()))
                    self.counts += 2
                    continue

                for key in self.size_price_dict.keys():
                    if str(gsids[0]) != key:
                        # self.log.info("商品编码：{}没有匹配到数据,跳过修改".format(gsids[0]))
                        continue
                    good_ids.append(key)
                    # 定位隐藏属性
                    ActionChains(self.driver).move_to_element(tr).perform()
                    amend_xpath = '//i[@class="next-icon next-icon-edit2 next-icon-small table-cell-edit-icon"]'
                    amend = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, amend_xpath)))
                    print(amend[self.counts].is_displayed())
                    amend[self.counts].click()

                    time.sleep(self.remove_time)
                    self.log.info("\n\n开始修改商品：{}".format(key))
                    self.edit_min_price(key)
                    time.sleep(self.remove_time)
                    modify += 1
                    break
        except Exception as e:
            self.log.error(e)

            self.counts += 2
        # ActionChains(self.driver).move_to_element(self.driver.find_element_by_id('qn-workbench-head')).perform()
        # time.sleep(10)
        self.log.info("当前页面商品编码共匹配到Excel数据：{}条,修改成功{}条".format(len(good_ids), modify))
        self.log.info("修改成功商品编码：{}".format(good_ids))

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
                        if product == key:
                            is_match = True
                            product = key
                            break
                    if not is_match:
                        continue
                    size_price = row[15].value
                    size_price = self.parse_price(size_price)
                    # 在售商品和表格成功匹配的数据
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
        time.sleep(3)
        # 尺码
        SKUS = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="next-table-cell first"]')))
        # 价格
        input_box = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//td[@class="next-table-cell last"]/div/div/div/span/span//span/input')))
        original_price = str(input_box[count].get_attribute("value")).replace(".00", "")
        # excel 价目表
        price_dict = self.size_price_dict[key]

        for size in SKUS:
            size = str(size.text).split('/')[-1]

            if size not in price_dict.keys():
                self.log.info("商品编号：{} 尺码：{}==》原价：{} 未匹配到excel中的数据,不做修改".format(key, size, original_price))
                continue

            # 是否增减价格
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

            all_price.append(int(edit_value))
            count += 1
        list.sort(all_price)

        min_price = all_price[0]
        # 一口价
        price = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@name="price"]')))
        price_str = str(price.get_attribute("value")).replace('.00', '')
        price.send_keys(Keys.CONTROL, 'a')
        time.sleep(0.2)
        price.send_keys(Keys.BACK_SPACE)
        time.sleep(0.2)
        price.send_keys(min_price)
        self.log.info("商品编号：{} 一口价修改 {}==》{}".format(key, price_str, min_price))
        time.sleep(1)

        # 提交
        submit_btn = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="next-btn next-btn-normal next-btn-medium"]')))
        submit_btn[0].click()

        self.edit_count += 1


if __name__ == '__main__':
    bot = Spider()
    bot.main()
