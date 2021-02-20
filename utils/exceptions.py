# -*- coding: utf-8 -*-
import re

from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.exceptions import PermissionDenied as RestPermissionDenied, AuthenticationFailed, NotAuthenticated
from django.core.exceptions import PermissionDenied
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from django.http import Http404
from django.core.exceptions import (ObjectDoesNotExist, )

SYSTEM_ERROR = 0000


def ErrorResponse(msg=u'服务器异常', status=status.HTTP_400_BAD_REQUEST, headers=None,
                  code=None, *args, **kwargs):
    err = {
        'success': False,
        'msg': msg,
    }
    if code:
        err["code"] = code

    return Response(err, status, headers=headers)


class Error(exceptions.APIException):

    def __init__(self, err_code=SYSTEM_ERROR, msg=u'服务器异常', status_code=status.HTTP_400_BAD_REQUEST):
        self.err_code = err_code
        self.default_detail = msg
        self.status_code = status_code

    def __unicode__(self):
        return u'[Error] %d: %s(%d)' % (self.err_code, self.default_detail, self.status_code)

    def getResponse(self):
        return ErrorResponse(error_code=self.err_code, msg=self.default_detail, status=self.status_code)


def custom_exception_handler(exc, context):
    from rest_framework.views import set_rollback

    if isinstance(exc, Error):
        set_rollback()
        return exc.getResponse()

    if isinstance(exc, NotAuthenticated):
        data = {'msg': exc.detail, 'success': False}
        set_rollback()
        return ErrorResponse(error_code=SYSTEM_ERROR, status=NotAuthenticated.status_code, **data)

    if isinstance(exc, AuthenticationFailed):
        data = {'msg': exc.detail, 'success': False}
        set_rollback()
        return ErrorResponse(error_code=SYSTEM_ERROR, status=AuthenticationFailed.status_code, **data)

    if isinstance(exc, (RestPermissionDenied, PermissionDenied)):
        msg = _('Permission denied.')
        data = {
            'msg': six.text_type(msg),
            'success': False
        }
        exc_message = str(exc)
        if 'CSRF' in exc_message:
            data['msg'] = exc_message

        set_rollback()
        return ErrorResponse(error_code=SYSTEM_ERROR, status=status.HTTP_403_FORBIDDEN, **data)

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        set_rollback()
        return ErrorResponse(error_code=SYSTEM_ERROR, msg=exc.detail, status=status.HTTP_200_OK, headers=headers)

    if isinstance(exc, (Http404, ObjectDoesNotExist)):
        msg = _('Not found.')
        data = {'msg': six.text_type(msg), 'success': False}

        set_rollback()
        return ErrorResponse(error_code=SYSTEM_ERROR, status=status.HTTP_404_NOT_FOUND, **data)

    if isinstance(exc, IntegrityError) and re.search(r"Duplicate entry '.*?' for key '.*?'", exc.args[1]):
        msg = _('数据重复！')
        data = {'msg': six.text_type(msg), 'success': False}

        set_rollback()
        return ErrorResponse(error_code=SYSTEM_ERROR, status=status.HTTP_400_BAD_REQUEST, **data)
