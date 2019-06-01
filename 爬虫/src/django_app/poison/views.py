#coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render
from poison import models
import sys,json
from django.core import serializers
from django.forms.models import model_to_dict
#sys.path.append(sys.path[0].replace("\\","/")+"./../spider_src")
#sys.path.append("/home/poison_app/src/spider_src")


def index(request):
    return render(request,'home.html')

# def get_data(request):
#     global old_sold
#     a = db.Db("test.db")
#     result = {}
#     db_data = a.query(is_all=True)
#     for i in db_data:
#         data = i['data']['data'] 
#         productId = data['detail']['productId']
#         temp = {
#             "productId": data['detail']['productId'],
#             "name": data['detail']['title'],
#             "size_list" : ",".join(data['detail']['sizeList']),
#             "color" : data['detail']['color'],
#             "articleNumber" : data['detail']['articleNumber'],
#             "authPrice" : data['detail']['authPrice'] / 100,
#             "sellDate" : data['detail']["sellDate"],
#             "exchangeDesc" : data["exchangeDesc"],
#             "soldNum"   : data['detail']['soldNum'],
#         }
#         result[str(productId)] = temp
#     diff_result = []
#     if old_sold:
#         for i in result:
#             temp = {
#                 "diff" : 0,
#                 "data" : result[i]
#             }
#             current_msg_sold = int(result[i]['soldNum'])
#             old_msg_sold = int(old_sold[i]['soldNum'])
#             temp['diff'] = current_msg_sold - old_msg_sold
#             diff_result.append(temp)
#         diff_result = sorted(diff_result,key = lambda x:x['diff'])
#         top_ten_result = diff_result[:11]
#     else:
#         top_ten_result = []
#     old_sold = result
#     json_data = json.dumps({"data":top_ten_result})

#     return HttpResponse(json_data,content_type="application/json,charset=utf-8")



def see_diff(request):
    diff = models.DiffTable.objects.all().order_by("-diff")[:10]
    diff_list = []
    result = []
    for row in diff:
        md = model_to_dict(row)
        productid = md['productid']
        temp = {
            "diff" : md['diff']
        }
        detail_data = models.DetailData.objects.get(productid=productid)
        md_detail = model_to_dict(detail_data)
        for i in md_detail:
            try:
                md_detail[i] = json.loads(md_detail[i])
            except BaseException as e:
                pass
        temp['detail'] = md_detail
        result.append(temp)
    return HttpResponse(json.dumps(result),content_type="application/json,charset=utf-8")

