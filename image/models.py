from django.db import models

from utils.base_model import TimeModel, IsActiveModel
from mptt.models import MPTTModel, TreeForeignKey


class Category(TimeModel, IsActiveModel, MPTTModel):
    value = models.CharField("类别", max_length=511, default="")
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name = "分类表"


class Image(TimeModel, IsActiveModel):
    local_path = models.CharField("本地路径", max_length=511, default="")
    oss_path = models.CharField("oss路径", max_length=511, default="")
    upload_time = models.DateTimeField("上传时间", auto_now_add=True)

    class Meta:
        verbose_name = "图片表"
