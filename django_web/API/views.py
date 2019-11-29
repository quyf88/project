from django.shortcuts import render
import time
import json
import datetime
from .models import AntiFraud
from django.http import HttpResponse


def get_user(request, course):
    """读取数据库返回数据到HTML"""
    # user_list = Area.objects.all()  # 读取Area表中所有数据
    # for user in user_list:
    #     print(user.area)  # 打印Area表中area字段
    # # render方法可接收三个参数，一是request参数，二是待渲染的html模板文件,三是保存具体数据的字典参数(选填)。
    # return render(request, 'alipay.html', {'user_list': user_list})
    return render(request, 'alipay.html', {'course': course})

    """读取数据库返回json数据"""
    # antis = AntiFraud.objects.all()
    # ants = AntiFraud.objects.filter(id='460a23180f3411ea9aec28d2447ab52e')
    # 根据数据库id字段查询数据返回数据列表
    # ants = AntiFraud.objects.filter(id=course)[0]
    # ant = ants.status  # 账号状态
    #
    # # 账号状态为False：已过期直接返回数据
    # if not eval(ant):
    #     article = json.dumps({
    #         'status': ant,
    #         'context': '代理到期请及时续费!',
    #         'errorcode': 10002},
    #         ensure_ascii=False)
    #     print('代理到期请及时续费!')
    #     return HttpResponse(article, content_type='application/json')
    #
    # # 账号已过有效期更改数据库账号状态
    # lasting = ants.udeta  # 更新时间字段数据
    # print(lasting)
    # if not proxy(lasting):
    #     # 根据id条件 修改数据库status字段
    #     AntiFraud.objects.filter(id=course).update(status=False)
    #     print('账号状态修改成功!')
    #
    # # 构造返回json数据
    # ants = AntiFraud.objects.filter(id=course)[0]
    # ant = ants.status  # 账号状态
    # article = json.dumps({
    #     'status': ant,
    #     'context': '账号状态正常!',
    #     'errorcode': 10001},
    #     ensure_ascii=False)
    # return HttpResponse(article, content_type='application/json')


def proxy(lasting):
    """效验账号有效期"""
    print(lasting, type(lasting))
    # lasting 数据库中时间加30天
    lasting = lasting + + datetime.timedelta(days=30)
    # 时间类型转换为字符串
    lasting = lasting.strftime('%Y-%m-%d %H:%M:%S')
    print(lasting, type(lasting))
    # 字符串转为时间数组
    timeArray = time.strptime(lasting, "%Y-%m-%d %H:%M:%S")
    # timeArray可以调用tm_year等
    # print(timeArray.tm_year)
    # 时间数组转为时间戳 秒级
    timeStamp = int(time.mktime(timeArray))
    print(timeStamp)

    # 当前时间戳
    now_time = int(round(time.time()))
    print(now_time)
    # 当前时间大于账号有效期(更新时间+有效期) 证明账号已过期
    if now_time > timeStamp:
        print('代理到期请及时续费!')
        return False
    return True