from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .models import BlogModel


# Create your views here.
def blog_index(request):
    """首页"""
    return render(request, 'blog/demo_index.html')


def blog_add(request):
    """添加文章页"""
    if request.method == 'GET':
        return render(request, 'blog/demo_add.html')
    elif request.method == 'POST':
        # 根据标签name获取POST提交的数据值
        title = request.POST.get('title')
        content = request.POST.get('content')
        # 保存至数据库
        blog = BlogModel(title=title, content=content)
        blog.save()
        # return HttpResponse('数据保存成功')
        # 页面渲染
        return render(request, 'blog/demo_add.html')
        # 页面重定向
        # return redirect(reverse('blog_add'))


def blog_list(request):
    """文章列表页"""
    # 从数据库获取所有文章
    blog_list = BlogModel.objects.all()
    # 通过上下文把文章传递给模板
    return render(request, 'blog/demo_list.html', context={'blog_list': blog_list})


def blog_detail(request, blog_id):
    """文章详情页"""
    # 传递参数时必须在路由里设置参数名称一致
    # 根据文章列表页点击时传递过来的blog_id 从数据库查询出文章详细信息
    blog = BlogModel.objects.get(id=blog_id)
    # 通过上下文把文章传递给模板
    return render(request, 'blog/demo_detail.html', context={'blog': blog})


def blog_delete(request, blog_id):
    """删除文章"""
    # 传递参数时必须在路由里设置参数名称一致
    # 根据文章列表页点击时传递过来的blog_id 从数据库查询出文章详细信息
    blog = BlogModel.objects.get(id=blog_id)
    if blog:
        # 删除
        blog.delete()
        # 页面重定向至文章列表页
        return redirect(reverse('blog_list'))
    else:
        return HttpResponse('不存在这篇文章')


def blog_update(request, blog_id):
    """编辑"""
    blog = BlogModel.objects.get(id=blog_id)
    if request.method == 'GET':
        return render(request, 'blog/demo_update.html', context={'blog': blog})
    elif request.method == 'POST':
        # 获取修改后的文本保存至数据库
        blog.title = request.POST.get('title')
        blog.content = request.POST.get('content')
        blog.save()
        # 修改完成后页面重定向至文章列表页
        return redirect(reverse('blog_list'))


"""类视图"""
from django.views import View
class BlogAdd(View):
    def get(self, request):
        return render(request, 'blog/demo_add.html')

    def post(self, request):
        # 根据标签name获取POST提交的数据值
        title = request.POST.get('title')
        content = request.POST.get('content')
        # 保存至数据库
        blog = BlogModel(title=title, content=content)
        blog.save()
        # return HttpResponse('数据保存成功')
        # 页面渲染
        return render(request, 'blog/demo_add.html')
        # 页面重定向
        # return redirect(reverse('blog_add'))