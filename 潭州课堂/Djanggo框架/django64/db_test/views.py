from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Test  # 导入模型类


def add(request):
    # 方法一
    # mr = User(name='蛋蛋', city='2')
    # mr.save()  # 保存提交
    # # 方法二
    # mr = User()
    # mr.name = '小明'
    # mr.city = '上海'
    # mr.save()
    # # 方法三
    # User.objects.create(name='小黑', city='北京')
    # 方法四 插入前会判断有没有重复数据如果有不会添加
    Test.objects.get_or_create(name='小白', age=18, gender=True, note='小伙子很帅气')

    return HttpResponse('添加成功')


def select(request):
    # 查询所有对象
    rs = User.objects.all()
    # 查询单个对象
    # rs = User.objects.get(name='蛋蛋')
    # 查询满足条件的的对象
    # rs = User.objects.filter(name='蛋蛋')
    # 查询第一条数据
    # rs = User.objects.first()
    # 查询最后一条数据
    # rs = User.objects.last()
    # return HttpResponse('查询成功')
    # 查询不满足条件的
    rs = User.objects.exclude(name='蛋蛋')
    # 对查询结果进行排序 '-age' 反向排序 可多字段排序
    rs = User.objects.order_by('age', 'id')
    # 查询结果转换成字典
    rs = User.objects.all().values()
    # 查询结果的总数
    rs = User.objects.count()

    # 查询条件
    # 相当于等于
    rs = User.objects.filter(name__exact='蛋蛋')
    # 包含
    rs = User.objects.filter(name__contains='蛋蛋')
    # 以。。开头
    rs = User.objects.filter(name__startswith='蛋蛋')
    # 以。。结尾
    rs = User.objects.filter(name__endswith='蛋蛋')
    # 成员所属
    rs = User.objects.filter(id_in=[2, 3, 5])
    # 大于age__gt 大于等于age__gte 小于age__lt 小于等于age__lte
    rs = User.objects.filter(age__lt=18)
    # 区间
    rs = User.objects.filter(id__range=(2, 4))
    # 切片 不可用负数切片
    rs = User.objects.all()[0:3]



    # 查询数据渲染至页面
    return render(request, 'db_index.html', context={'rs': rs})


def update(request):
    # 方法一
    rs = Test.objects.get(id=1)
    rs.age = 2
    rs.save()
    # 方法二 修改数据后时间不会实时更新
    # User.objects.filter(name='蛋蛋').update(city='北京')
    # 修改所有数据
    # User.objects.all().update(city='北京')

    return HttpResponse('修改成功')


def delete(request):
    User.objects.get(name='蛋蛋').delete()

    return HttpResponse('删除成功')