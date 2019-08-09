from django.contrib import admin
from .models import Course, Student, Studetail, Department
# Register your models here.


class DepartmentAdmin(admin.ModelAdmin):
    """自定义管理界面"""
    # 显示字段， 可以点击列头进行排序
    list_display = ['d_id', 'd_name']
    # 可点击
    list_display_links = ['d_id', 'd_name']
    # 分页 每页显示数据量
    list_per_page = 10


# 注册模型
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Studetail)
admin.site.register(Department, DepartmentAdmin)