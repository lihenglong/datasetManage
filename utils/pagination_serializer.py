# -*- coding: utf-8  -*-
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination


class CustomPaginationSerializer(LimitOffsetPagination):
    def get_paginated_response(self, data):
        return Response({
            "success": True,
            "msg": "数据获取成功",
            "data": {
                "count": self.count,
                "results": data
            }
        })


class StandardResultSetPagination(LimitOffsetPagination):
    # 默认每页显示的条数
    default_limit = 10
    # url 中传入的显示数据条数的参数
    limit_query_param = 'limit'
    # url中传入的数据位置的参数
    offset_query_param = 'offset'
    # 最大每页显示条数
    max_limit = 10000
