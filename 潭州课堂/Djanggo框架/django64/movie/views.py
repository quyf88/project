from django.shortcuts import render, redirect, reverse  # 页面重定向
from django.http import HttpResponse
from django.template.loader import get_template  # 页面渲染文件
# Create your views here.


def index(request, **kwargs):
    return HttpResponse('这是 movie 目录 index 页面 ')


def old_movie(request, **kwargs):
    """页面重定向"""
    if kwargs.get('decide'):
        return redirect(reverse('new_mv'))
    return HttpResponse('这是 movie 目录 旧 页面  ')


def new_movie(request, **kwargs):
    return HttpResponse('这是 movie 目录 新 页面  ')


def index1(request, **kwargs):
    """页面渲染 需要设置主项目设置文件DIRS 设置路径"""
    return render(request, 'movie/movie_index.html')