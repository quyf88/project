"""url请求模块"""
from time import sleep
import requests
from retrying import retry
from yingping.maoyan.headers_dao import GetUserAgent


class ParseDao:

    @retry(stop_max_attempt_number=3)
    # 如果请求超时让被装饰的函数反复执行三次，三次全部报错才会报错
    def _parse_url(self, url):
        sleep(3)
        print('休息{0}秒'.format('5'))
        print('*' * 20)
        print(url)

        # 随机获取一个请求头
        headers = GetUserAgent().user_agent_list()
        
        response = requests.get(url, headers=headers, timeout=3)  # 3秒无响应报错

        return response.content.decode()

    def parse_url(self, url):
        try:
            html_str = self._parse_url(url)
        except:
            html_str = None
            print('数据为{0}'.format(html_str))
        return html_str

