from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
# Create your views here.
def home(request):
    """登录页面"""
    print('这是调用的视图函数')
    username = request.session.get('username')
    return render(request, 'form_test/home.html', context={'username': username})

from django.views import View

# class Login(View):
#     """登录功能"""
#     def get(self, request):
#         return render(request, 'form_test/login.html')
#
#     def post(self, request):
#         username = request.POST.get('username')
#         # 字典传值 会存到数据库
#         request.session['username'] = username
#         # 设置 session 过期时间 0 表示 关闭浏览器即过期 None默认两周过期
#         request.session.set_expiry(0)
#         print(request.session)
#         return redirect(reverse('home'))

def logout(request):
    """退出登录"""
    # flush 清除登录cookie和session
    request.session.flush()
    return redirect(reverse('login'))


from .models import UserModel
from .forms import RegisterForm, LoginForm


class Register(View):
    def get(self, request):
        # 实例化一个表单实例
        form = RegisterForm()
        return render(request, 'form_test/register.html', context={'form': form})

    def post(self, request):
        # 获取form表单的数据
        form = RegisterForm(request.POST)
        # 验证数据
        if form.is_valid():
            # 获取表单提交的数据
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            password_repeat = form.cleaned_data.get('password_repeat')
            email = form.cleaned_data.get('email')
            if password == password_repeat:
                UserModel.objects.create(username=username, password=password, email=email)
                return HttpResponse('注册成功')
            else:
                return HttpResponse('两次密码不一致')
        else:
            return HttpResponse('注册失败')


class Login(View):
    """登录功能"""
    def get(self, request):
        # 实例化一个表单实例
        form = LoginForm()
        return render(request, 'form_test/login.html', context={'form': form})

    def post(self, request):
        # 获取发送的请求值
        form = LoginForm(request.POST)
        # 监测数据是否合法
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = UserModel.objects.filter(username=username, password=password)
            if user:
                # 设置登录session
                request.session['username'] = username
                return redirect(reverse('home'))
            else:
                return redirect(reverse('register'))
        else:
            return HttpResponse('登录失败')