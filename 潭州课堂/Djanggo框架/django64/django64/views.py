# -*- coding: utf-8 -*-
# @Time    : 2019/7/23 10:56
# @Author  : project
# @File    : views.py
# @Software: PyCharm
from django.http import HttpResponse


def index(request, course, count):
    return HttpResponse('这是主项目 {} 第{}个页面'.format(course, count))
