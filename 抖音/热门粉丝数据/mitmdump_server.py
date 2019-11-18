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
    url = 'https://aweme-hl.snssdk.com/aweme/v1/user/follower/list/'

    # 筛选出以上面url为开头的url
    if flow.request.url.startswith(url):
        # 获取评论json数据
        text = flow.response.text
        # 将已编码的json字符串解码为python对象
        content = json.loads(text)
        # 评论内容
        comments = content['followers']
        for comment in comments:
            # 用户名
            nickname = comment['nickname']
            # 个性签名
            signature = comment['signature']
            signature = signature.replace('\n', '').replace(' ', '')
            print(f'用户名：{nickname} 个性签名：{signature}')
            if 'V' in signature or 'wx' in signature or 'vx' in signature or '微信' in signature or '➕' in signature \
                    or '合作' in signature or '薇' in signature or '威' in signature or 'w' in signature or 'W' in signature\
                    or '私信' in signature or '微' in signature or '胃心' in signature or '+' in signature:

                # data = f'个性签名：{signature}'
                # save_txt(data)
                result = re.findall(r'([a-zA-Z0-9_\-]{6,})', signature)
                if result:
                    if len(result[0]) < 18:
                        print(f'用户名：{nickname} 个性签名：{signature}')
                        tt = result[0].lstrip('V')
                        tt = tt.lstrip('vx')
                        tt = tt.lstrip('x')
                        tt = tt.lstrip('v')
                        tt = tt.lstrip('X')
                        tt = tt.lstrip('VX')
                        save_txt(tt)


def save_txt(data):
    filename = '微信号/' + datetime.datetime.now().strftime('%Y-%m-%d') + '.txt'
    with open(filename, 'a+', encoding='utf-8') as f:
        f.write(data)
        f.write('\n')

