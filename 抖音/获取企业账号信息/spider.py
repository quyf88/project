# -*- coding:utf-8 -*-
# 文件 ：spider.py
# IED ：PyCharm
# 时间 ：2019/10/30 0030 16:37
# 版本 ：V1.0
"""
切换至脚本目录下运行脚本
mitmdump -s spider.py
"""


import json


def response(flow):
    url = 'https://aweme-hl.snssdk.com/aweme/v2/comment/list/'

    # 筛选出以上面url为开头的url
    if flow.request.url.startswith(url):
        # 获取评论json数据
        text = flow.response.text
        # 将已编码的json字符串解码为python对象
        content = json.loads(text)
        # 评论内容
        comments = content['comments']
        for comment in comments:
            # 评论内容
            text = comment['text']
            # 用户名
            nickname = comment['user']['nickname']
            # 个性签名
            signature = comment['user']['signature']
            signature = signature.replace('\n', '').replace(' ', '')
            if '微信' in signature or 'VX' in signature or 'vx' in signature or 'V' in signature or 'v' in signature:
                print(f'用户名：{nickname} 个性签名：{signature} 评论内容：{text}')
                # data = f'用户名：{nickname} 个性签名：{signature} 评论内容：{text}'
                data = signature
                save_txt(data)


def save_txt(data):
    with open('demo.txt', 'a+', encoding='utf-8') as f:
        f.write(data)
        f.write('\n')

