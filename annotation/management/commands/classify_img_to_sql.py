# _*_coding:utf-8_*_
# __author: guo
import json
import os

import numpy as np
from django.core.management.base import BaseCommand

from django.db import transaction
import tensorflow as tf
from tensorflow import keras

from annotation.models import Annotation
from datasetManage.settings import model_path
from image.models import Category, Image
from sentry_sdk import capture_exception

np.set_printoptions(suppress=True)


class Command(BaseCommand):
    """添加用户"""
    model_file = "model.h5"
    conf_file = "conf.json"
    class_file = "class_name.json"
    img_suffix = {"jpg", "jpeg", "JPEG", "png", "JPG", "PNG", "gif", "bmp"}
    one_num = 100
    top_num = 30

    def get_file_data(self, json_file):
        with open(json_file, "r") as fr:
            data = json.loads(fr.read())
        return data

    def gen_keras_data(self, img_list, size):
        img = []
        for _img_path in img_list:
            try:
                _x = tf.keras.preprocessing.image.load_img(_img_path, target_size=size)
            except Exception as e:
                capture_exception(e)
                print(_img_path, e)
                continue

            _x = tf.keras.preprocessing.image.img_to_array(_x)
            _x = np.expand_dims(_x, axis=0)
            img.append(_x)

        x = np.concatenate([x for x in img])
        return x

    def _get_img_dict(self):
        result = {}
        path = "/home/dd/Share/dataset_pool/imgs"
        for root, _, files in os.walk(path):
            for file in files:
                if "." in file and file.rsplit(".", 1)[1] in self.img_suffix:
                    result[os.path.join(root, file)] = "https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=3952160391,2864289195&fm=26&gp=0.jpg"
        return result

    def handle(self, *args, **options):
        path_dict = self._get_img_dict()
        # path_dict = {
        #     "/Users/guo/Documents/data/image/数据集/四分类数据集/厨余垃圾_鹌鹑蛋/img_鹌鹑蛋_1.jpeg": "https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=3952160391,2864289195&fm=26&gp=0.jpg",
        #     "/Users/guo/Documents/data/image/数据集/四分类数据集/厨余垃圾_鹌鹑蛋/img_鹌鹑蛋_2.jpeg": "https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=3952160391,2864289195&fm=26&gp=0.jpg",
        #     "/Users/guo/Documents/data/image/数据集/四分类数据集/厨余垃圾_鹌鹑蛋/img_鹌鹑蛋_3.jpeg": "https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=3952160391,2864289195&fm=26&gp=0.jpg",
        # }

        path_list = list(path_dict)
        model = keras.models.load_model(os.path.join(model_path, self.model_file))
        size = self.get_file_data(os.path.join(model_path, self.conf_file))["img_size"]
        class_names = list(self.get_file_data(os.path.join(model_path, self.class_file)).values())

        class_name__id_dict = dict(Category.objects.filter(is_active=1).values_list("value", "id"))

        # bulk_category_data = []
        for class_name in set(class_names) - set(class_name__id_dict):
            obj = Category.objects.create(value=class_name)
            class_name__id_dict[class_name] = obj.id

        for i in range(0, len(path_list), self.one_num):
            img_path = path_list[i: i + self.one_num]
            img_data = self.gen_keras_data(img_path, size)
            predictions = model.predict(img_data)

            # 获取前一百的识别结果
            for index, one_pred in enumerate(predictions):

                local_path = img_path[index]
                try:
                    with transaction.atomic():
                        img_obj = Image.objects.create(local_path=local_path, oss_path=path_dict[local_path])

                        index_sort_list = np.argsort(one_pred)[::-1]

                        other_classify = []
                        other_pred = []
                        # print(self.top_num)
                        # print(one_pred)
                        for j in range(1, min(self.top_num, len(one_pred)) + 1):
                            classify_index = index_sort_list[j]
                            if one_pred[classify_index] < 0.001:
                                break

                            other_pred.append(str(round(one_pred[classify_index], 3)))
                            other_classify.append(str(class_name__id_dict[class_names[classify_index]]))

                        other_pred = ",".join(other_pred)
                        other_classify = ",".join(other_classify)
                        classify = class_name__id_dict[class_names[index_sort_list[0]]]
                        pred = str(round(one_pred[index_sort_list[0]], 3))

                        Annotation.objects.create(
                            img=img_obj, classify_id=classify, pred=pred,
                            other_classify=other_classify, other_pred=other_pred
                        )
                except Exception as e:
                    # raise e
                    # print(e)
                    # capture_exception(e)
                    continue
