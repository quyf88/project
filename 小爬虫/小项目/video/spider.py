# coding=utf-8
# 作者    ： Administrator
# 文件    ：spider.py
# IED    ：PyCharm
# 创建时间 ：2019/8/31 14:36

import os
import re
import time
import shutil
import logging
import datetime
from lxml import etree
from retrying import retry
from multiprocessing import Pool
from fake_useragent import UserAgent
import urllib.request, urllib.error, requests
import socket
socket.setdefaulttimeout(30)  # 设置超时时间


class Spider:
    def __init__(self):
        # self.log = self.log_init()
        self.headers = {'user-agent': str(UserAgent().random),
                        'authority': 'cdn.av01.tv',
                        'method': 'GET',
                        'scheme': 'https',
                        'accept': '*/*',
                        'origin': 'https://www.av01.tv',
                        'referer': 'https://www.av01.tv/video/26791/ssni-452-%E4%B8%8B%E7%9D%80%E3%83%A2%E3%83%87%E3%83%AB%E3%82%92%E3%81%95%E3%81%9B%E3%82%89%E3%82%8C%E3%81%A6-%E3%83%95%E3%82%A7%E3%83%81%E3%82%BA%E3%83%A09%E3%83%A9%E3%83%B3%E3%82%B8%E3%82%A7%E3%83%AA%E3%83%BCspecial-%E4%B8%89%E4%B8%8A%E6%82%A0%E4%BA%9C',

                        }
        self.proxies = {
            "http": "http://127.0.0.1:1080",
            "https": "https://127.0.0.1:1080"
            }
        # 视频路径
        self.path = None
        # TS文件数量
        self.movies_url = None

    # def log_init(self):
    #     """日志模块"""
    #     path = os.path.abspath('.') + r'\log\spider.log'
    #     formatter = logging.Formatter('%(asctime)s | %(name)-6s | %(levelname)-6s| %(message)s')
    #     console = logging.StreamHandler()
    #     console.setLevel(logging.DEBUG)
    #     fh = logging.FileHandler(path, encoding='utf-8', mode='a+')
    #     fh.setLevel(logging.DEBUG)
    #     fh.setFormatter(formatter)
    #     console.setFormatter(formatter)
    #     # 如果需要同時需要在終端上輸出，定義一個streamHandler
    #     # print_handler = logging.StreamHandler()  # 往屏幕上输出
    #     # print_handler.setFormatter(formatter)  # 设置屏幕上显示的格式
    #     logger = logging.getLogger("spider")
    #     # logger.addHandler(print_handler)
    #     logger.setLevel(logging.DEBUG)
    #     logger.addHandler(console)
    #     logger.addHandler(fh)
    #     return logger

    @retry(stop_max_attempt_number=3)
    def get_video_url(self):
        """
        获取指定女优所有视频url
        :return:
        """
        for i in range(1, 6):
            url = 'https://www.av01.tv/search/videos?actress=%E4%B8%89%E4%B8%8A%E6%82%A0%E4%BA%9C&id=216&page={}'.format(i)
            print(url)
            response = requests.get(url, headers=self.headers, timeout=30)
            response = response.content.decode('utf-8')
            print(response)
            result = etree.HTML(response)
            url_list = result.xpath('//*[@class="well well-sm "]/a/@href')
            # print(url_list)
            with open('config/url.txt', 'a', encoding='utf-8') as f:
                for _url in url_list:
                    _url = 'https://www.av01.tv' + _url
                    print(_url)
                    f.write(_url)
                    f.write('\n')

    def read_url(self):
        """
        读取配置文件 url
        :return:
        """
        with open('config/url.txt', 'r', encoding='UTF-8') as f:
            urls = f.readlines()

        return urls

    @retry(stop_max_attempt_number=3)
    def get_summary(self, url):
        """
        获取视频摘要信息
        :return:
        """
        response = requests.get(url, headers=self.headers, timeout=30)
        response = response.content.decode('utf-8')
        result = etree.HTML(response)

        # 日期 番号
        date_number = result.xpath('//div[@id="id_list"]//text()')
        if date_number:
            date_number = [i for i in date_number if i.replace('\n', '').replace(' ', '')]
        # 女优
        Female = result.xpath('//div[@id="actresses"]//text()')
        if Female:
            Female = [i for i in Female if i.replace('\n', '').replace(' ', '')]
        # 分类
        sort = result.xpath('//div[@id="tags_list"]//text()')
        if sort:
            sort = [i for i in sort if i.replace('\n', '').replace(' ', '')]
        # 系列
        series = result.xpath('//div[@id="series"]//text()')
        if series:
            series = [i for i in series if i.replace('\n', '').replace(' ', '')]
        # 制作商
        maker = result.xpath('//div[@id="maker"]//text()')
        if maker:
            maker = [i for i in maker if i.replace('\n', '').replace(' ', '')]
        # 简介
        description_tc = result.xpath('//div[@id="description_tc"]//text()')
        if description_tc:
            description_tc = [i for i in description_tc if i.replace('\n', '').replace(' ', '')]
        description = result.xpath('//div[@id="description"]//text()')
        if description:
            description = [i for i in description if i.replace('\n', '').replace(' ', '')]

        content = [date_number, Female, sort, series, maker, description_tc, description]
        return content, date_number[-1:]

    def video_path(self, series):
        """
        构造视频保存地址
        :return:
        """
        # os.sep 根据系统自动选择适合的拼接拼接符
        self.path = os.getcwd() + os.sep + 'video' + os.sep + series[0]
        # print(f'视频保存地址：{self.path}')
        # self.log.info(f'视频保存地址：{self.path}')
        if not os.path.exists(self.path):
            os.mkdir(self.path)
            return
        files = os.listdir(self.path)
        print(files)
        if series[0] + '.mp4' in files:
            print('当前视频已经下载!')
            return True

    def save_video_info(self, content, series):
        """
        保存视频基本信息
        :return:
        """
        path = self.path + os.sep + series[0] + '.txt'
        with open(path, 'w+', encoding='UTF-8') as f:
            for i in content:
                for k in i:
                    f.write(k)
                f.write('\n')
            print('视频 {} 基本信息保存成功!'.format(series[0]))
            # self.log.info('视频 {} 基本信息保存成功!'.format(series[0]))

    def get_m3u8(self, url):
        """
        获取视频TS流下载地址
        :return:
        """
        res = requests.get("http://httpbin.org/ip", headers=self.headers, proxies=self.proxies, verify=False, timeout=10).json()
        ip = str(res['origin']).split(',')
        print(ip)
        # url = 'https://cdn.av01.tv/v2/20190423_2/ssni00452/content/index4500-v1.m3u8?hdnea=ip=193.38.139.232~st=1567914459~exp=1568000859~acl=/v2/20190423_2/ssni00452/content/*~hmac=49a05a8ea1dd09464a2e8dcac677fb371d204a0042038f9dabdfe57e5349d270'
        response = requests.get(url, headers=self.headers, timeout=30)
        with open('config/m3u8_url.txt', 'w') as m3u8_content:
            m3u8_content.write(response.text)
        print('成功获取m3u8视频下载URL!')

    def get_url(self, m3u8_url):
        # 提取请求头
        headred = re.findall(r'^(.*?)index', m3u8_url)[0]
        # 提取ts视频的url
        movies_url = []
        _urls = open('config/m3u8_url.txt', 'r')
        for line in _urls.readlines():
            if '.ts' in line:
                # movies_url.append('https://cdn.av01.tv/v2/20190423_2/ssni00452/content/' + line)
                # 根据具体视频修改
                movies_url.append(headred + line)
            else:
                continue
        print(f'共：{len(movies_url)} 个TS文件')
        self.movies_url = len(movies_url)
        for url in movies_url:
            yield url

    def user_proxy(self, proxy_addr, url):
        """
        添加代理
        :param url:
        :return:
        """
        proxy = urllib.request.ProxyHandler({'http://': proxy_addr, 'https://': proxy_addr})
        # 创建opener
        opener = urllib.request.build_opener(proxy)
        # 安装opener，此后调用urlopen()时都会使用安装过的opener对象
        urllib.request.install_opener(opener)
        data = urllib.request.urlopen(url).read().decode('utf-8')
        return data

    @retry(stop_max_attempt_number=3)
    def get_video(self, video_url):
        # 效验代理是否添加成功
        # res = requests.get("http://httpbin.org/ip", headers=self.headers, proxies=self.proxies, timeout=10).json()
        # ip = str(res['origin']).split(',')
        # print(ip)

        # 构造当前下载视频文件名
        num = re.findall(r'file4500-(.*?)-v1', video_url)[0]
        start = datetime.datetime.now().replace(microsecond=0)
        ts_path = self.path + os.sep + num + '.ts'
        # 效验当前视频是否已下载
        path_list = os.listdir(self.path)
        path_list = [i for i in path_list if 'ts' in i]
        if num + '.ts' in path_list:
            print(f'{num + ".ts"}已下载,跳过!!!')
            return
        try:
            urllib.request.urlretrieve(video_url, ts_path)
        except socket.timeout:  # 当前进程超时会走下面的流程
            count = 1
            while count <= 3:
                try:
                    urllib.request.urlretrieve(video_url, ts_path)
                    break
                except socket.timeout:
                    err_info = 'Reloading for %d time' % count if count == 1 else 'Reloading for %d times' % count
                    print(err_info)
                    count += 1
            if count > 3:
                print("downloading picture fialed!")

        end = datetime.datetime.now().replace(microsecond=0)
        print("{} 下载完成 耗时：{}".format(num + '.ts', end - start))

    def ts_to_pm4(self, series):
        """
        合并TS视频文件,输出为MP4
        os.popen(f'copy/b {files} {new_path}') 合并上限为100个文件
        """
        # 读取指定目录下的ts文件列表
        path_list = os.listdir(self.path)
        ts_list = [i for i in path_list if 'ts' in i]
        # 效验是否下载完整
        if self.movies_url == len(ts_list):
            print('数据效验成功,已全部下载!')
        # lambda 剔除
        # 按照文件名顺序排序(数字)
        ts_list.sort(key=lambda x: int(x[:-3]))
        # 拼接ts文件绝对路径,os.sep自适应路径拼接符
        ts_list = [self.path + os.sep + i for i in ts_list]
        # 用+把需要合并的ts文件拼接起来
        files = '+'.join(ts_list)
        print(len(ts_list))
        # 判断TS文件数量
        if len(ts_list) > 100:
            count = 1
            for i in range(0, len(ts_list), 100):
                print(f'i:{i}')
                # 一次提取400个TS文件用于合并
                _path = ts_list[i:i + 100]
                # 用+把需要合并的ts文件拼接起来
                files = '+'.join(_path)
                # 合并后小段mp4文件名称
                new_path = self.path + os.sep + str(count) + '.mp4'
                # 合并ts视频 为MP4
                res = os.popen(f'copy/b {files} {new_path}')
                print(res.read())
                print(f'{series[0]}_{count} 视频合并成功!')
                count += 1
            # 删除ts文件
            p = self.path + os.sep + '*.ts'
            os.system(f'del /Q {p}')
            print(f'{series[0]} TS缓存文件删除成功!')

            # 把小段MP4视频合并为完整视频
            while True:
                # 合并为一个MP4文件
                print('等待缓存文件写入')
                time.sleep(3)
                path_list = os.listdir(self.path)
                mp4_list = [i for i in path_list if 'mp4' in i]
                mp4_list.sort(key=lambda x: int(x[:-4]))
                print(mp4_list)
                if not len(mp4_list):
                    continue
                mp4_list = [self.path + os.sep + i for i in mp4_list]
                files = '+'.join(mp4_list)
                # 合并ts视频 为MP4
                mp4_path = self.path + os.sep + series[0] + '.mp4'
                print('视频转码合并中')

                res = os.popen(f'copy/b {files} {mp4_path}')
                print(res.read())
                print('视频合并成功!')
                break

        else:
            # mp4文件名称
            new_path = self.path + os.sep + series[0] + '.mp4'
            # 合并ts视频 为MP4
            res = os.popen(f'copy/b {files} {new_path}')
            print(res.read())
            print(f'{series[0]} 视频合并成功!')
            # 删除ts和m3u8文件
            p = self.path + os.sep + '*.ts'
            os.system(f'del /Q {p}')
            print(f'{series[0]} TS缓存文件删除成功!')

    def run(self, url, m3u8_url):
        print('*'*20, '程序启动', '*'*20)
        count = 1
        # 读取配置文件url
        print('读取配置文件,读取URL')
        # self.log.info('读取配置文件,读取URL')
        # for url in self.read_url():
        # 获取视频摘要信息
        content, series = self.get_summary(url)
        print(content, series)
        # self.log.info(f'{content}, {series}')
        print(f'----{series[0]} 视频下载中----')
        print('效验代理成功!')
        # self.log.info(f'----{series[0]} 视频下载中----')
        # 构造视频保存路径
        if self.video_path(series):
            return
        # 保存视频基本信息
        self.save_video_info(content, series)
        # 获取TS流URL地址
        self.get_m3u8(m3u8_url)
        # 视频下载
        # 创建进程池,执行20个任务
        print('创建进程池')
        pool = Pool(30)
        for video_url in self.get_url(m3u8_url):
            # 启动线程
            pool.apply_async(self.get_video, (video_url,))
            count += 1
            # if count > 500:
            #     break
        pool.close()
        pool.join()
        print('TS文件下载完成,合并中...')
        # self.log.info('TS文件下载完成,合并中...')
        time.sleep(3)
        # TS合并文件为MP4
        self.ts_to_pm4(series)
        content = {'content': [series[0], self.path, url]}
        # print(content)
        print('*' * 50, '\n')
        # os._exit(0)
        print('End of program execution')
        # self.log.info('End of program execution')


