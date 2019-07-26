import re
import time
import math
import random
import requests
import requests_html
from bs4 import BeautifulSoup
"""
安居客二手房信息
西刺代理
"""

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0'}


def get_ip_list(ip_url):
    web_data = requests.get(ip_url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        try:
            tds = ip_info.find_all('td')
            if tds[5].text == 'HTTPS':
                ip_list.append(tds[1].text + ':' + tds[2].text)
        except:
            continue

    for ip in ip_list:
        try:
            proxy_host = "https://" + ip
            proxy_temp = {"https": proxy_host}
            test_url = 'https://wulumuqi.anjuke.com/community/'
            print(proxy_temp)
            # res = requests.get(test_url, headers=headers, proxies=proxy_temp)
            res = requests.get(test_url, headers=headers, proxies=proxy_temp, timeout=3)
            print(res)
            if res.status_code == 200:
                return ip
        except Exception as e:
            ip_list.remove(ip)
            print(e)
            continue


def get_random_ip(ip_url):  # 随机生成代理
    # ip_list = get_ip_list(ip_url)
    # proxy_ip = random.choice(ip_list)
    # proxy_ip = proxy_ip.strip('\n')
    ip = get_ip_list(ip_url)
    proxy_host = "https://" + ip
    proxies = {"https": proxy_host}
    return proxies


def get_area_url(city_url, proxies):  # 获取区县的url ok
    session = requests_html.HTMLSession()
    area_response = session.get(city_url, headers=headers, timeout=5)
    print(area_response)
    area_urls = area_response.html.xpath('/html/body/div[5]/div[2]/div[1]/span[2]', first=True).links  # 返回的set格式
    area_url_list = list(area_urls)[1:]
    print(area_url_list)
    return area_url_list


def get_page(areaurl, proxies):  # 获取页数 ok
    session = requests_html.HTMLSession()
    star_response = session.get(areaurl, headers=headers, timeout=5)
    totle_num = star_response.html.xpath('//html/body/div[5]/div[3]/div[1]/div/span/em[2]')[0].text
    page_num = math.ceil(int(totle_num) / 30)  # 有余数加一
    print(page_num)
    return page_num


def get_moues_url(area_url, proxies):
    """
    获取 房子url
    :param city_url:
    :param proxies:
    :return: 返回房子url列表
    """
    time.sleep(3)
    session = requests_html.HTMLSession()
    print(area_url)
    r = session.get(area_url, headers=headers, timeout=3)
    print('get_moues_url:{}'.format(r))
    moues_url_list = r.html.xpath('//div[@class="li-itemmod"]/a/@href')

    return moues_url_list


def get_data(page_url, proxies):
    time.sleep(3)
    session = requests_html.HTMLSession()
    print(page_url)
    r = session.get(page_url, headers=headers, timeout=3)
    print('get_data:{}'.format(r))
    title = r.html.xpath('/html/body/div[2]/div[3]/div[1]/a/@title')[0]
    loc = r.html.xpath('/html/body/div[2]/div[3]/div[1]/a/@href')[0]
    lat = re.findall(r'#l1=(.*?)&', loc, re.S)[0]
    lnt = re.findall(r'&l2=(.*?)&', loc, re.S)[0]
    wuyefei = r.html.xpath('//html/body/div[2]/div[4]/div[2]/dl/dd[2]', first=True).text
    zongjianmianji = r.html.xpath('//html/body/div[2]/div[4]/div[2]/dl/dd[3]', first=True).text
    zonghushu = r.html.xpath('//html/body/div[2]/div[4]/div[2]/dl/dd[4]', first=True).text
    jianzaoniandai = r.html.xpath('//html/body/div[2]/div[4]/div[2]/dl/dd[5]', first=True).text
    tinchewei = r.html.xpath('//html/body/div[2]/div[4]/div[2]/dl/dd[6]', first=True).text
    rongjilv = r.html.xpath('//html/body/div[2]/div[4]/div[2]/dl/dd[7]', first=True).text
    lvhualv = r.html.xpath('//html/body/div[2]/div[4]/div[2]/dl/dd[8]', first=True).text
    suoshushangquan = r.html.xpath('//html/body/div[2]/div[4]/div[2]/dl/dd[11]', first=True).text
    price = r.html.xpath('//html/body/script[12]')[0].text
    data = re.findall(r"data : (.+?), ajaxUrl", price, re.S)[0]
    # area_price=re.findall(r"\"area\":(.+?),\"community\":",data,re.S)[0]
    # month_area_price=re.findall(r"\:\"(.*?)\"\},",area_price,re.S)
    comm_price = re.findall(r"\"community\":(.+?),\"comm_midprice\":", data, re.S)[0]
    month_comm_price = re.findall(r"\:\"(.*?)\"\},", comm_price, re.S)  # 小区三年房价数据
    with open('test2.csv', 'a', encoding='gbk') as f:
        print(title, lat, lnt, wuyefei, zongjianmianji, zonghushu,
               jianzaoniandai, tinchewei, rongjilv, lvhualv,
               suoshushangquan, month_comm_price)
        f.write("{},{},{},{},{},{},{},{},{},{},{},{}\n".format(title, lat, lnt, wuyefei, zongjianmianji, zonghushu,
                                                               jianzaoniandai, tinchewei, rongjilv, lvhualv,
                                                               suoshushangquan, month_comm_price))


def main(city_url):
    # proxies = get_random_ip(ip_url)
    proxies = '1'
    for area_url in get_area_url(city_url, proxies):
        for moues_url in get_moues_url(area_url, proxies):

            get_data(moues_url, proxies)


if __name__ == '__main__':
    city_url = 'https://wulumuqi.anjuke.com/community/'
    ip_url = 'http://www.xicidaili.com/'
    main(city_url)


