from django.shortcuts import render
from .models import Area
import json
from django.http import HttpResponse


def get_user(request):
    """读取数据库返回数据到HTML"""
    # user_list = Area.objects.all()
    # for user in user_list:
    #     print(user.area)
    # # render方法可接收三个参数，一是request参数，二是待渲染的html模板文件,三是保存具体数据的字典参数(选填)。
    # return render(request, 'index.html', {'user_list': user_list})

    """返回json数据"""
    # resp = {'errorcode': 100, 'detail': 'Get success'}
    # return HttpResponse(json.dumps(resp), content_type='application/json')
    article_info = {}
    data = json.loads(json.dumps(article_info))
    data['article1'] = 'NONE'
    article2 = {'title': 'python基础', 'publish_time': '2019-4-1', 'writer': {}}
    data['article2'] = article2
    writer = {'name': '李先生', 'sex': '男', 'email': 'xxx@gmail.com'}
    data['article2']['writer'] = writer
    article = json.dumps(data, ensure_ascii=False)
    print(article)
    return HttpResponse(article, content_type='application/json')