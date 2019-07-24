# -*- coding: utf-8 -*-
# @Time    : 2019/7/23 11:16
# @Author  : project
# @File    : urls.py
# @Software: PyCharm

from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index),
    path('old_movie/', views.old_movie),
    path('new_movie/', views.new_movie, name='new_mv'),  # 定义name值 根据name值 重定向
    path('index1/', views.index1),
    path('index2/', views.index2),
]
