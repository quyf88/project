# -*- coding: utf-8 -*-
# @Time    : 2019/8/5 14:01
# @Author  : project
# @File    : urls.py
# @Software: PyCharm

from django.urls import path, include  # 子路由分配
from . import views

urlpatterns = [
    path('add/', views.add),
    path('select/', views.select),
    path('update/', views.update),
    path('delete/', views.delete),
]
