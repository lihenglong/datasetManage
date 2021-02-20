# _*_coding:utf-8_*_
# __author: guo
from django.db import models


class TimeModel(models.Model):
    c_time = models.DateTimeField('创建时间', auto_now_add=True)
    u_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        abstract = True


class IsActiveModel(models.Model):

    is_active = models.BooleanField(verbose_name='逻辑删除', default=True)

    class Meta:
        abstract = True
