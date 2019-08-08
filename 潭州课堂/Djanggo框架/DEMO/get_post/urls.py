# -*- coding: utf-8 -*-
# @Time    : 2019/8/8 10:55
# @Author  : project
# @File    : urls.py
# @Software: PyCharm
from django.urls import path, include
from . import views
urlpatterns = [
    path('index/', views.index),
    path('get_test/', views.get_test),
    path('post_test/', views.post_test),
    # 类视图路由配置
    path('cls_file/', views.Upload.as_view(), name='cls_file'),
]

