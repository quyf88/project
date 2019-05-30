# coding=utf-8
# 作者    ： Administrator
# 文件    ：get_comment.py
# IED    ：PyCharm
# 创建时间 ：2019/5/30 22:21


import requests
from retrying import retry


class GetComment:
    def __init__(self):
        super().__init__()

        self.headers = {'User-Agent':
                        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                        ' Chrome/59.0.3071.104 Safari/537.36'
                        }
        self.cookie = {'_T_WM': '31576192650',
                       ' SCF': 'AiijZBWTC3cK4xjwOUz27rnhXM13IutsjntDNytulWwnuWiLzenrdulnr8RBLmKClrJFMRwCfY1hieUEs9bbS7g.',
                       ' MLOGIN': '1',
                       ' SUB': '_2A25x65U1DeRhGeBO4lEV9ybJyD2IHXVTFzt9rDV6PUJbkdAKLXPxkW1NRbX_QKAlFu3rCiwBBYhdRhowWvMWmW_4',
                       ' SUHB': '0h1J1PizDoA8ye', ' SSOLoginState': '1559225701',
                       ' M_WEIBOCN_PARAMS': 'lfid%3D102803%26luicode%3D20000174'
                       }

    @retry(stop_max_attempt_number=3)
    def run(self):
        url = 'https://m.weibo.cn/api/comments/show?id=4377707464827773&page={}'.format(1)
        response = requests.get(url, headers=self.headers, cookies=self.cookie, timeout=3)

        print(response.json())


if __name__ == '__main__':
    comment = GetComment()
    comment.run()