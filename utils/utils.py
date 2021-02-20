# _*_coding:utf-8_*_
# __author: guo
import datetime

from rest_framework.response import Response


def get_response(data='', success=True, msg='数据获取成功', **kwargs):
    data = {
        "success": success,
        "msg": msg,
        "data": data,
        "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    data.update(kwargs)
    return Response(data)
