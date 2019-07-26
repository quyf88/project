# -*- coding: utf-8 -*-
# @Time    : 2019/7/26 13:35
# @Author  : project
# @File    : urls.py
# @Software: PyCharm

from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index)
]
