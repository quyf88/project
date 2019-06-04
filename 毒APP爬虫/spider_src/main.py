import os
import time
import pandas
import logging
import hashlib
import requests
import asyncio
import traceback
import async_timeout
import multiprocessing
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from collections import OrderedDict
from twisted.internet import iocpreactor


from app.spider_src import db
from app.spider_src import config
from app.spider_src import frozen

# iocpreactor.install()
requests.packages.urllib3.disable_warnings()


if __name__ == '__main__':
    # 在此处添加
    multiprocessing.freeze_support()


class Crakeme:
    def __init__(self):
        self.cookcek = 'd41d8cd9%7C38667932%7C1548905083%7C3b52704520b7eea1'
        self.header = {
            'Connection': 'Keep-Alive',
            "User-Agent": "duapp/3.5.31(android;4.4.2)",
            'Accept-Encoding': 'gzip',
            "dudeviceTrait": "HUAWEI MLA-AL10",
            "duuuid": "b8868744a7af3160",
            "duplatform": "android",
            "duimei": "354730010184863",
            "duchannel": "huawei",
            "duv": "3.5.32",
            "duloginToken": "be5ca850|38667932|25f921d1b93471c9",
        }
        self.path = os.getcwd()

    def get_md5_str(self, dic):
        s = []
        for i in dic:
            temp = i + dic[i]
            s.append(temp)
        s = sorted(s)
        return self.hash_md5(s)

    def hash_md5(self, s):
        res = "".join(s) + "3542e676b4c80983f6131cdfe577ac9b"
        h1 = hashlib.md5()
        h1.update(res.encode(encoding='utf-8'))
        return h1.hexdigest()

    def my_logging(self):
        path = self.path + '\log\\'
        if not os.path.isdir(path):
            os.makedirs(path)
        m_log = logging.Logger('错误日志')
        mh = logging.FileHandler(path + 'main.log')
        mh.setLevel(logging.INFO)
        fmt = logging.Formatter('时间：%(asctime)s 文件名：%(filename)s 行号%(lineno)d')

        mh.setFormatter(fmt)
        m_log.addHandler(mh)

        return m_log


