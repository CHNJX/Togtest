# -*- coding:utf-8 -*-
# @Time     :2023/3/21 10:20 下午
# @Author   :CHNJX
# @File     :api_views.py
# @Desc     :项目视图
from rest_framework import status
from rest_framework.decorators import action

from api.models import Project, Environment
from api.serializer import ProjectSerializer, EnvironmentSerializer, EnvironmentSelectSerializer
from api.utils.custom_json_response import JsonResponse
from api.utils.custom_pagination import PageNumberPagination
from api.utils.custom_view_set import CustomModelViewSet


class ProjectView(CustomModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = PageNumberPagination


class EnvView(CustomModelViewSet):
    queryset = Environment.objects.all()
    serializer_class = EnvironmentSerializer
    pagination_class = PageNumberPagination

    @action(methods=['GET'], detail=False)
    def tree_list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset().filter(project_id=request.query_params['project_id']))
        serializer = self.get_serializer(qs, many=True)
        return JsonResponse(data=serializer.data, msg='成功', status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == 'tree_list':
            return EnvironmentSelectSerializer
