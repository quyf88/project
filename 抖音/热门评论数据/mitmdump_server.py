# -*- coding:utf-8 -*-
# 文件 ：mitmdump_server.py
# IED ：PyCharm
# 时间 ：2019/10/30 0030 16:37
# 版本 ：V1.0
"""
切换至脚本目录下运行脚本
mitmdump -s mitmdump_server.py
OSError: [WinError 87] 参数错误 : 把print注释掉
"""
import re
import json
import datetime


def response(flow):
    url = 'https://aweme-hl.snssdk.com/aweme/v2/comment/list/'
    _url = 'https://aweme.snssdk.com/aweme/v2/comment/list/'
    # print(url)
    # 筛选出以上面url为开头的url
    filename = '微信号/' + datetime.datetime.now().strftime('%Y-%m-%d') + '.txt'
    with open(filename, 'a+', encoding='utf-8') as f:
        if flow.request.url.startswith(url) or flow.request.url.startswith(_url):
            # 获取评论json数据
            text = flow.response.text
            # 将已编码的json字符串解码为python对象
            content = json.loads(text)
            # 评论内容
            comments = content['comments']
            for comment in comments:
                # 评论内容
                _text = comment['text']
                # 用户名
                nickname = comment['user']['nickname']
                # 个性签名
                signature = comment['user']['signature']
                signature = signature.replace('\n', '').replace(' ', '')
                print(f'评论内容：{_text} 用户名：{nickname} 个性签名:{signature}')
                if 'V' in signature or 'wx' in signature or 'vx' in signature or '微信' in signature or '➕' in signature \
                        or '合作' in signature or '薇' in signature or '威' in signature or 'w' in signature or 'W' in signature\
                        or '私信' in signature or '微' in signature or '胃心' in signature or '+' in signature:

                    result = re.findall(r'([a-zA-Z0-9_\-]{6,})', signature)
                    if not result or len(result) > 1:
                        continue
                    if len(result[0]) < 18:
                        tt = result[0].lstrip('V')
                        tt = tt.lstrip('vx').rstrip('vx')
                        tt = tt.lstrip('x').rstrip('x')
                        tt = tt.lstrip('v').rstrip('v')
                        tt = tt.lstrip('X').rstrip('X')
                        tt = tt.lstrip('VX').rstrip('VX')
                        f.write(tt)
                        f.write('\n')

