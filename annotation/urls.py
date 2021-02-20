# _*_coding:utf-8_*_
# __author: guo
# from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r"image", views.ImageView, basename="image")
router.register(r"category", views.CategoryView, basename="category")
router.register(r"over", views.OverView, basename="over")

urlpatterns = [
    url(r'^', include(router.urls)),
]