if __name__ == '__main__':
    # url = 'https://www.av01.tv/video/29379/miaa-155-%E9%83%A8%E4%B8%8B%E3%81%AE%E5%BE%A1%E4%B8%96%E8%BE%9E%E3%82%92%E5%A5%BD%E6%84%8F%E3%81%A8%E5%8F%97%E3%81%91%E5%8F%96%E3%81%A3%E3%81%9F-%E3%82%BB%E3%82%AF%E3%83%8F%E3%83%A9%E4%B8%8A%E5%8F%B8%E3%81%AE%E8%83%8C%E4%B8%AD%E3%81%BE%E3%81%A7%E5%B1%8A%E3%81%8F%E3%82%82%E3%81%AE%E5%87%84%E3%81%84%E5%B0%BB%E5%B0%84-%E7%AF%A0%E7%94%B0%E3%82%86%E3%81%86'
    # m3u8_url = 'https://cdn.av01.tv/v2/20190911_3/miaa00155/content/index4500-v1.m3u8?hdnea=ip=139.28.235.118~st=1568863059~exp=1568949459~acl=/v2/20190911_3/miaa00155/content/*~hmac=146cd1d663e5d7bc1ddd490a1979e7a9f45c06f9ba83501c7ba47294b3b22ea1'
    # m3u8 播放地址
    spider = Spider()
    # spider.get_video_url()  # 获取指定女优所有视频URL地址
    with open('config/url.txt', 'r', encoding='utf-8') as f:
            urls = f.readlines()
            urls = [i.replace('\n', '') for i in urls]
    for url in urls:
        print(url)
        m3u8_url = input('m3u8地址：')
        spider.run(url, m3u8_url)


# 代理
# https://www.proxydocker.com/zh/buyproxy/
# adsffqweriifgsfgwer@protonmail.com
# DFDSq345