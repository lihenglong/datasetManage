# _*_coding:utf-8_*_
# __author: guo
import re

from rest_framework import serializers

from datasetManage.settings import LOCAL_OR_OSS
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    classify = serializers.SerializerMethodField()

    def get_classify(self, instance):
        return getattr(instance, f"classify__value")

    class Meta:
        model = Annotation
        fields = [
            "classify_id", "classify"
        ]


class AnnotationSerializer(CategorySerializer):
    src = serializers.SerializerMethodField()
    recommend = serializers.SerializerMethodField()

    def get_recommend(self, instance):
        return [self.context["category_dict"].get(int(i), "") for i in re.findall(r"\d+", instance.top_num)[:10]]

    def get_src(self, instance):
        return getattr(instance, f"img__{LOCAL_OR_OSS}")

    class Meta:
        model = Annotation
        fields = [
            "id", "src", "classify_id", "classify", "recommend"
        ]
