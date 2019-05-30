# coding=utf-8
# 作者    ： Administrator
# 文件    ：123.py
# IED    ：PyCharm
# 创建时间 ：2019/5/30 23:23


import csv
import requests
import json
import re


search=input('请输入关键词:')
url='https://m.weibo.cn/api/container/getIndex?type=all&queryVal={}&featurecode=20000320&luicode=10000011&lfid=106003type%3D1&title={}&containerid=100103type%3D1%26q%3D{}'.format(search,search,search)


headers = {'User-Agent':
                        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                        ' Chrome/59.0.3071.104 Safari/537.36'
                        }
cookie = {'_T_WM': '31576192650',
               ' SCF': 'AiijZBWTC3cK4xjwOUz27rnhXM13IutsjntDNytulWwnuWiLzenrdulnr8RBLmKClrJFMRwCfY1hieUEs9bbS7g.',
               ' MLOGIN': '1',
               ' SUB': '_2A25x65U1DeRhGeBO4lEV9ybJyD2IHXVTFzt9rDV6PUJbkdAKLXPxkW1NRbX_QKAlFu3rCiwBBYhdRhowWvMWmW_4',
               ' SUHB': '0h1J1PizDoA8ye', ' SSOLoginState': '1559225701',
               ' M_WEIBOCN_PARAMS': 'lfid%3D102803%26luicode%3D20000174'
               }



results=[]

links=[]
i=1
b=[1]
weibo=0
while True:
    if len(b)==0:
        break
    else:
        url_1=url+'&page='+str(i)
        print(url_1)
        r =requests.get(url_1,headers=headers,cookies=cookie).text
        a=json.loads(r)
        b=a['data']['cards']
        i+=1
        for j in range(len(b)):
            bb=b[j]
            try:
                for c in bb['card_group']:
                    try:
                        d=c['mblog']
                        link='https://m.weibo.cn/api/comments/show?id={}'.format(d['mid'])
                        links.append(link)
                        if d['isLongText']==False:
                            text=d['text']
                            pattern =re.compile(u"[\u4e00-\u9fa5]+")
                            text=re.findall(pattern,text)
                        else:
                            text=d['longText']['longTextContent']
                        results.append(text)
                        weibo+=1
                    except:
                        continue
            except:
                continue

print('共抓取{}条记录'.format(weibo))

pl=[]
for url_2 in links:
    r =requests.get(url_2,headers=headers,cookies=cookie).text
    a=json.loads(r)
    try:
        num=a['data']['total_number']
        j=0
        for i in range(num//10+1):
            url_3=url_2+'&page='+str(i+1)
            r =requests.get(url_3,headers=headers,cookies=cookie).text
            a=json.loads(r)
            b=a['data']
            try:
                c=b['hot_data']
                for i in range(len(c)):
                    d=c[i]['text']
                    pattern =re.compile(u"[\u4e00-\u9fa5]+")
                    d=re.findall(pattern,d)
                    j+=1
                    pl.append(d)
                    print(d)
            except:
                c=b['data']
                for i in range(len(c)):
                    d=c[i]['text']
                    pattern =re.compile(u"[\u4e00-\u9fa5]+")
                    d=re.findall(pattern,d)
                    j+=1
                    pl.append(d)
                    print(d)
        print('%s条评论'%j)
    except:
        print('无评论')



