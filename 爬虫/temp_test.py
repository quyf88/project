# -*- coding: utf-8 -*- 
import time
import asyncio
import aiohttp
import hashlib
import json



# # import pandas

# def get_json_img(dic):
#     img_src = []
#     data = dic['data']
#     for i in data['detail']['images']:
#         img_src.append(i['url'])
#     for i in data['relationTrends']['list']:
#         if "images" in i['trends']:
#             for j in i['trends']['images']:
#                 img_src.append(j['url'])
#     img_src.append(data['detail']['brandLogoUrl'])
#     return img_src

import sys
sys.path.append("./src/spider_src/")
import db


# w =  {'status': 200, 'msg': '成功', 'data': {'item': [], 'detail': {'productId': 19854, 'isSelf': 0, 'brandId': 10082, 'typeId': 3, 'logoUrl': 'https://du.hupucdn.com/news_byte50820byte_63542562b0bc5fe07d7b60b3c4cf7833_w500h320.jpg', 'images': [{'type': 0, 'url': 'https://du.hupucdn.com/news_byte50820byte_f8d925f96e875aadaec63abe67320660_w500h320.jpg', 'originUrl': 'https://du.hupucdn.com/news_byte50820byte_f8d925f96e875aadaec63abe67320660_w500h320.jpg', 'width': 500, 'height': 320}], 'title': 'FOG FEAR OF GOD Half Zip Hoodie  半拉链帽衫 军绿', 'soldNum': 5, 'sellDate': '2017.12.10', 'articleNumber': 'FOG-FW18-002-03', 'articleNumbers': ['FOG-FW18-002-03'], 'color': '军绿', 'authPrice': 158000, 'goodsId': 0, 'sizeList': ['S', 'M', 'L', 'XL'], 'unit': {'name': '尺码', 'suffix': ' '}, 'deliverTime': '129600', 'preSellStatus': 0, 'preSellDeliverTime': 2592000, 'preSellLimitPurchase': 0, 'isShowPreSellTag': 0, 'isPreSellNew': 0, 'isShow': 1, 'sourceName': 'default', 'brandLogoUrl': 'https://du.hupucdn.com/news_byte23329byte_3e247b5d598f7da36a1af24d08cb9ad8_w350h350.png'}, 'sizeList': [{'size': 'S', 'formatSize': 'S', 'item': [], 'rapidlyExpressItem': [], 'buyerBiddingItem': {'buyerBiddingId': 0, 'size': 'S', 'price': 0}, 'showItem': [], 'preSellItem': []}, {'size': 'M', 'formatSize': 'M', 'item': [], 'rapidlyExpressItem': [], 'buyerBiddingItem': {'buyerBiddingId': 0, 'size': 'M', 'price': 0}, 'showItem': [], 'preSellItem': []}, {'size': 'L', 'formatSize': 'L', 'item': [], 'rapidlyExpressItem': [], 'buyerBiddingItem': {'buyerBiddingId': 0, 'size': 'L', 'price': 0}, 'showItem': [], 'preSellItem': []}, {'size': 'XL', 'formatSize': 'XL', 'item': [], 'rapidlyExpressItem': [], 'buyerBiddingItem': {'buyerBiddingId': '0', 'size': 'XL', 'price': '0'}, 'showItem': [], 'preSellItem': []}], 'relationList': [], 'relationIsFull': 0, 'lastSoldList': [{'avatar': 'https://wx.qlogo.cn/mmopen/vi_32/GrhaxTh4kCB1Kg2Hze8z3A8XJSLPJGNGGnprTSotxPTP5iaU2KLENy9pZ9yu00nAvkOc3xEfpXvzvXZ0MoJGjfQ/0?imageView2/2/w/50/h/50', 'userName': '_****南', 'sizeDesc': 'M ', 'formatTime': '12月19日'}, {'avatar': 'https://du.hupucdn.com/icon_byte3636byte_5bdaadb7c88ed_w180h180.png?imageView2/2/w/50/h/50', 'userName': 'F****k', 'sizeDesc': 'M ', 'formatTime': '12月16日'}, {'avatar': 'https://du.hupucdn.com/1604668_model_ANE-TL00_model_byte136023byte_bc70397bde51986eae0157accf97d180_hupu_android_w0h0.png?imageView2/2/w/50/h/50', 'userName': 'w****t', 'sizeDesc': 'L ', 'formatTime': '12月14日'}, {'avatar': 'https://du.hupucdn.com/icon_byte3636byte_5be84df636c55_w180h180.png?imageView2/2/w/50/h/50', 'userName': 'C****e', 'sizeDesc': 'L ', 'formatTime': '12月9日'}], 'discountList': [], 'discountShow': '', 'shareLinkUrl': 'https://m.poizon.com/mdu/product/detail.html?id=19854&source=shareDetail', 'rapidlyExpressTips': '约三天到货', 'exchangeDesc': '不支持7天无理由退换货', 'imageAndText': '<!DOCTYPE html><html lang="zh_CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1,user-scalable=no"><style type="text/css">*,:after,:before{box-sizing:border-box;margin:0;padding:0;word-wrap:break-word}.dc{}p{padding:0 20px;color:#54565e;font-weight:300;font-size:14px;font-family:PingFangSC;line-height:25px}img,p{margin-top:20px}img{display:block;width:100%}</style></head><body><div class="dc"><img width="100%" alt="" src="https://du.hupucdn.com/news_byte50820byte_93e71a17610cd58fb1f72cc8fdf14ab2_w500h320.jpg" /><img width="100%" alt="" src="https://du.hupucdn.com/news_byte302033byte_c710747f0149bb0f4659cd87b67e68fd_w1067h1600.jpg" /><img width="100%" alt="" src="https://du.hupucdn.com/news_byte153672byte_2014ca28436cbe6ba9ffd90517eba95e_w500h667.jpg" /><img width="100%" alt="" src="https://du.hupucdn.com/news_byte53327byte_639a0581bfb311e7707a68e8bb038fca_w750h472.jpg" /><img src="https://du.hupucdn.com/news_byte89056byte_557ccbb0e1e909d038baefc646145651_w1125h1709.png" alt="" width="100%"/></div></body></html>', 'chestList': [], 'collectSizeList': [], 'dispatchName': '顺丰速运', 'relationTrends': {'list': [], 'addRelationTrendTips': {'entryTips': '穿搭精选(0)', 'emptyTips': '晒出你的搭配'}, 'total': '0'}, 'sellerBiddingTypeTips': {'sellTitle': '', 'sellContent': '36小时内寄付至平台', 'preSellTitle': '', 'preSellContent': '可提前30天优先出售', 'sellNowTitle': '12.25～1.3免手续费', 'sellNowContent': '匹配最高求购价即刻成交', 'preSellStatus': 0}}, 'timestamp': 0.010832071304321, 'log': None}



