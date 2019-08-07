# -*- coding: utf-8 -*-
# @Time    : 2019/8/7 13:34
# @Author  : project
# @File    : urls.py
# @Software: PyCharm

from django.urls import path, include
from . import views

urlpatterns = [
    path('index/', views.blog_index, name='blog_index'),
    path('add/', views.blog_add, name='blog_add'),
    path('list/', views.blog_list, name='blog_list'),
    path('detail/<blog_id>', views.blog_detail, name='blog_detail'),
    path('delete/<blog_id>', views.blog_delete, name='blog_delete'),
]
