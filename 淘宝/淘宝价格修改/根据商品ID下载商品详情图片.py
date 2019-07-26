# -*- coding: utf-8 -*-
# @Time    : 2019/6/17 13:05
# @Author  : project
# @File    : 根据商品ID下载商品详情图片.py
# @Software: PyCharm
"""淘宝 根据商品ID 下载商品详情图片"""
import hashlib
import requests
import re
import time
import json


def get_images_from_mtop(num_iid):

    APPKEY = '12574478'
    DATA = '{"item_num_id":"%s"}' % num_iid
    URL = 'https://h5api.m.taobao.com/h5/mtop.wdetail.getitemdescx/4.9/'
    params = {'jsv': '2.4.11', 'appKey': APPKEY, 't': int(time.time()*1000),
              'sign': 'FAKE_SIGN_WITH_ANYTHING', 'api': 'mtop.wdetail.getItemDescx', 'v': '4.9',
              'type': 'jsonp', 'dataType': 'jsonp', 'callback': 'mtopjsonp2',
              'data': DATA}
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_4 like Mac OS X) AppleWebKit/601.1.46 ' + \
                      '(KHTML, like Gecko) Version/9.0 Mobile/13G35 Safari/601.1',
    }
    images = []
    try:
        # get token in first request
        r1 = requests.get(URL, params=params, headers=headers, verify=False)
        token_with_time = r1.cookies.get('_m_h5_tk')
        print(token_with_time)
        token = token_with_time.split('_')[0]
        enc_token = r1.cookies.get('_m_h5_tk_enc')
        print(r1.cookies)
        # get results in second request
        t2 = str(int(time.time() * 1000))
        c = '&'.join([token, t2, APPKEY, DATA])
        m = hashlib.md5()
        m.update(c.encode('utf-8'))
        params.update({'t': t2, 'sign': m.hexdigest()})
        print(params)
        cookies = {'_m_h5_tk': token_with_time, '_m_h5_tk_enc': enc_token}

        r2 = requests.get(URL, params=params, headers=headers, cookies=cookies, verify=False)
        # print(r2.text)
        json_text = re.match(r'(.*\()(.*)(\))', r2.text).group(2)
        images = dict(json.loads(json_text))['data']['images']
        print(images)
    except Exception as e:
        print(e)


shop_id = '554401452734'  # 商品ID
get_images_from_mtop(shop_id)
