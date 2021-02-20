from annotation.filters import BookFilter
from annotation.models import Annotation
from annotation.serializers import AnnotationSerializer, CategorySerializer
from datasetManage.settings import LOCAL_OR_OSS
from image.models import Category
from utils.viewset import ModelViewSet


class ImageView(ModelViewSet):
    http_method_names = ["get"]
    queryset = Annotation.objects.filter(is_active=1, status=0) \
        .values_list(f"img__{LOCAL_OR_OSS}", "classify__value", "top_num", "classify_id", named=1)
    serializer_class = AnnotationSerializer
    filter_class = BookFilter

    def get_serializer_context(self):
        result = super(ImageView, self).get_serializer_context()
        result["category_dict"] = dict(Category.objects.filter(is_active=1).values_list("id", "value"))
        return result


class CategoryView(ModelViewSet):
    http_method_names = ["get"]
    serializer_class = CategorySerializer
    queryset = Annotation.objects.filter(is_active=1, status=0) \
        .values_list("classify_id", "classify__value", named=1)
