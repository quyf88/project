"""数据处理DAO"""
import json
from com.baiduwords.feed_dao import FeedDao


class DataProcessingDao(FeedDao):
    def __init__(self):
        super().__init__()

    def handle(self, htmlstr):
        """数据处理"""

        # 剔除首部字符
        # htmlstr = htmlstr.replace('var eMVMZSCu={pages:5,data:', '')
        # 剔除尾部字符
        # htmlstr = htmlstr.strip('}')

        # 截取字符串
        htmlstr = htmlstr[27:-1]
        # json str 转换为 python list
        html_list = json.loads(htmlstr)

        data = []
        for row in html_list:
            data_list = list(row.values())

            fields = {}

            fields['sname'] = data_list[1]
            fields['hfqjg'] = float(data_list[2])
            fields['tdate'] = data_list[3]
            fields['close'] = float(data_list[5])
            fields['zdf'] = float(data_list[6])
            fields['zdf3'] = float(data_list[7])
            fields['zdf5'] = float(data_list[8])
            fields['zdf10'] = float(data_list[9])
            fields['AGSZBHXS'] = float(data_list[10])
            fields['rzye'] = float(data_list[11])
            fields['rzyezb'] = float(data_list[12])
            fields['rzmre'] = float(data_list[13])
            fields['rzmre3'] = float(data_list[14])
            fields['rzmre5'] = float(data_list[15])
            fields['rzmre10'] = float(data_list[16])
            fields['rzche'] = float(data_list[17])
            fields['rzche3'] = float(data_list[18])
            fields['rzche5'] = float(data_list[19])
            fields['rzche10'] = float(data_list[20])
            fields['rzjmre'] = float(data_list[21])
            fields['rzjmre3'] = float(data_list[22])
            fields['rzjmre5'] = float(data_list[23])
            fields['rzjmre10'] = float(data_list[24])
            fields['rqye'] = float(data_list[25])
            fields['rqyl'] = float(data_list[26])
            fields['rqmcl'] = float(data_list[27])
            fields['rqmcl3'] = float(data_list[28])
            fields['rqmcl5'] = float(data_list[29])
            fields['rqmcl10'] = float(data_list[30])
            fields['rqchl'] = float(data_list[31])
            fields['rqchl3'] = float(data_list[32])
            fields['rqchl5'] = float(data_list[33])
            fields['rqchl10'] = float(data_list[34])
            fields['rqjmcl'] = float(data_list[35])
            fields['rqjmcl3'] = float(data_list[36])
            fields['rqjmcl5'] = float(data_list[37])
            fields['rqjmcl10'] = float(data_list[38])
            fields['rzrqye'] = float(data_list[39])
            fields['rzrqyec'] = float(data_list[40])
            data.append(fields)

        # 保存数据到数据库
        for feedbackword in data:
            feeddao = FeedDao()
            feeddao.create(feedbackword)