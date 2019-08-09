# -*- coding: utf-8 -*-
# @Time    : 2019/8/9 10:40
# @Author  : project
# @File    : mymiddleware.py
# @Software: PyCharm
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class MyException(MiddlewareMixin):
    """异常中间件"""
    def process_exception(self, request, exception):
        return HttpResponse(exception)


class UserMiddlewaer(object):
    """
    自定义中间件
    需要在主项目文件setting MIDDLEWARE中配置
    """
    def __init__(self, get_resp):
        self.get_resp = get_resp

    def __call__(self, request):
        # call方法实现实例对象可调用
        # 如果没有获取到username 默认为xxxxx
        username = request.session.get('username', 'xxxxxx')
        if username:
            # setattr 赋值
            setattr(request, 'myuser', username)
            print('这是到达视图函数之前的代码')
        response = self.get_resp(request)
        print('这是响应之后的代码')

        return response