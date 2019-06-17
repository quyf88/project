# -*- coding: utf-8 -*-
# @Time    : 2019/6/17 13:05
# @Author  : project
# @File    : 123.py
# @Software: PyCharm


from urllib.parse import quote


a = [{'domain': 'mall.icbc.com.cn', 'expiry': 1560832432, 'httpOnly': False, 'name': 'BROWSE_GOODS', 'path': '//', 'secure': False, 'value': 'e9a7c962-da87-46df-81b1-d43ccd60189c'}, {'domain': 'mall.icbc.com.cn', 'expiry': 1560770105, 'httpOnly': False, 'name': 'MALLID', 'path': '//', 'secure': False, 'value': '85851fda-0c20-44a4-9045-af0436fa2d9d'}, {'domain': 'mall.icbc.com.cn', 'httpOnly': False, 'name': 'MALL_SHOPCAR', 'path': '//', 'secure': False, 'value': '35876138-d221-4328-831f-75ffd67e80fa'}, {'domain': 'mall.icbc.com.cn', 'httpOnly': True, 'name': 'SESSION', 'path': '//', 'secure': False, 'value': '6a40e228-86b5-46a0-a26a-268bb76af330'}, {'domain': 'icbc.com.cn', 'httpOnly': False, 'name': 'ar_stat_ss', 'path': '//', 'secure': False, 'value': '4273772146_1_1560784506_9999'}, {'domain': 'icbc.com.cn', 'expiry': 1875329315, 'httpOnly': False, 'name': 'ar_stat_uv', 'path': '//', 'secure': False, 'value': '65685819188582272697|9999'}, {'domain': 'mall.icbc.com.cn', 'expiry': 1563338455, 'httpOnly': False, 'name': 'deliveryInfo', 'path': '//', 'secure': False, 'value': '{"cityId":"110000","provinceId":"119999","coutryId":"110106"}'}, {'domain': 'mall.icbc.com.cn', 'expiry': 1560832432, 'httpOnly': False, 'name': 'historyLookUp', 'path': '//', 'secure': False, 'value': '9000874368_9000727005_9000936967'}, {'domain': 'mall.icbc.com.cn', 'expiry': 1875065096, 'httpOnly': False, 'name': 'usertrack', 'path': '//', 'secure': False, 'value': '10.161.17.61.1559705096463573'}, {'domain': 'mall.icbc.com.cn', 'expiry': 1561349949, 'httpOnly': False, 'name': 'zoneNo', 'path': '//', 'secure': False, 'value': '%E5%8C%97%E4%BA%AC_0200'}]


for k in a:
    print('{}={}; '.format(k['name'], k['value']))



