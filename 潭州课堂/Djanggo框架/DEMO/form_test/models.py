from django.db import models


# Create your models here.
class UserModel(models.Model):
    """
    模型类 创建数据库映射表
    python manage.py makemigrations 创建一个映射文件
    python manage.py migtate 将映射文件的映射数据真正提交到数据库(迁移)
    """
    # unique 用户名不能重复
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField()


class Department(models.Model):
    """学院表"""
    d_id = models.AutoField(primary_key=True)
    d_name = models.CharField(max_length=30)

    def __str__(self):
        return 'd_id={},d_name={}'.format(self.d_id, self.d_name)


class Student(models.Model):
    """学生表"""
    s_id = models.AutoField(primary_key=True)
    s_name = models.CharField(max_length=20)
    # 设置外键 on_delete级联删除
    department = models.ForeignKey('Department', on_delete=models.CASCADE)

    def __str__(self):
        return 's_id={},s_name={}'.format(self.s_id, self.s_name)


class Studetail(models.Model):
    """学生详情表"""
    # OneToOneField 设置一对一关系
    student = models.OneToOneField('Student', on_delete=models.CASCADE)
    s_age = models.IntegerField()
    note = models.TextField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return 's_age={},note={},phone={}'.format(self.s_age, self.note, self.phone)


class Course(models.Model):
    """课程表"""
    c_id = models.AutoField(primary_key=True)
    c_name = models.CharField(max_length=30)
    # ManyToManyField 设置多对多关系 自动生成中间表
    student = models.ManyToManyField('Student')

    def __str__(self):
        return 'c_id={},c_name={}'.format(self.c_id, self.c_name)
