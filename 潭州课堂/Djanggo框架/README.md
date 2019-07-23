- #### **虚拟环境**
  - ```cmd
    查看当前有哪些虚拟环境:  workon
    创建虚拟环境: mkvirtualenv -p /usr/bin/python3 envname
    进入虚拟环境: workon envname
    退出虚拟环境: deactivate
    删除虚拟环境: rmvirtualenv envname
    ```
  
- #### **django安装项目创建**
  - ```cmd
    安装django : pip install django
    查看当前python环境下的第三方库:  pip list
    
    新建项目的命令: 
        django-admin startproject projectname
    命令行启动命令：
        python manage.py runserver 0.0.0.0:8000    
    ```
- #### **创建视图函数 配置路由 创建APP**
  ######视图函数
  - ```python
    # 主项目中新建views视图文件
    # 导入响应模块
    from django.http import HttpResponse
    # 定义响应函数 必须传入request参数
    def index(request):
        return HttpResponse('这是Django index页面')
    ```
   ######路由配置
  - ```python
    from django.contrib import admin
    from django.urls import path
    from . import views  # .导入同目录下文件
    
    urlpatterns = [
        path('admin/', admin.site.urls),
        # index/ 路由路径  views.index 调用视图函数
        path('index/', views.index) 
        ]
    # include 路由分配
    # render 渲染页面
    # reverse, redirect 页面跳转
    ```
  ######新建APP
  - ```python
    # 命令行创建
    # python manage.py startapp 新建名称
    # pycharm 创建
    # Tools --> Run manage.py Task
    # startapp 新建名称
    # 创建成功后 需要在主目录settings中注册APP
    ``` 
- #### **页面重定向**
  - ```python
    """
    urls 设置
    path('new_movie/', views.new_movie, name='new_mv'),  # 定义name值 根据name值 重定向
    """
    from django.http import HttpResponse
    from django.shortcuts import redirect, reverse  # 页面重定向
    def old_movie(request, **kwargs):
        """页面重定向"""
        if kwargs.get('decide'):
            return redirect(reverse('new_mv'))
        return HttpResponse('这是 movie 目录 旧 页面  ')
    
    def new_movie(request, **kwargs):
        return HttpResponse('这是 movie 目录 新 页面  ')
    ```   

- #### **页面渲染**
  - ```python
    from django.shortcuts import render
    from django.template.loader import get_template  # 页面渲染文件
    def index1(request, **kwargs):
        """页面渲染 需要设置主项目设置文件DIRS 设置路径"""
        return render(request, 'movie/movie_index.html')
    ``` 

- #### **常用错误**
    ######进程已启动
  - ```cmd
    ps -aux|grep python  查看python进程
    kill -9 端口号  杀死进程
    ```