class Poison_spider:

    def __init__(self, config_new):

        self.header = {
            'Connection': 'Keep-Alive',
            "User-Agent": "duapp/3.5.31(android;4.4.2)",
            'Accept-Encoding': 'gzip',
            "dudeviceTrait": "HUAWEI MLA-AL10",
            "duuuid": "b8868744a7af3160",
            "duplatform": "android",
            "duimei": "354730010184863",
            "duchannel": "huawei",
            "duv": "3.5.31",
            "duloginToken": "be5ca850|38667932|25f921d1b93471c9",
        }
        cookcek = "d41d8cd9%7C38667932%7C1548905083%7C3b52704520b7eea1"
        self.cookie = {"duToken": cookcek}
        self.host = "http://du.hupu.com/"
        self.worker = Crakeme()
        self.config = config_new
        self.db = db.Db('test.db')

        try:
            os.mkdir("res")
        except:
            pass

    def send_req(self, url):
        """根据API URL 获取所有数据 json"""

        print('API：{}'.format(url))
        while True:
            try:
                # TODO
                response = requests.get(url, headers=self.header, cookies=self.cookie, verify=False, timeout=(15, 20))
                break
            except Exception as e:
                self.worker.my_logging().exception(e)
                print("请求出错：", str(e))
                pass
        return response

    def get_url_parma(self, dic):
        s = []
        for i in dic:
            temp = i + "=" + dic[i]
            s.append(temp)
        return "&".join(s)

    def make_url(self, dic, end_url, host=None):
        """拼接 API URL"""

        java_dic = {
            "v": "3.5.31",
            "loginToken": "be5ca850|38667932|25f921d1b93471c9",
            "platform": "android",
            "uuid": "b8868744a7af3160",
        }
        if host == None:
            host = self.host
        all_dic = dict(java_dic, **dic)
        sign = self.worker.get_md5_str(all_dic)  # 获取MD5码
        url_pre = self.get_url_parma(dic)
        host_url = host + end_url
        all_url = host_url + url_pre + "&sign=" + sign

        return all_url

    def get_goods_list(self, catId):
        """获取 商品详细信息列表"""

        url_dic = {"catId": str(catId)}
        end_url = "/search/categoryDetail?"
        response = self.send_req(self.make_url(url_dic, end_url))
        return response.json()['data']['list']

    def get_detail_list(self, goods_id, catId, page):
        """获取 商品json [data]"""

        url_dic = {
            "title": "",  # title=      title=
            "size": "[]",  # size=[]     size=[]
            "unionId": str(goods_id),  # unionId=144 limit=20
            "sortMode": "1",  # sortMode=1  sortMode=1
            "typeId": "0",  # typeId=0    typeId=0
            "sortType": "0",  # sortType=0  page=0
            "catId": str(catId),  # catId=0     catId=0
            "page": str(page),  # page=0      unionId=13
            "limit": "20",  # limit=20    sortType=0
        }
        end_url = "/search/list?"
        response = self.send_req(self.make_url(url_dic, end_url))
        return response.json()['data']

    def get_one_detail_all(self, goods_id, catId, page):
        """获取 商品信息列表[productList]"""

        result = []
        while True:
            temp_detail = self.get_detail_list(goods_id, catId, page)
            result += temp_detail['productList']
            # 根据当前商品页数循环完跳出
            page = temp_detail['page']
            if page == 0:
                break

        return result

    def get_product_detail(self, productId):
        url_dic = {
            "productId": str(productId),
            "isChest": "1"
        }
        end_url = "/product/detail?"
        r = self.send_req(self.make_url(url_dic, end_url))
        print(r.json)
        return r.json()

    def parse_html(self, html):
        """获取 品牌介绍文本"""
        soup = BeautifulSoup(str(html), 'lxml')
        text_tag = soup.find_all('p')
        text = ''
        for i in text_tag:
            text += i.get_text(strip=True)
        return text

    def parse_html_img(self, html):
        """解析图片"""

        soup = BeautifulSoup(str(html), 'lxml')
        img_tag = soup.find_all('img')
        img_src = []
        for i in img_tag:
            img_src.append(i['src'])
        return img_src

    def get_json_img(self, dic):
        img_src = []
        data = dic['data']
        for i in data['detail']['images']:
            img_src.append(i['url'])
        for i in data['relationTrends']['list']:
            if "images" in i['trends']:
                for j in i['trends']['images']:
                    img_src.append(j['url'])
        img_src.append(data['detail']['brandLogoUrl'])
        return img_src

    def save_file_name(self, file_name):
        unsave_string = r':\/:*<>"|?'
        for i in unsave_string:
            file_name = file_name.replace(i, "-")
        return file_name

    def make_pdfrm_data(self, dic):
        """数据保存"""

        data = dic['data']
        result = {
            "productId": data['detail']['productId'],
            "name": data['detail']['title'],
            "size_list": ",".join(data['detail']['sizeList']),
            "color": data['detail']['color'],
            "articleNumber": data['detail']['articleNumber'],
            "authPrice": data['detail']['authPrice'] / 100,
            "sellDate": data['detail']["sellDate"],
            "exchangeDesc": data["exchangeDesc"],
            "text": self.parse_html(data['imageAndText']),
            "soldNum": data['detail']['soldNum'],
        }
        try:
            if type(data['item']['price']) == str:
                data['item']['price'] = int(data['item']['price'])
            result["price"] = data['item']['price'] / 100
            if result["price"] == 0:
                result["price"] = "--"
        except:
            result["price"] = "--"
        key_list = ["name", "productId", "price", "size_list", "color", "articleNumber", "authPrice", "sellDate",
                    "exchangeDesc", "soldNum", "text"]
        # 把字典转换成有序模式
        order_result = OrderedDict()
        for i in key_list:
            order_result[i] = result[i]
        for i in data['sizeList']:
            key = i['size']
            try:
                if type(i['item']['price']) == str:
                    i['item']['price'] = int(i['item']['price'])
                order_result[key] = i['item']['price'] / 100
            except:
                order_result[key] = "--"
        return pandas.DataFrame(data=[order_result])

    async def fetch_json(self, session, productId):
        url_dic = {
            "productId": str(productId),
            "isChest": "1"
        }
        end_url = "/product/detail?"
        while True:
            try:
                with async_timeout.timeout(10):  # 设置线程超时时间
                    async with session.get(self.make_url(url_dic, end_url), headers=self.header) as response:
                        return await response.json()
            except Exception as e:
                self.worker.my_logging().exception(e)
                print("### TOP 请求超时 :", e)

    # def new_thead_excel(self, current_path, item_msg):
    #     """单线程 单独生成xlsx文档 不下载图片"""
    #
    #     self.excel_writer1("{}/{}.xlsx".format(current_path, self.save_file_name(item_msg['data']['detail']['title'])),
    #                        self.make_pdfrm_data(item_msg))

    async def run(self, brand_name, item, loop, sem):
        """
        多线程 生成xlsx文档，并下载图片
        breand_name : 商品品牌
        item : 商品信息详情 dict
        loop : 协程事件循环
        sem : 并发量
        """

        try:
            with (await sem):
                async with ClientSession(loop=loop, headers=self.header, cookies=self.cookie) as session:
                    item_msg = await self.fetch_json(session, item['productId'])
            current_path = "res/{}/{}".format(brand_name, self.save_file_name(item_msg['data']['detail']['title']))

            # 效验文件 是否存在 TODO
            if not os.path.isdir(current_path):
                os.mkdir(current_path)
                print("Created successfully：{}".format(current_path))
            else:
                print("{} is exist! 文件已存在".format(current_path))
                return

            await self.excel_writer(
                "{}/{}.xlsx".format(current_path, self.save_file_name(item_msg['data']['detail']['title'])),
                self.make_pdfrm_data(item_msg))
            await self.db_insert(item_msg, current_path, brand_name, loop)

        except BaseException as e:
            print("### run", str(e))
            traceback.print_exc()

    # async def db_insert(self, item_msg, current_path, brand_name, loop):
    #    """ 多线程 更新数据库"""
    #     img_src = self.parse_html_img(item_msg['data']['imageAndText']) + self.get_json_img(item_msg)
    #     msg = {"productId": item_msg['data']['detail']['productId'], "json_data": item_msg, "img_list": img_src}
    #     self.db.insert_detail(msg)
    #     if not self.db.query_basic_exists(msg):
    #         self.db.insert_basic_table(msg)
    #         if brand_name in ['Nike', 'Jordan', "adidas", "Supreme", "OFF-WHITE", "Y-3", "Champion", "Bounce"]:
    #             await self.img_downloader(current_path, img_src, loop)
    #     else:
    #         self.db.update(msg)
    #         if self.db.query_diff_exists(msg):
    #             self.db.insert_diff_table(msg)
    #         else:
    #             self.db.insert_diff_table(msg)

    async def db_insert(self, item_msg, current_path, brand_name, loop):
        """多线程  写入数据库"""
        img_src = self.parse_html_img(item_msg['data']['imageAndText']) + self.get_json_img(item_msg)
        msg = {"productId": item_msg['data']['detail']['productId'], "json_data": item_msg, "img_list": img_src}
        if self.config.is_first:
            self.db.insert_detail(msg)
            self.db.insert_temp_table(msg)
            # await self.img_downloader(current_path, img_src, loop)
        else:
            self.db.insert_temp_table(msg)
            if self.config.go_img:
                await self.img_downloader(current_path, img_src, loop)

    async def excel_writer(self, path, msg):
        """多线程 xlsx文档写入"""

        try:
            print("{} EXCEL WRITing....".format(path))
            excel_writer = pandas.ExcelWriter(path)
            pdfrm = pandas.DataFrame(data=msg)
            pdfrm.to_excel(excel_writer)
            excel_writer.save()
            print("{} EXCEL WRITE OVER!".format(path))
            del excel_writer
            del pdfrm
        except Exception as e:
            # 错误日志
            self.worker.my_logging().exception(e)
            print("excel wirte error! error : {}".format(path))

    # def excel_writer1(self, path, msg):
    #     """单线程 xlsx文档写入"""
    #     try:
    #         print("{} EXCEL WRITing....".format(path))
    #         excel_writer1 = pandas.ExcelWriter(path)
    #         pdfrm = pandas.DataFrame(data=msg)
    #         pdfrm.to_excel(excel_writer1)
    #         excel_writer1.save()
    #         print("{} EXCEL WRITE OVER!".format(path))
    #     except:
    #         print("excel wirte error! error : {}".format(path))

    async def fetch(self, session, url):
        url = url.replace("%5C%22", "")
        n = 0
        while True:
            try:
                async with session.get(url, headers=self.header, verify_ssl=False, timeout=20) as response:
                    return await response.read()
            except BaseException as e:
                n += 1
                if n >= 5:
                    self.worker.my_logging().exception(e)
                    raise ValueError("img requests error! url : {}".format(url))

    async def img_downloader(self, path, url_list, loop):
        """
        多线程 下载 商品图片
        path : 商品文件夹名
        url_list : 图片URL
        loop : 协程事件循环
        """

        print("now write img {} ...".format(path))
        for i in url_list:
            print("*img url :", i)
            time_now = time.time()
            n = 0
            while True:
                try:
                    async with ClientSession(loop=loop) as session:
                        r = await self.fetch(session, i)
                    img_name = i.split("/")[-1]
                    if "." not in img_name:
                        img_name += ".jpg"
                    await self.img_save(path, img_name, r)
                    break
                except BaseException as e:
                    n += 1
                    if n >= 10:
                        print("***", str(e))
                        break
                    if time.time() - time_now > 30:
                        break
        print("img path : {} complete!".format(path))

    async def img_req(self, url):
        n = 0
        while True:
            try:
                r = requests.get(url, headers=self.header, timeout=(5, 10), verify=False)
                return r.content
            except BaseException as e:
                n += 1
                if n >= 5:
                    self.worker.my_logging().exception(e)
                    raise ValueError("normal request also error!")

    async def img_save(self, path, img_name, r):
        """
        多线程 保存图片
        :param path: 路径
        :param img_name: 图片名称
        :param r: content
        :return: None
        """
        with open("{}/{}".format(path, img_name), 'wb+') as f:
            f.write(r)
            print('Get the picture successfully：{}'.format(img_name))


