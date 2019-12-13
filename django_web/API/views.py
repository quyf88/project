import time
import json
import datetime
from .models import AntiFraud
from .models import Alipay
from django.shortcuts import render
from django.http import HttpResponse


def alipay(request, course):
    """读取数据库返回数据到HTML"""
    # user_list = Alipay.objects.filter(id=course)
    # for user in user_list:
    #    id = user.id
    #    longurl = user.longurl
    #    shortlink = user.shortlink
    #     udeta = user.udeta
    #    datatime = user.datatime
    #    data.append(id)
    #    data.append(shortlink)
    # return render(request, 'alipay.html', {'List': json.dumps(data), 'user_list': course})

    """读取账号文件返回到alipay.html页面"""
    file = 'API/config/access.txt'
    data = read_txt(course, file)

    if not data:
        article = json.dumps({
            'status': 200,
            'errorcode': 10002,
            'context': '二维码异常!'},
            ensure_ascii=False)
        return HttpResponse(article, content_type='application/json')
    # print(data)
    # render方法可接收三个参数，一是request参数，二是待渲染的html模板文件,三是保存具体数据的字典参数(选填) 向js传递数据需要转换为json格式。
    return render(request, 'alipay.html', {'List': json.dumps(data), 'user_list': data[1]})


def ceshi(request):
    return HttpResponse('测试页面')


def validity_period(request, course):
    """效验账号有效期 读取数据库返回json数据"""
    # antis = AntiFraud.objects.all()
    # ants = AntiFraud.objects.filter(id='460a23180f3411ea9aec28d2447ab52e')
    # 根据数据库id字段查询数据返回数据列表
    # ants = AntiFraud.objects.filter(id=course)[0]
    # ant = ants.status  # 账号状态

    """读取账号记录文件"""
    file = 'API/config/proxy.txt'
    data = read_txt(course, file)

    if not data:
        article = json.dumps({
            'status': 200,
            'errorcode': 10002,
            'context': '账号错误!'},
            ensure_ascii=False)
        return HttpResponse(article, content_type='application/json')
    # 账号状态为False：已过期直接返回数据
    if not proxy(data[4]):
        article = json.dumps({
            'status': data[3],
            'context': '代理到期请及时续费!',
            'errorcode': 10002},
            ensure_ascii=False)
        print('代理到期请及时续费!')
        return HttpResponse(article, content_type='application/json')

    # 账号已过有效期更改数据库账号状态
    # if not proxy(data[4]):
        # 根据id条件 修改数据库status字段
        # AntiFraud.objects.filter(id=course).update(status=False)
        # print('账号状态修改成功!')

    # 构造返回json数据
    article = json.dumps({
        'status': data[3],
        'context': '代理效验成功!',
        'errorcode': 10001},
        ensure_ascii=False)
    return HttpResponse(article, content_type='application/json')


def proxy(lasting):
    """从数据库读取时间效验有效期"""
    # print(lasting, type(lasting))
    # # lasting 数据库中时间加30天
    # lasting = lasting + datetime.timedelta(days=30)
    # # 时间类型转换为字符串
    # lasting = lasting.strftime('%Y-%m-%d %H:%M:%S')
    # print(lasting, type(lasting))
    # # 字符串转为时间数组
    # timeArray = time.strptime(lasting, "%Y-%m-%d %H:%M:%S")
    # # timeArray可以调用tm_year等
    # # print(timeArray.tm_year)
    # # 时间数组转为时间戳 秒级
    # timeStamp = int(time.mktime(timeArray))
    # print(timeStamp)
    #
    # # 当前时间戳
    # now_time = int(round(time.time()))
    # print(now_time)
    # # 当前时间大于账号有效期(更新时间+有效期) 证明账号已过期
    # if now_time > timeStamp:
    #     print('代理到期请及时续费!')
    #     return False
    # return True
    timeArray = time.strptime(lasting, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    now_time = int(round(time.time()))
    if now_time > timeStamp:
        print('代理到期请及时续费')
        return False

    return True


def read_txt(course, file):
    """读取账号文件"""
    with open(file, 'r', encoding='UTF-8') as f:
        access = f.readlines()
        for data in access:
            data = [i for i in data.strip().split(',') if i]
            print(data, type(data))
            if course in data:
                return data
