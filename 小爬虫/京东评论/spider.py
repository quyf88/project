# -*- coding: utf-8 -*-
# @Time    : 2019/8/15 12:55
# @Author  : project
# @File    : 批量添加子站.py
# @Software: PyCharm
import csv
import json
import time
import requests
from fake_useragent import UserAgent
"""京东商品评价信息"""

START = 0


def spider(start):
    headers = {'User-Agent': str(UserAgent().random),
               # 必须加上此参数 不然获取不到信息
               'referer': 'https://item.jd.com/100006808184.html'}
    count = 1
    for i in range(start, 100):
        url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv2222&productId=100006808184&score=0&sortType=5&page={}&pageSize=10&isShadowSku=0&rid=0&fold=1'.format(i)
        print('第[{}]页评论 开始爬取'.format(i+1))
        if count % 20 == 0:
            print('休眠3秒')
            time.sleep(3)
        if i > 30:
            time.sleep(2)
        response = requests.get(url, headers=headers)
        # response = requests.get(url, headers=headers, verify=False)
        html = response.content.decode('gbk')
        html = html.replace('fetchJSON_comment98vv2222(', '').replace(');', '')
        html = json.loads(html)
        # 提取数据
        # 评论列表
        comments = html['comments']
        if not len(comments):
            print('获取信息失败：重试')
            global START
            START = i
            return
        data = []
        for comment in comments:
            # 产品ID
            ID = comment['referenceId']
            # 产品型号 颜色
            productColor = comment['productColor']
            productSize = comment['productSize']
            referenceName = productSize + ' ' + productColor
            # 评论内容
            content = comment['content'].replace('\n', '').replace('\r', '')
            # 评论时间
            referenceTime = comment['referenceTime']
            # 评论人
            nickname = comment['nickname']
            # 评分
            score = comment['score']
            # 会员级别
            userLevelName = comment['userLevelName']
            # 点赞
            usefulVoteCount = comment['usefulVoteCount']
            data.append([ID, referenceName, content, usefulVoteCount, score, nickname, userLevelName, referenceTime])
        scv_data(data)
        print('第[{}]页数据保存成功'.format(i+1))
        print('*'*50)
        print('\n')
        count += 1


def scv_data(data):
    """保存为csv"""
    with open("3.csv", "a+", encoding='utf-8', newline="") as f:
        k = csv.writer(f, delimiter=',')
        with open("3.csv", "r", encoding='utf-8', newline="") as f1:
            reader = csv.reader(f1)
            if not [row for row in reader]:
                k.writerow(['商品ID', '产品型号', '评论内容', '点赞', '评分', '评论id', '会员级别', '评论时间'])
                k.writerows(data)
            else:
                k.writerows(data)


def run():
    count = 1
    while True:
        if count >= 10:
            break
        spider(START)
        print('休眠5秒')
        time.sleep(5)
        count += 1


if __name__ == '__main__':
    run()