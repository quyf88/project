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

