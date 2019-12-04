from django.db import models


class AntiFraud(models.Model):
    # 账号ID UUID
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    # 业务名称
    business = models.CharField(db_column='Business', max_length=255, blank=True, null=True)  # Field name made lowercase.
    # 有效期
    expiration = models.CharField(db_column='Expiration', max_length=255, blank=True, null=True)  # Field name made lowercase.
    # 账号状态
    status = models.CharField(db_column='Status', max_length=255, blank=True, null=True)  # Field name made lowercase.
    # 更新时间
    udeta = models.DateTimeField(db_column='Udeta', blank=True, null=True)  # Field name made lowercase.
    # 创建时间
    datatime = models.DateTimeField(db_column='Datatime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'anti-fraud'


class Alipay(models.Model):
    # 账号ID UUID
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    # 名称
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    # 长链接
    longurl = models.CharField(db_column='LongUrl', max_length=10000, blank=True, null=True)  # Field name made lowercase.
    # 短链接
    shortlink = models.CharField(db_column='ShortLink', max_length=255, blank=True, null=True)  # Field name made lowercase.
    # 更新时间
    udeta = models.DateTimeField(db_column='Udeta', blank=True, null=True)  # Field name made lowercase.
    # 创建时间
    datatime = models.DateTimeField(db_column='Datatime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'alipay'

