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
    """
    页面渲染 需要设置主项目设置文件DIRS 设置路径
    模板传值 context={key:value}
    """
    return render(request, 'movie/movie_index.html', context={'name': 'dandan'})


def test():
    return 'this is test'


class Fruits:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def say(self):
        return 'this is say'


fruits = Fruits('蛋蛋', '2')
li = ['q', 'w', 'e', 'r']
tu = ('a', 's', 'd', 'f')
dic = {'x': 1, 'y': 2}
st = 'this is django course'


def index2(request):
    """
    模板传值
    :param request:
    :return:
    """
    return render(request, 'movie/movie_index.html',
                  context={'test': test,
                           'fruits': fruits,
                           'li': li,
                           'tu': tu,
                           'dic': dic,
                           'str': st})