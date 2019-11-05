# -*- coding:utf-8 -*-
# 文件 ：mitmdump_server.py
# IED ：PyCharm
# 时间 ：2019/10/30 0030 16:37
# 版本 ：V1.0
"""
切换至脚本目录下运行脚本
mitmdump -s mitmdump_server.py
"""
import re
import json
import datetime


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
            # if '微信' in signature or 'VX' in signature or 'vx' in signature or 'V' in signature or 'v' in signature:
            #     print(f'用户名：{nickname} 个性签名：{signature} 评论内容：{text}')
            #     # data = f'用户名：{nickname} 个性签名：{signature} 评论内容：{text}'
            #     data = signature
            result = re.findall('([a-zA-Z0-9_\-]{8,})', signature)
            if result:
                print(f'用户名：{nickname} 个性签名：{signature} 评论内容：{text}')
                for itme in result:
                    if len(itme) <= 20 and 'QQ' not in itme and '_' not in itme:
                        pattern = re.compile('[0-9]+')
                        match = pattern.findall(itme)
                        if match:
                            tt = itme.lstrip('V')
                            tt = tt.lstrip('v')
                            tt = tt.lstrip('X')
                            tt = tt.lstrip('__')
                            save_txt(tt)


def save_txt(data):
    filename = '微信号/' + datetime.datetime.now().strftime('%Y-%m-%d') + '.txt'
    with open(filename, 'a+', encoding='utf-8') as f:
        f.write(data)
        f.write('\n')