# print(type(w))
# print(w.keys())

a = db.Db('test.db')
print(time.time())
a.insert_detail()

# #print(a.query_detail({"productId":17475,"json_data":w,"img_list":get_json_img(w)}))

# a.insert_detail({"productId":w['data']['detail']['productId'],"json_data":w,"img_list":get_json_img(w)})
# #print(a.query_all_detail())
# # for i in a.query_all_detail():
# #     for j in i:
# #         print(j)


# # brand_dic = {'10000': 'ROARINGWILD',
# #  '10001': 'Thrasher',
# #  '10002': 'Y-3',
# #  '10012': 'Balenciaga',
# #  '10013': 'Neil Barrett',
# #  '10014': 'KENZO',
# #  '10016': 'Vetements',
# #  '10017': 'PLACES+FACES',
# #  '10018': '大疆',
# #  '10019': 'Givenchy',
# #  '10021': 'Cav Empt',
# #  '10022': 'LONGINES',
# #  '10024': 'BANDAI',
# #  '10027': 'DICKIES',
# #  '10029': 'McQ',
# #  '10030': 'CarharttWIP',
# #  '10031': 'Alpha Industries',
# #  '10033': 'Hasbro',
# #  '10035': 'dyson',
# #  '10037': 'C2H4',
# #  '10038': 'KITH',
# #  '10039': 'Randomevent',
# #  '10082': 'FOG',
# #  '10084': 'Bounce',
# #  '1222': 'NOAH',
# #  '1245': 'OFF-WHITE',
# #  '13': 'Jordan',
# #  '1310': 'Champion',
# #  '144': 'Nike',
# #  '176': 'CONVERSE',
# #  '1860': 'THOM BROWNE',
# #  '2': 'Puma',
# #  '2389': 'LEGO',
# #  '3': 'adidas',
# #  '3023': 'UNDERCOVER',
# #  '33': '李宁',
# #  '34': '安踏',
# #  '4': 'New Balance',
# #  '421': 'Kaws',
# #  '439': 'Supreme',
# #  '45': 'THE NORTH FACE',
# #  '494': 'adidas original',
# #  '4981': '虎扑优选',
# #  '4985': 'Revenge Storm',
# #  '4988': 'OMEGA',
# #  '4991': 'Medicom Toy',
# #  '4992': 'FR2',
# #  '4993': 'Fucking Awesome',
# #  '577': 'PALACE',
# #  '6': 'Reebok',
# #  '634': 'A BATHING APE',
# #  '65': 'Apple',
# #  '7': 'Under Armour',
# #  '8': 'Asics',
# #  '843': 'CASIO',
# #  '9': 'Vans'}