brand_list = [{'brandName': 'Nike', 'goodsBrandId': 144},
              {'brandName': 'Jordan', 'goodsBrandId': 13},
              {'brandName': 'adidas original', 'goodsBrandId': 494},
              #  {'brandName': 'Supreme', 'goodsBrandId': 439},
              #  {'brandName': 'KITH', 'goodsBrandId': 10038},
              #  {'brandName': 'THE NORTH FACE', 'goodsBrandId': 45},
              #  {'brandName': 'A BATHING APE', 'goodsBrandId': 634},
              #  {'brandName': 'Apple', 'goodsBrandId': 65},
              #  {'brandName': 'Randomevent', 'goodsBrandId': 10039},
              #  {'brandName': 'C2H4', 'goodsBrandId': 10037},
              #  {'brandName': 'Puma', 'goodsBrandId': 2},
              #  {'brandName': '李宁', 'goodsBrandId': 33},
              #  {'brandName': 'CASIO', 'goodsBrandId': 843},
              #  {'brandName': 'adidas', 'goodsBrandId': 3},
              #  {'brandName': 'OFF-WHITE', 'goodsBrandId': 1245},
              #  {'brandName': 'OFF-WHITE', 'goodsBrandId': 1245},
              #  {'brandName': 'Vans', 'goodsBrandId': 9},
              #  {'brandName': 'CONVERSE', 'goodsBrandId': 176},
              #  {'brandName': 'New Balance', 'goodsBrandId': 4},
              #  {'brandName': 'Under Armour', 'goodsBrandId': 7},
              #  {'brandName': 'NOAH', 'goodsBrandId': 1222},
              #  {'brandName': 'Kaws', 'goodsBrandId': 421},
              #  {'brandName': 'FR2', 'goodsBrandId': 4992},
              #  {'brandName': 'CarharttWIP', 'goodsBrandId': 10030},
              #  {'brandName': 'Asics', 'goodsBrandId': 8},
              #  {'brandName': 'LEGO', 'goodsBrandId': 2389},
              #  {'brandName': '虎扑优选', 'goodsBrandId': 4981},
              #  {'brandName': 'Reebok', 'goodsBrandId': 6},
              #  {'brandName': 'PALACE', 'goodsBrandId': 577},
              #  {'brandName': 'Champion', 'goodsBrandId': 1310},
              #  {'brandName': 'ROARINGWILD', 'goodsBrandId': 10000},
              #  {'brandName': 'Cav Empt', 'goodsBrandId': 10021},
              #  {'brandName': 'BANDAI', 'goodsBrandId': 10024},
              #  {'brandName': 'Revenge Storm', 'goodsBrandId': 4985},
              #  {'brandName': '安踏', 'goodsBrandId': 34},
              #  {'brandName': 'PLACES+FACES', 'goodsBrandId': 10017},
              #  {'brandName': '大疆', 'goodsBrandId': 10018},
              #  {'brandName': 'DICKIES', 'goodsBrandId': 10027},
              #  {'brandName': 'Alpha Industries', 'goodsBrandId': 10031},
              #  {'brandName': 'Thrasher', 'goodsBrandId': 10001},
              #  {'brandName': 'KENZO', 'goodsBrandId': 10014},
              #  {'brandName': 'Vetements', 'goodsBrandId': 10016},
              #  {'brandName': 'Givenchy', 'goodsBrandId': 10019},
              #  {'brandName': 'OMEGA', 'goodsBrandId': 4988},
              #  {'brandName': 'LONGINES', 'goodsBrandId': 10022},
              #  {'brandName': 'Medicom Toy', 'goodsBrandId': 4991},
              #  {'brandName': 'Fucking Awesome', 'goodsBrandId': 4993},
              #  {'brandName': 'McQ', 'goodsBrandId': 10029},
              #  {'brandName': 'THOM BROWNE', 'goodsBrandId': 1860},
              #  {'brandName': 'Hasbro', 'goodsBrandId': 10033},
              #  {'brandName': 'dyson', 'goodsBrandId': 10035},
              #  {'brandName': 'UNDERCOVER', 'goodsBrandId': 3023},
              #  {'brandName': 'Y-3', 'goodsBrandId': 10002},
              #  {'brandName': 'Balenciaga', 'goodsBrandId': 10012},
              #  {'brandName': 'Neil Barrett', 'goodsBrandId': 10013},
              #  {'brandName': 'FOG', 'goodsBrandId': 10082},
              #  {'brandName': 'Bounce', 'goodsBrandId': 10084}
              ]


