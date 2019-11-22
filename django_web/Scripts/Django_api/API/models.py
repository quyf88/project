from django.db import models


class Area(models.Model):
    id = models.IntegerField(primary_key=True)
    areaid = models.CharField(db_column='areaID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    area = models.CharField(max_length=60, blank=True, null=True)
    father = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'area'


class City(models.Model):
    id = models.IntegerField(primary_key=True)
    cityid = models.CharField(db_column='cityID', max_length=6, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(max_length=50, blank=True, null=True)
    father = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'city'


class Povince(models.Model):
    id = models.IntegerField(primary_key=True)
    provinceid = models.CharField(db_column='provinceID', max_length=6, blank=True, null=True)  # Field name made lowercase.
    province = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'povince'
