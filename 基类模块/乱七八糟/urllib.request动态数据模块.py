"""获得动态数据"""

import urllib.request

from com.baiduwords.base_dao import BaseDao
from com.baiduwords.data_processing_dao import DataProcessingDao
from com.baiduwords.md5_dao import Md5Dao


class GetData(BaseDao):
    def __init__(self):
        super().__init__()

    def retrieve_data(self):
        """获取数据"""
        md5ojb = Md5Dao()
        data_processint = DataProcessingDao()

        url_list = ['http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=RZRQ_DETAIL_NJ&token=70f12f2f4f091e459a279469fe49eca5&filter=(scode=%27600000%27)&st=tdate&sr=-1&p=1&ps=50&js=var%20vsIEvvee={pages:(tp),data:(x)}&time=1&rt=51477765',
                    'http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=RZRQ_DETAIL_NJ&token=70f12f2f4f091e459a279469fe49eca5&filter=(scode=%27600000%27)&st=tdate&sr=-1&p=2&ps=50&js=var%20XrZRmnQz={pages:(tp),data:(x)}&time=1&rt=51477769',
                    'http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=RZRQ_DETAIL_NJ&token=70f12f2f4f091e459a279469fe49eca5&filter=(scode=%27600000%27)&st=tdate&sr=-1&p=3&ps=50&js=var%20kKVCFiPR={pages:(tp),data:(x)}&time=1&rt=51477775',
                    'http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=RZRQ_DETAIL_NJ&token=70f12f2f4f091e459a279469fe49eca5&filter=(scode=%27600000%27)&st=tdate&sr=-1&p=4&ps=50&js=var%20RSUEUqJS={pages:(tp),data:(x)}&time=1&rt=51477778',
                    'http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=RZRQ_DETAIL_NJ&token=70f12f2f4f091e459a279469fe49eca5&filter=(scode=%27600000%27)&st=tdate&sr=-1&p=5&ps=50&js=var%20aeTwPdBa={pages:(tp),data:(x)}&time=1&rt=51477780'
                    ]
        for url in url_list:

            req = urllib.request.Request(url)

            with urllib.request.urlopen(req) as response:
                data = response.read()
                htmlstr = data.decode('utf-8')  # 指定网页编码格式

            # 检查数据是否更新
            if md5ojb.dateupdate(htmlstr):

                # 数据更新处理数据
                data_processint.handle(htmlstr)


