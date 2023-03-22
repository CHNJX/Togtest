# -*- coding:utf-8 -*-
# @Time     :2023/1/15 3:13 下午
# @Author   :CHNJX
# @File     :custom_pagination.py
# @Desc     :自定义分页类

from rest_framework import status
from rest_framework.pagination import PageNumberPagination as _PageNumberPagination

from api.utils.custom_json_response import JsonResponse


class PageNumberPagination(_PageNumberPagination):
    page_size = 10

    # Client can control the page using this query parameter.
    page_query_param = 'page'
    page_query_description = '页码设置'

    page_size_query_param = 'size'
    page_size_query_description = '页码设置'

    max_page_size = 100

    invalid_page_message = '错误页码'

    def get_paginated_response(self, data):
        resp = super().get_paginated_response(data)
        resp.data['current_page'] = self.page.number
        return JsonResponse(data=resp.data, code=200, msg="success", status=status.HTTP_200_OK)