def make_thead(poison, brand):
    """
    创建目录文件夹
    poison : 主程序
    brand : 主目录
    breand_name : 商品品牌
    item : 商品信息详情 dict
    loop : 协程事件循环
    sem : 并发量
    """
    brand_name = brand['brandName']
    brand_id = brand['goodsBrandId']
    # print("{} is finding...".format(brand_name))
    print("{} 获取中...".format(brand_name))
    # 商品信息列表[productList]
    detail_list = poison.get_one_detail_all(brand_id, 0, 0)

    # TODO 效验文件是否存在
    if not os.path.isdir("res/{}".format(brand_name)):
        os.mkdir("res/{}".format(brand_name))
        print("Created successfully：res/{}!".format(brand_name))

    # 创建一个新的事件循环
    loop = asyncio.new_event_loop()
    # 设置事件循环为当前线程的事件循环
    asyncio.set_event_loop(loop)
    if brand_name == "Nike":
        x1 = 0
        x2 = 1000
        split_list = []
        while True:
            temp = detail_list[x1:x2]
            if temp:
                split_list.append(temp)
                x1 = x2
                x2 += 1000
            else:
                break
        for detail_list in split_list:
            # 设置并发量 TODO
            sem = asyncio.Semaphore(5)
            # ensure_future 创建task对象
            coros = [asyncio.ensure_future(poison.run(brand_name, item, loop, sem)) for item in detail_list]
            loop.run_until_complete(asyncio.gather(*coros))
    else:
        sem = asyncio.Semaphore(10)
        coros = [asyncio.ensure_future(poison.run(brand_name, item, loop, sem)) for item in detail_list]
        loop.run_until_complete(asyncio.gather(*coros))
    print("{} is complete!!!!...".format(brand_name))


def init_lock(l):
    global lock
    lock = l


def run(conf):
    with open("数据生成日期.txt", "a+", encoding="utf-8") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
        f.write("\n")

    # 实例化主程序对象 TODO
    poison = Poison_spider(conf)
    # 创建进程池
    lock = multiprocessing.Lock()
    pool = multiprocessing.Pool(processes=4, initializer=init_lock, initargs=(lock,))

    # 启动异步进程
    for brand in brand_list:
        pool.apply_async(make_thead, (poison, brand,))
    pool.close()
    pool.join()

    # 数据库连接
    print("now is compare two table....")
    poison.db.compare_table()
    poison.db.change_db_name()
    poison.db.delete_same()
    print("table compare compleate!")
    # 生成数据汇总xlsx
    if conf.is_write_excel:
        print("now is writing excel...")
        import ExcelSummary
        bigexecl = ExcelSummary.BigExcel()
        data = poison.db.query_all_detail()
        bigexecl.run(data)
        print("excel all have done!")
    with open("数据生成时间日志.txt", "a+", encoding="utf-8") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
        f.write("\n")


if __name__ == '__main__':
    multiprocessing.freeze_support()
    conf = config.Config(go_img=False)
    run(conf)