# _*_coding:utf-8_*_
# __author: guo
from django_filters.rest_framework import DjangoFilterBackend


class MyDjangoFilterBackend(DjangoFilterBackend):
    raise_exception = False
