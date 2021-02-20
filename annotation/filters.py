# _*_coding:utf-8_*_
# __author: guo
from django_filters import rest_framework as filters
from .models import *


class BookFilter(filters.FilterSet):
    classify_id = filters.NumberFilter(label="类别", field_name="classify_id")

    class Meta:
        model = Annotation
        fields = []
