# _*_coding:utf-8_*_
# __author: guo
import re

from rest_framework import serializers

from datasetManage.settings import LOCAL_OR_OSS
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    classify = serializers.SerializerMethodField()
    classify_count = serializers.SerializerMethodField()

    def get_classify_count(self, instance):
        return getattr(instance, f"classify_count")

    def get_classify(self, instance):
        return getattr(instance, f"classify__value")

    class Meta:
        model = Annotation
        fields = [
            "classify_id", "classify", "classify_count"
        ]


class AnnotationSerializer(CategorySerializer):
    src = serializers.SerializerMethodField()
    recommend = serializers.SerializerMethodField()

    def get_recommend(self, instance):
        other_classify = re.findall(r"\d+", instance.other_classify)
        other_pred = re.findall(r"(\d+\.\d+)", instance.other_pred)
        result = [
            {
                "id": int(classify),
                "value": self.context["category_dict"].get(int(classify), ""),
                "pred": other_pred[i]
            }
            for i, classify in enumerate(other_classify[:10])
        ]
        return result

    def get_src(self, instance):
        return getattr(instance, f"img__{LOCAL_OR_OSS}")

    class Meta:
        model = Annotation
        fields = [
            "id", "src", "classify_id", "classify", "recommend", "pred"
        ]


class CategoryAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id", "value"
        ]
