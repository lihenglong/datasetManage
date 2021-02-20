from django.db import models

# Create your models here.
from image.models import Image, Category
from utils.base_model import TimeModel, IsActiveModel


class Annotation(TimeModel, IsActiveModel):
    img = models.ForeignKey(Image, on_delete=models.CASCADE, verbose_name="图片")

    # top1
    classify = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="分类")
    # , 隔开 n=100
    other_classify = models.CharField("top2-n的分类", max_length=511, default="")

    # 5位小数
    pred = models.CharField("top1的置信度", max_length=31, default="")
    other_pred = models.CharField("top2-n的置信度", max_length=1023, default="")

    # 0 待审核， 1 已审核
    status = models.SmallIntegerField(verbose_name="状态信息", default=0)

    class Meta:
        verbose_name = "标注表"
