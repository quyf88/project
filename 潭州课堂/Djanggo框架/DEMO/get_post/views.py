from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    # 请求路径
    print(request.path)
    # 请求方式
    print(request.method)
    # 编码格式
    print(request.encoding)

    return HttpResponse(111111)


def get_test(request):
    if request.method == 'GET':
        return render(request, 'get_post/get_post_test.html')
    elif request.method == 'POST':
        a = request.POST.get('a')
        b = request.POST.get('b')
        print(a, b)
        return HttpResponse('这是get_test测试')


def post_test(request):
    if request.method == 'GET':
        return render(request, 'get_post/get_post_test.html')
    elif request.method == 'POST':
        # get() 获取单个值 getlist 获取多个值 以列表形式展示 一键多值得情况下使用
        # request.POST.getlist('a')
        a = request.POST.get('a')
        b = request.POST.get('b')
        print(a, b)
        return HttpResponse('这是post_test测试')


"""类视图 实现文件上传"""
import os
from django.views import View
from mysite.settings import MEDIA_ROOT
class Upload(View):
    def get(self, request):
        return render(request, 'get_post/files.html')

    def post(self, request):
        # 获取请求中携带的文件
        f1 = request.FILES.get('file')
        # 拼接路径创建文件
        f_name = os.path.join(MEDIA_ROOT, f1.name)
        with open(f_name, 'wb') as f:
            # 读取文件流 固定写法
            for i in f1.chunks():
                f.write(i)

        return HttpResponse('这是文件上传测试页面')


"""cookie"""
import datetime
def set_cookie(request):
    """设置cookie"""
    response = HttpResponse('设置cookie')
    # max_age设置30秒之后过期 name 不可为中文
    response.set_cookie('name', 'dandan', max_age=30)
    return response

def get_cookie(request):
    """获取cookie"""
    cookie = request.COOKIES
    # 根据cookie name 获取cookie值
    print(cookie.get('name'))
    return HttpResponse('获取cookie')

def delete_cookie(request):
    """删除cookie"""
    response = HttpResponse('删除cookie')
    # 根据cookie name 删除cookie
    response.delete_cookie('name')
    return response