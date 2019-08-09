# -*- coding: utf-8 -*-
# @Time    : 2019/8/8 16:02
# @Author  : project
# @File    : forms.py
# @Software: PyCharm
from django import forms

"""自动生成form表单页面"""
# 可以验证 也可以生成前端代码
class RegisterForm(forms.Form):
    """注册表单页面"""
    username = forms.CharField(max_length=30, min_length=6)
    password = forms.CharField(max_length=30, min_length=6,
                               widget=forms.PasswordInput(attrs={'placeholder': '请输入密码'}))
    password_repeat = forms.CharField(max_length=30, min_length=6,
                                      widget=forms.PasswordInput(attrs={'placeholder': '请输入密码'}))
    email = forms.EmailField()


class LoginForm(forms.Form):
    """登录表单页面"""
    username = forms.CharField(max_length=30, min_length=6, widget=forms.TextInput(attrs={'placeholder': '请输入用户名'}))
    password = forms.CharField(max_length=30, min_length=6, widget=forms.PasswordInput(attrs={'placeholder': '请输入密码'}))
