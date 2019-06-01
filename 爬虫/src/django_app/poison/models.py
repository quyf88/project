# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DetailData(models.Model):
    #id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    productid = models.CharField(db_column='productId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    price = models.IntegerField()
    size_list = models.CharField(max_length=100, blank=True, null=True)
    brand_id = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    articlenumber = models.CharField(db_column='articleNumber', max_length=100, blank=True, null=True)  # Field name made lowercase.
    authprice = models.IntegerField(db_column='authPrice')  # Field name made lowercase.
    selldate = models.CharField(db_column='sellDate', max_length=100, blank=True, null=True)  # Field name made lowercase.
    exchangedesc = models.CharField(db_column='exchangeDesc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    soldnum = models.IntegerField(db_column='soldNum')  # Field name made lowercase.
    text_string = models.CharField(max_length=2000, blank=True, null=True)
    img_list = models.CharField(max_length=2000, blank=True, null=True)
    size_price = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detail_data'


class DiffTable(models.Model):
    #id = models.IntegerField(blank=True, null=True)
    productid = models.CharField(db_column='productId', max_length=50,blank=True, null=True)  # Field name made lowercase.
    diff = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'diff_table'


class TempTable(models.Model):
    #id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    productid = models.CharField(db_column='productId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    price = models.IntegerField()
    size_list = models.CharField(max_length=100, blank=True, null=True)
    brand_id = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    articlenumber = models.CharField(db_column='articleNumber', max_length=100, blank=True, null=True)  # Field name made lowercase.
    authprice = models.IntegerField(db_column='authPrice')  # Field name made lowercase.
    selldate = models.CharField(db_column='sellDate', max_length=100, blank=True, null=True)  # Field name made lowercase.
    exchangedesc = models.CharField(db_column='exchangeDesc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    soldnum = models.IntegerField(db_column='soldNum')  # Field name made lowercase.
    text_string = models.CharField(max_length=2000, blank=True, null=True)
    img_list = models.CharField(max_length=2000, blank=True, null=True)
    size_price = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'temp_table'