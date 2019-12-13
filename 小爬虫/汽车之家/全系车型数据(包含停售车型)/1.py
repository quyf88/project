# -*- coding:utf-8 -*-
# 文件 ：1.py
# IED ：PyCharm
# 时间 ：2019/12/13 0013 14:48
# 版本 ：V1.0


import bs4
import requests as req
'''
第一步，下载出所有车型的网页。
'''


def mainMethod():
    '''
    解析汽车之家所有车型数据保存到D盘
    '''
    li = [chr(i) for i in range(ord("T"), ord("Z")+1)]
    firstSite = "https://www.autohome.com.cn/grade/carhtml/"
    firstSiteSurfixe = ".html"
    secondSite = "https://car.autohome.com.cn/config/series/"
    secondSiteSurfixe = ".html"

    for a in li:
        if a is not None:
            requestUrl = firstSite+a+firstSiteSurfixe
            print(requestUrl)
            # 开始获取每个品牌的车型
            resp = req.get(requestUrl)
            # print(str(resp.content,"gbk"))
            bs = bs4.BeautifulSoup(str(resp.content, "gbk"), "html.parser")
            bss = bs.find_all("li")
            con = 0
            for b in bss:
                d = b.h4
                if d is not None:
                    her = str(d.a.attrs['href'])
                    her = her.split("#")[0]
                    her = her[her.index(".cn")+3:].replace("/", '')
                    if her is not None:
                        secSite = secondSite + her + secondSiteSurfixe
                        print("secSite="+secSite)
                        # 奥迪A3
                        if her is not None:
                            resp = req.get(secSite)
                            text = str(resp.content, encoding="utf-8")
                            print(a)
                            with open('html/' + str(her), 'a', encoding='utf-8') as f:
                                f.write(text)

                    con = (con+1)
            else:
                print(con)


if __name__ =="__main__":
    mainMethod()