# -*- coding: utf-8 -*-
# @Time    : 2019/8/8 14:51
# @Author  : project
# @File    : urls.py
# @Software: PyCharm

from django.urls import path, include
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.Login.as_view(), name='login'),
    path('register/', views.Register.as_view(), name='register'),
]
