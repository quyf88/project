from django.db import models

"""
只有修改表结构时才需要执行以下操作
"""

# Create your models here.
# 1.创建模型类
# 表映射关系 模型类-->表 属性-->字段
class User(models.Model):
    id = models.AutoField(primary_key=True)  # 自增长主键列 默认自动创建
    name = models.CharField(max_length=30)  # max_length 长度
    # 中途增加字段 需要添加默认值
    city = models.CharField(max_length=30, default=None, null=True)
    age = models.IntegerField(default=18)  # IntegerField int类型数据 默认值18

    def __str__(self):
        # 打印时触发此方法
        return 'id={},name={},city={}'.format(self.id, self.name, self.city)


class Test(models.Model):
    """
    常用的字段类型映射关系
    1. IntegerField : 整型，映射到数据库中的int类型。
    2. CharField:  字符类型，映射到数据库中的varchar类型，通过max_length指定最大长度。
    3. TextField:  文本类型，映射到数据库中的text类型。
    4. BooleanField: 布尔类型，映射到数据库中的tinyint类型，在使用的时候，传递True/False进去。如果要可以为空，则用NullBooleanField。
    5. DateField:  日期类型，没有时间。映射到数据库中是date类型，
       在使用的时候，可以设置DateField.auto_now每次保存对象时，自动设置该字段为当前时间。设置DateField.auto_now_add当对象第一次被创建时自动设置当前时间。
    6. DateTimeField:   日期时间类型。映射到数据库中的是datetime类型，
       在使用的时候，传递datetime.datetime()进去。

    """
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    gender = models.BooleanField(default=True)
    note = models.TextField()
    create_time = models.DateField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'name={},age={},gender={},note={}'.format(
            self.name, self.age, self.gender, self.note
        )

# 2. 创建一个映射文件(迁移)
# python manage.py makemigrations

# 3. 将映射文件的映射数据真正提交到数据库(迁移)
# python manage.py migtate


"""
OneToOneField 设置一对一关系
ManyToManyField 设置多对多关系 自动生成中间表
设置关系表时必须设置级联删除
级联删除 保证数据的完整性与一致性
on_delete=models.CASCADE 删除主键同时删除外键数据
on_delete=models.SET_NULL,null=True 删除主键同时把外键设置为空
on_delete=models.PROTECT 如果有外键正在引用主键 那么主键不允许删除
"""


class Department(models.Model):
    """学院表"""
    d_id = models.AutoField(primary_key=True)
    d_name = models.CharField(max_length=30)


class Student(models.Model):
    """学生表"""
    s_id = models.AutoField(primary_key=True)
    s_name = models.CharField(max_length=20)
    # 设置外键 on_delete级联删除
    department = models.ForeignKey('Department', on_delete=models.CASCADE)


class Studetail(models.Model):
    """学生详情表"""
    # OneToOneField 设置一对一关系
    student = models.OneToOneField('Student', on_delete=models.CASCADE)
    s_age = models.IntegerField()
    note = models.TextField()
    phone = models.CharField(max_length=20)


class Course(models.Model):
    """课程表"""
    c_id = models.AutoField(primary_key=True)
    c_name = models.CharField(max_length=30)
    # ManyToManyField 设置多对多关系 自动生成中间表
    student = models.ManyToManyField('Student')





