# coding=utf-8
# 作者    ： Administrator
# 文件    ：设置程序自动运行时间.py
# IED    ：PyCharm
# 创建时间 ：2019/8/9 18:16


# -*- coding: utf-8 -*-
import sys
import pandas as pd
import re
import json
import requests
import time
import random
# sys.setdefaultencoding("utf-8")
# from login import Longin


class Crawl():
    def __init__(self, file_path, save_name, session):
        self.file_path = file_path
        self.save_name = save_name
        # 加载数据
        self.df = pd.read_excel(file_path)
        self.df_Data = pd.DataFrame(self.df)
        self.datas = self.read_xls()

        # 访问网址
        self.queryOtherUrl = 'https://amr.sz.gov.cn/aicmerout/command/ajax/com.inspur.gcloud.giapbase.aicmer.qydj.cmd.QydjUrlCxCmd/queryOtherUrl'
        self.Session = requests.Session()
        # 请求头
        self.headres = {
            # 最终网址
            'Cookie':
                '__jsluid_h=d1b72a9835b446f852a6df0ef9153bd2; yfx_c_g_u_id_10001435=_ck19081015034712898868910397172; yfx_f_l_v_t_10001435=f_t_1565420627273__r_t_1565420627273__v_t_1565420627273__r_c_0; pgv_pvi=1192167424; __jsluid_s=210c2622388df03ec8fa20cdb745369a; Hm_lvt_f89f708d1e989e02c93927bcee99fb29=1565420628; sangfor_cookie=85882078; isCaUser=true; isSameUser=DB43F867638230A81B20F2838A40CF7E; psout_sso_token=Ns1a2n0PbYiQxLNsteeFv-p; gdbsTokenId=AQIC5wM2LY4SfcyXijS9RmmKrxTKc3ATjXXF1fP4pfdUhww.*AAJTSQACMDMAAlNLABQtNDg1Njg0ODQ0NzIxNDM3OTMyNAACUzEAAjIw*@node27; accessToken=e3ecc874-65e4-4e31-b92b-d6914286e533@node27; userType=1; ishelp=false; JSESSIONID=0000HS3LrY8mHKEoFIO2cvS6LF6:-1',
            'Host': 'amr.sz.gov.cn',
            'Origin': 'https://amr.sz.gov.cn',
            'Referer': 'https://amr.sz.gov.cn/aicmerout/jsp/gcloud/giapout/industry/aicmer/processpage/step_one.jsp?ywType=30',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'}
        #
        self.load_url = "https://amr.sz.gov.cn/aicmerout/command/ajax/com.inspur.gcloud.giapbase.aicmer.formmgr.datamgr.cmd.AicmerBaseFormDataInitCmd/loadData"
        # 保存信息
        self.load_list = []
        self.count = 0

    def read_xls(self):
        df = self.df_Data
        print(df.keys())
        keys = ['企业名称', '省份', 'l联系电话', '城市', '统一社会信用代码', '法定代表人', '企业类型', '成立日期',
                '成立日期', '地址', '邮箱', '经营范围', '网址', '电话号码', '电话号码（更多号码）']
        pre_names = df['企业名称']
        pre_codes = df['统一社会信用代码']
        pre_privinces = df['所属省份']
        pre_citys = df['所属城市']
        pre_persons = df['法定代表人']
        pre_types = df['企业类型']
        pre_datas = df['成立日期']
        pre_prices = df['注册资本']
        pre_addresss = df['企业地址']
        pre_ranges = df['经营范围']
        # pre_site=df['网址']
        for pre_name, pre_privince, pre_code, pre_city, pre_person, pre_type, pre_data, pre_price, pre_address, pre_range in zip(
                pre_names, pre_privinces, pre_codes, pre_citys, pre_persons, pre_types, pre_datas, pre_prices,
                pre_addresss, pre_ranges):
            pre_base = {}
            pre_base['企业名称'] = pre_name
            pre_base['省份'] = pre_privince
            pre_base['城市'] = pre_city
            pre_base['统一社会信用代码'] = pre_code
            pre_base['法定代表人'] = pre_person
            pre_base['企业类型'] = pre_type
            pre_base['成立日期'] = pre_data
            pre_base['注册资本'] = pre_price
            pre_base['地址'] = pre_address
            pre_base['经营范围'] = pre_range
            yield pre_base

    def run(self):
        for query_data in self.datas:
            # print(query_data)
            pre_name = query_data['企业名称']
            pre_code = query_data['统一社会信用代码']
            print(pre_name, pre_code)
            pre_infos = self.Get_mid(pre_name, pre_code)

            try:
                primary_key = pre_infos['map']['map']['map']['id']
                html = self.Get_phone(primary_key)
                phone = self.parse(html)
                if phone == None:
                    print('primary_key', primary_key)
                query_data['联系方式'] = phone
                self.load_list.append(query_data)
                self.count += 1
                print("run{}".format(self.count))
            except Exception as e:
                pass
            time.sleep(random.randint(1, 3))
        self.save()

    # @property
    def save(self):
        df = pd.DataFrame(self.load_list)
        df.to_excel('{}'.format(self.save_name), sheet_name='data')
        print('end!')

    def Get_mid(self, pre_name, pre_code):
        """

        :param pre_name: 企业名称
        :param pre_code: 企业编号
        :return: 企业id
        """

        json_data = {"params": {"javaClass": "ParameterSet",
                                "map": {"bgContentType": "", "ywtype": "30", "regno": "{}".format(pre_code),
                                        "entName": "{}".format(pre_name), "isDivOrMer": "0",
                                        "isSecond": "0"}, "length": 6},
                     "context": {"javaClass": "HashMap", "map": {}, "length": 0}}
        # json_data = {"params": {"javaClass": "ParameterSet",
        #             "map": {"bgContentType": "", "ywtype": "30", "regno": "92440300MA5EQ7GQ4X",
        #                     "entName": "深圳市福田区西星美化妆品商行", "isDivOrMer": "0", "isSecond": "0"},
        #             "length": 7}, "context": {"javaClass": "HashMap", "map": {}, "length": 0}}
        infos = self.Session.post(self.queryOtherUrl, json=json_data, headers=self.headres)


        try:
            return infos.json()
        except Exception as e:
            print(e)
            print("失效")
            exit()

    def get_code(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'

            }
        url = 'https://amr.sz.gov.cn/aicmerout/validImageServlet'

        res = requests.session().get(url, headers=headers)
        with open('a.png', 'wb') as f:
            f.write(res.content)
        return input('验证码：')


    def Get_phone(self, key):
        """

        :param key: 企业id
        :return: 企业信息
        """

        # """id: "8a8084516a34e66c016a38f58bea0144"
        # infoflowId: "8a8a84d552fc7c940152fd49108e0004"
        # message: ""
        # nameid: "8a8084b06a2ae861016a38f57e7f785b"
        # opetype: "GS"
        # pripid: "440300000012019042312909"
        # state: "1"
        # url: "/jsp/gcloud/giapout/industry/aicmer/processpage/step_two.jsp"
        # ywtype: "30""""
        # {"params": {"javaClass": "ParameterSet",
        #             "map": {"formId": "SCZT_NZGS_BG_NW", "primaryKey": "8a8084516a34e66c016a38f58bea0144"},
        #             "length": 2}, "context": {"javaClass": "HashMap", "map": {}, "length": 0}}
        # json_key = {"params": {"javaClass": "ParameterSet",
        #                        "map": {"formId": "SCZT_NZGS_BG_NW", "primaryKey": "{}".format(key)},
        #                        "length": 2}, "context": {"javaClass": "HashMap", "map": {}, "length": 0}}

        json_key = {"params": {"javaClass": "ParameterSet", "map": {"formId": "SCZT_GTHBG",
                                                         "primaryKey": "{}".format(key),
                                                         "ywType": "30"}, "length": 3},
                    "context": {"javaClass": "HashMap", "map": {}, "length": 0}}

        infos = self.Session.post(self.load_url, json=json_key, headers=self.headres)
        return infos.text

    def Patter_phone_1(self):
        Patter_phone = '"FDDBR_GuDingDianHua":"\d+"'
        return Patter_phone

    def Patter_phone_2(self):
        Patter_phone = '"FDDBR_ShouJiHaoMa":"\d+"'
        return Patter_phone

    def parse(self, html):
        print('****', html.replace('\\', ''))
        Patter_phone = self.Patter_phone_1()
        text = re.findall(Patter_phone, html.replace('\\', ''))

        if text:
            phone_nums = re.findall('\d+', text[0])
            if len(phone_nums[0]) == 11:
                return phone_nums[0]
            else:
                Patter_phone = self.Patter_phone_2()
                text = re.findall(Patter_phone, html.replace('\\', ''))
                if text:
                    phone_nums = re.findall('\d+', text[0])
                    if len(phone_nums[0]) == 11:
                        return phone_nums[0]
                    else:
                        return ''
        else:
            Patter_phone = self.Patter_phone_2()
            text = re.findall(Patter_phone, html.replace('\\', ''))
            if text:
                phone_nums = re.findall('\d+', text[0])
                if len(phone_nums[0]) == 11:
                    return phone_nums[0]
                else:
                    return ''



if __name__ == '__main__':
    user = 'wyn16888'
    pwd = 'wyn16888'
    # Lg = Longin(user, pwd)
    session = requests.session()
    s = time.time()
    # 打开文件路径
    file_path = r'ceshi111.xlsx'
    # 保存文件名称
    save_name = 'ceshi2.xlsx'
    splider = Crawl(file_path, save_name, session)
    # splider.get_code()
    splider.run()
    print(time.time() - s)
    # text=splider.Get_phone('8a8084546a2b12f0016a2f672015053')
    # print(text)
    # phone = splider.parse(text)
    # print(phone)
    # print(data)
    #
    # datas=read_xls(file_path)
    # for data in datas:
    #     print(data)