# # all_data = {
# #     "all_data" : []
# # }
# # for i in a.query_all_detail():
# #     all_data['all_data'].append(i)
# #     if str(i['brand_id']) not in all_data:
# #         all_data[str(i['brand_id'])] = [i]
# #     else:
# #         all_data[str(i['brand_id'])].append(i)


# # for k,v in all_data.items():
# #     key_list = ["id","name","productId","price","size_list","brand_id","color","articleNumber","authPrice","sellDate","exchangeDesc","soldNum" ,"text_string" ,"img_list" ,"size_price"]
# #     new_list = []
# #     str_list = []
# #     for i in v:
# #         size_price = json.loads(i['size_price'])
# #         for price_list in size_price:
# #             print(price_list)
# #             if price_list[0] not in i:
# #                 i[price_list[0]] = price_list[1]
# #             if price_list[0] not in new_list and price_list[0] not in str_list:
# #                 if "." in price_list[0]:
# #                     price_list[0] = float(price_list[0])
# #                     new_list.append(price_list[0])
# #                 elif price_list[0].isdigit():
# #                     price_list[0] = int(price_list[0])
# #                     new_list.append(price_list[0])
# #                 else:
# #                     str_list.append(price_list[0])
# #     new_list = sorted(new_list)
# #     key_list = key_list + new_list + str_list
# #     print(key_list)
# #     for i in v:
# #         for key in key_list:
# #             key = str(key)
# #             if key not in i:
# #                 i[key] = "--"
# #     try:
# #         brand_name = brand_dic[k]
# #     except:
# #         brand_name = k
    
# #     writer = pandas.ExcelWriter("{}.xlsx".format(brand_name))
# #     pdfrm = pandas.DataFrame(data = v)
# #     pdfrm.to_excel(writer)
# #     writer.save()



# # # import json

# # # w = eval(w)



# # # print(get_json_img(w))

# # # import asyncio
# # # import requests

# # # async def img_req(url):
# # #     n = 0
# # #     while True:
# # #         try:
# # #             r  = requests.get(url,timeout=(5,10),verify = False)
# # #             return r.content
# # #         except BaseException as e:
# # #             print(e)
# # #             n += 1
# # #             if n >= 5:
# # #                 raise ValueError("normal request also error!")

# # # def main():
# # #     #asyncio.ensure_future(img_req("https://du.hupucdn.com/Fk5Dmq9oGF4wc0IrkSv0uy-WaXNq"))
# # #     loop = asyncio.get_event_loop()
# # #     r = loop.run_until_complete(asyncio.ensure_future(img_req("https://du.hupucdn.com/Fk5Dmq9oGF4wc0IrkSv0uy-WaXNq")))
# # #     print(r)
# # # main()



# import os

# print(os.listdir('excel_res'))
