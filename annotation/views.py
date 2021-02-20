from annotation.filters import AnnotationFilter
from annotation.models import Annotation
from annotation.serializers import AnnotationSerializer, CategorySerializer
from datasetManage.settings import LOCAL_OR_OSS
from image.models import Category
from utils.utils import get_response
from utils.viewset import ModelViewSet


class ImageView(ModelViewSet):
    http_method_names = ["get", "patch"]
    queryset = Annotation.objects.filter(is_active=1, status=0) \
        .values_list(
        f"img__{LOCAL_OR_OSS}", "classify__value", "other_classify", "classify_id",
        "id", "pred", "other_pred", named=1
    )
    serializer_class = AnnotationSerializer
    filter_class = AnnotationFilter
    updated_files = {"classify_id"}

    def get_serializer_context(self):
        result = super(ImageView, self).get_serializer_context()
        result["category_dict"] = dict(Category.objects.filter(is_active=1).values_list("id", "value"))
        return result

    def update(self, request, *args, **kwargs):
        Annotation.objects.filter(id=kwargs["pk"]).update(
            **{k: request.data[k] for k in set(request.data) & self.updated_files})
        return self.retrieve(request, *args, **kwargs)


class CategoryView(ModelViewSet):
    http_method_names = ["get"]
    serializer_class = CategorySerializer
    queryset = Annotation.objects.filter(is_active=1, status=0) \
        .values_list("classify_id", "classify__value", named=1)


class OverView(ModelViewSet):
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        classify_id = request.data.get("classify_id")
        datetime = request.data.get("datetime")
        assert classify_id and datetime

        Annotation.objects.filter(is_active=1, status=0, classify_id=classify_id, c_time__lt=datetime).update(status=1)
        return get_response(msg="更新成功")

