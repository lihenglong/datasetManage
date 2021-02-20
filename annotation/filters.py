# _*_coding:utf-8_*_
# __author: guo
from django_filters import rest_framework as filters
from .models import *


class AnnotationFilter(filters.FilterSet):
    classify_id = filters.NumberFilter(label="类别", field_name="classify_id")
    datetime = filters.DateTimeFilter(field_name="c_time", lookup_expr="lt")

    class Meta:
        model = Annotation
        fields = []
